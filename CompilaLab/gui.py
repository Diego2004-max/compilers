"""Interfaz local Tkinter, sin dependencias externas."""
import json
import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path
from compiler import compile_source
from coverage import COVERAGE
from native_backend import build_native, NativeError, find_compiler

BASE=Path(__file__).resolve().parent
root=tk.Tk(); root.title('CompilaLab v10 | Laboratorio integral de compiladores'); root.geometry('1420x850')
root.configure(bg='#101b2c')
style=ttk.Style(); style.theme_use('clam')
style.configure('TNotebook',background='#101b2c'); style.configure('TNotebook.Tab',padding=(15,9))
header=tk.Frame(root,bg='#101b2c'); header.pack(fill='x',padx=20,pady=(14,8))
tk.Label(header,text='CompilaLab',font=('Segoe UI',24,'bold'),fg='#e9f4ff',bg='#101b2c').pack(side='left')
tk.Label(header,text='  Lexer → AST → Semántica → TAC → CPU / RAM',font=('Segoe UI',11),fg='#92a6bf',bg='#101b2c').pack(side='left',padx=14)
bar=tk.Frame(root,bg='#101b2c'); bar.pack(fill='x',padx=20,pady=7)
reg=tk.IntVar(value=3); optimize=tk.BooleanVar(value=False)
tk.Label(bar,text='Registros:',bg='#101b2c',fg='white').pack(side='left')
ttk.Spinbox(bar,from_=3,to=16,textvariable=reg,width=4).pack(side='left',padx=6)
ttk.Checkbutton(bar,text='Activar optimización',variable=optimize).pack(side='left',padx=15)
status=tk.StringVar(value='Preparado para compilar')
main=tk.PanedWindow(root,orient='horizontal',sashwidth=7,bg='#101b2c'); main.pack(fill='both',expand=True,padx=20,pady=8)
left=tk.Frame(main,bg='#17263a'); right=tk.Frame(main,bg='#17263a'); main.add(left,minsize=350,width=450); main.add(right,minsize=500)
tk.Label(left,text='CÓDIGO FUENTE',font=('Segoe UI',11,'bold'),bg='#17263a',fg='white').pack(anchor='w',padx=12,pady=10)
editor=tk.Text(left,font=('Consolas',12),bg='#0e1828',fg='#dceeff',insertbackground='white',undo=True,wrap='none',padx=12,pady=12)
editor.pack(fill='both',expand=True,padx=12,pady=(0,12)); editor.insert('1.0',(BASE/'examples'/'correcto.clab').read_text(encoding='utf-8'))
notebook=ttk.Notebook(right); notebook.pack(fill='both',expand=True,padx=12,pady=12)
views={}
for name in ['Tokens','Autómatas','Gramática','AST','Símbolos','TAC','Optimización','Ensamblador','Spill','Memoria','CPU virtual','Paso a paso','Cobertura','Salida','C nativo','Salida nativa']:
    frame=tk.Frame(notebook,bg='#0e1828'); notebook.add(frame,text=name)
    widget=tk.Text(frame,font=('Consolas',11),bg='#0e1828',fg='#dceeff',insertbackground='white',wrap='none',padx=14,pady=14)
    widget.pack(fill='both',expand=True); views[name]=widget

last_result={}
step_index=tk.IntVar(value=0)

def show_step():
    trace=last_result.get('cpu_trace',[])
    if not trace:
        message='Sin traza. Compila un programa válido.'
    else:
        index=max(0,min(step_index.get(),len(trace)-1)); step_index.set(index)
        message=json.dumps({'paso':index+1,'total':len(trace),**trace[index]},ensure_ascii=False,indent=2)
    w=views['Paso a paso']; w.delete('1.0','end'); w.insert('1.0',message)

def advance_step(delta):
    step_index.set(step_index.get()+delta); show_step(); notebook.select(list(views).index('Paso a paso'))

def compile_action():
    r=compile_source(editor.get('1.0','end-1c'),reg.get(),optimize.get())
    last_result.clear(); last_result.update(r); step_index.set(0)
    data={'Tokens':r.get('tokens',[]),'Autómatas':r.get('automata',[]),'Gramática':r.get('grammar',''),'AST':r.get('ast',{}),'Símbolos':r.get('symbols',[]),'TAC':r.get('tac',[]),'Optimización':{'notas':r.get('optimizations',[]),'tac':r.get('optimized_tac',[])},'Ensamblador':r.get('assembly',[]),'Spill':{'cantidad':r.get('spill_count',0),'eventos':r.get('register_events',[]),'slots':r.get('register_slots',{})},'Memoria':{'eventos':r.get('memory_events',[]),'variables':r.get('globals',{}),'heap_pendiente':r.get('heap_remaining',{})},'CPU virtual':{'salida_cpu':r.get('cpu_output',[]),'coincide_con_tac':r.get('cpu_matches_tac'),'registros_finales':r.get('cpu_registers',{}),'ram_spill':r.get('cpu_ram',{}),'heap_final':r.get('cpu_heap_remaining',{}),'eventos_memoria':r.get('cpu_memory_events',[]),'traza':r.get('cpu_trace',[])},'Paso a paso':{},'Cobertura':[{'semana':week,'concepto':concept,'ubicacion':location,'estado':status} for week,concept,location,status in COVERAGE],'Salida':r.get('output',[])}
    for key,value in data.items():
        w=views[key]; w.delete('1.0','end'); w.insert('1.0','\n'.join(map(str,value)) if isinstance(value,list) and key not in ('Tokens','Símbolos') else json.dumps(value,ensure_ascii=False,indent=2))
    show_step()
    status.set(('✓ Compilación exitosa · Spill: '+str(r.get('spill_count',0))) if r['success'] else '✗ '+r['error'])
    notebook.select(list(views).index('Salida') if r['success'] else 0)

def native_action():
    # Traduce el programa al AST, genera C11, invoca GCC/Clang y ejecuta el binario real.
    try:
        result = build_native(editor.get('1.0', 'end-1c'))
        for tab, value in [('C nativo', result['c_source']), ('Salida nativa', result['output'])]:
            views[tab].delete('1.0', 'end')
            views[tab].insert('1.0', value)
        status.set('✓ Compilación NATIVA exitosa: ' + result['executable'])
        notebook.select(list(views).index('Salida nativa'))
    except Exception as error:
        # La interfaz informa el error y permanece abierta.
        views['Salida nativa'].delete('1.0', 'end')
        views['Salida nativa'].insert('1.0', str(error))
        status.set('✗ Compilación nativa fallida: ' + str(error)[:110])
        notebook.select(list(views).index('Salida nativa'))

def open_action():
    file=filedialog.askopenfilename(filetypes=[('CompilaLab','*.clab'),('Todos','*.*')])
    if file: editor.delete('1.0','end'); editor.insert('1.0',Path(file).read_text(encoding='utf-8'))

def example(name):
    editor.delete('1.0','end'); editor.insert('1.0',(BASE/'examples'/name).read_text(encoding='utf-8')); compile_action()

ttk.Button(bar,text='▶ Compilar y ejecutar',command=compile_action).pack(side='left',padx=8)
ttk.Button(bar,text='▶ Ejecutable REAL (GCC/Clang)',command=native_action).pack(side='left',padx=5)
ttk.Button(bar,text='Abrir archivo',command=open_action).pack(side='left',padx=8)
for label,name in [('Correcto','correcto.clab'),('Spill','spill.clab'),('Tipos','tipos_error.clab'),('Stack / Heap','memoria.clab'),('Optimiz.','optimizacion.clab')]:
    ttk.Button(bar,text=label,command=lambda n=name:example(n)).pack(side='left',padx=3)
ttk.Button(bar,text='◀ CPU',command=lambda:advance_step(-1)).pack(side='left',padx=3)
ttk.Button(bar,text='CPU ▶',command=lambda:advance_step(1)).pack(side='left',padx=3)
tk.Label(root,textvariable=status,anchor='w',font=('Segoe UI',11),bg='#101b2c',fg='#86d8c5').pack(fill='x',padx=20,pady=(0,12))
compile_action(); root.mainloop()
