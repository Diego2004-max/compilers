/* CompilaLab · panel web. JavaScript sin librerías: todo se dibuja con DOM y SVG. */
'use strict';

const $ = (sel, root = document) => root.querySelector(sel);
const esc = (v) => String(v ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const SVGNS = 'http://www.w3.org/2000/svg';

async function api(path, body) {
  const res = await fetch(path, body === undefined ? {} : {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || res.statusText);
  return data;
}

/* ════════════════ navegación ════════════════ */
const views = { pipeline: $('#view-pipeline'), bench: $('#view-bench'), arch: $('#view-arch') };
document.querySelectorAll('.tabs button').forEach((btn) => btn.addEventListener('click', () => showView(btn.dataset.view)));
function showView(name) {
  document.querySelectorAll('.tabs button').forEach((b) => b.setAttribute('aria-selected', String(b.dataset.view === name)));
  Object.entries(views).forEach(([k, el]) => { el.hidden = k !== name; });
  if (name === 'arch') renderArch();
  if (name === 'bench') redrawCharts();
}

/* ════════════════ PIPELINE ════════════════ */
const FAILING = new Set(['errores_lexicos', 'errores_sintacticos', 'error_semantico', 'tipos_error']);
const STAGES = [
  { id: 'lexico', name: 'Léxico', unit: 'tokens', phase: 'Léxico', metric: (r) => r.tokens && r.tokens.length - 1 },
  { id: 'sintactico', name: 'Sintaxis', unit: 'nodos del AST', phase: 'Sintáctico', metric: (r) => r.ast && countNodes(r.ast) },
  { id: 'semantico', name: 'Semántica', unit: 'símbolos', phase: 'Semántico', metric: (r) => r.symbols && r.symbols.length },
  { id: 'tac', name: 'TAC', unit: 'cuádruplas', metric: (r) => r.raw_quads && r.raw_quads.length },
  { id: 'optimizacion', name: 'Optimización', unit: 'cuádruplas finales', metric: (r) => r.optimized_tac && r.optimized_tac.length },
  { id: 'ensamblador', name: 'Ensamblador', unit: 'instrucciones', metric: (r) => r.assembly && r.assembly.length },
  { id: 'cpu', name: 'CPU virtual', unit: 'pasos ejecutados', metric: (r) => r.cpu_trace && r.cpu_trace.length },
];
const state = { result: null, stage: 'lexico', step: 0, timer: null, examples: {} };

function countNodes(n) { return 1 + (n.children || []).reduce((s, c) => s + countNodes(c), 0); }

function failIndex(r) {
  if (!r || r.success) return -1;
  const byPhase = { 'Léxico': 0, 'Sintáctico': 1, 'Semántico': 2 };
  if (r.error_phase in byPhase) return byPhase[r.error_phase];
  return r.assembly ? 6 : 5;
}

function renderCinta() {
  const r = state.result;
  const fail = failIndex(r);
  $('#cinta').innerHTML = STAGES.map((s, i) => {
    let cls = 'pending';
    let metric = '–';
    if (r) {
      if (fail === -1 || i < fail) { cls = 'done'; metric = s.metric(r) ?? '–'; }
      else if (i === fail) { cls = 'failed'; metric = 'error'; }
    }
    let unit = s.unit;
    if (s.id === 'ensamblador' && r && r.spill_count != null && cls === 'done') unit = `instrucciones, ${r.spill_count} spill${r.spill_count === 1 ? '' : 's'}`;
    return `<li><button class="station ${cls}" role="tab" aria-selected="${state.stage === s.id}" data-stage="${s.id}">
      <span class="n">${i + 1}</span><span class="name">${s.name}</span>
      <span class="metric">${esc(metric)}</span><span class="unit">${esc(unit)}</span></button></li>`;
  }).join('');
  $('#cinta').querySelectorAll('.station').forEach((b) => b.addEventListener('click', () => selectStage(b.dataset.stage)));
}

function selectStage(id) {
  state.stage = id;
  stopPlay();
  renderCinta();
  renderDetail();
}

/* editor con numeración de líneas */
const code = $('#code');
const gutter = $('#gutter');
function updateGutter(errLine) {
  const n = code.value.split('\n').length;
  gutter.innerHTML = Array.from({ length: n }, (_, i) => (i + 1 === errLine ? `<span class="err">${i + 1}</span>` : String(i + 1))).join('\n');
  gutter.scrollTop = code.scrollTop;
}
code.addEventListener('input', () => updateGutter());
code.addEventListener('scroll', () => { gutter.scrollTop = code.scrollTop; });
code.addEventListener('keydown', (e) => {
  if (e.key === 'Tab') { e.preventDefault(); code.setRangeText('    ', code.selectionStart, code.selectionEnd, 'end'); updateGutter(); }
  if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) { e.preventDefault(); compile(); }
});

async function loadExamples() {
  state.examples = await api('/api/examples');
  const names = Object.keys(state.examples);
  const label = (n) => (FAILING.has(n) ? `${n} (con error)` : n);
  $('#example').innerHTML = names.map((n) => `<option value="${n}">${esc(label(n))}</option>`).join('');
  $('#bench-example').innerHTML = names.filter((n) => !FAILING.has(n)).map((n) => `<option>${n}</option>`).join('');
  const start = names.includes('spill') ? 'spill' : names[0];
  $('#example').value = start;
  $('#bench-example').value = start;
  code.value = state.examples[start];
  updateGutter();
}
$('#example').addEventListener('change', (e) => { code.value = state.examples[e.target.value]; updateGutter(); compile(); });
$('#compile').addEventListener('click', compile);
$('#optimized').addEventListener('change', compile);
$('#registers').addEventListener('change', compile);

async function compile() {
  const btn = $('#compile');
  btn.disabled = true;
  try {
    const registers = Math.max(3, Math.min(16, Number($('#registers').value) || 3));
    $('#registers').value = registers;
    const r = await api('/api/compile', { source: code.value, registers, optimized: $('#optimized').checked });
    state.result = r;
    state.step = 0;
    const fail = failIndex(r);
    // Tras compilar, se abre la fase que falló, o se conserva la que el usuario estaba mirando.
    if (fail >= 0) state.stage = STAGES[fail].id;
    renderStatus();
    renderCinta();
    renderDetail();
  } catch (err) {
    $('#status').className = 'status fail';
    $('#status').innerHTML = `<b>No se pudo contactar al compilador</b>${esc(err.message)}. Verifica que <code>python dashboard.py</code> siga abierto.`;
  } finally {
    btn.disabled = false;
  }
}

function renderStatus() {
  const r = state.result;
  const st = $('#status');
  const total = Object.values(r.timings || {}).reduce((a, b) => a + b, 0);
  if (r.success) {
    st.className = 'status ok';
    st.innerHTML = `<b>Compilado y ejecutado en ${fmtMs(total)}</b>${r.spill_count} spill${r.spill_count === 1 ? '' : 's'} con ${$('#registers').value} registros${$('#optimized').checked ? ', con optimización' : ''}.`;
  } else {
    st.className = 'status fail';
    const phaseName = { 'Léxico': 'el análisis léxico', 'Sintáctico': 'el análisis sintáctico', 'Semántico': 'el análisis semántico', 'Ejecución': 'la ejecución' }[r.error_phase] || 'la compilación';
    st.innerHTML = `<b>Falló ${phaseName}</b>${esc(r.error)}`;
  }
  const m = /línea (\d+)/.exec(r.error || '');
  updateGutter(m ? Number(m[1]) : null);
  $('#output').textContent = (r.output || []).join('\n');
  $('#match').innerHTML = r.success
    ? '<span class="badge ok">TAC y CPU coinciden</span>'
    : '';
}

/* ── paneles de detalle por fase ── */
function head(title, text, extra = '') {
  return `<div class="detail-head"><div><h2>${title}</h2><p>${text}</p></div>${extra}</div>`;
}

function renderDetail() {
  const el = $('#detail');
  const r = state.result;
  if (!r) { el.innerHTML = '<p class="empty">Compila un programa para ver qué hace cada fase.</p>'; return; }
  const idx = STAGES.findIndex((s) => s.id === state.stage);
  const fail = failIndex(r);
  if (fail >= 0 && idx === fail) { el.innerHTML = renderFailure(r, STAGES[idx]); return; }
  if (fail >= 0 && idx > fail) {
    el.innerHTML = head(STAGES[idx].name, `Esta fase no se ejecutó: el compilador se detuvo en la fase ${STAGES[fail].name}. Cada fase es un filtro y solo recibe la salida de una fase exitosa.`);
    return;
  }
  const render = { lexico: renderTokens, sintactico: renderAst, semantico: renderSymbols, tac: renderTac, optimizacion: renderOpt, ensamblador: renderAsm, cpu: renderCpu }[state.stage];
  el.innerHTML = '';
  render(el, r);
}

function renderFailure(r, stage) {
  const why = {
    'Léxico': 'El analizador léxico encontró texto que no corresponde a ningún patrón del lenguaje. Revisa caracteres fuera del alfabeto o cadenas y comentarios sin cerrar.',
    'Sintáctico': 'Los tokens son válidos, pero su orden no encaja en ninguna regla de la gramática.',
    'Semántico': 'La estructura es correcta, pero el significado no: una variable no existe, los tipos no son compatibles o se usa algo fuera de su ámbito.',
    'Ejecución': 'El programa compiló, pero falló al ejecutarse: el valor problemático solo se conoce en tiempo de ejecución.',
  }[r.error_phase] || '';
  return head(`Error en ${stage.name}`, why) + `<div class="error-box">${esc(r.error)}${caretView(r.error)}</div>`;
}

/* Muestra la línea del fuente con un ^ bajo la columna del error, como hacen gcc o clang. */
function caretView(message) {
  const m = /línea (\d+), columna (\d+)/.exec(message || '');
  if (!m) return '';
  const text = code.value.split('\n')[Number(m[1]) - 1];
  if (text === undefined) return '';
  return `<pre class="caret">${esc(text)}\n${' '.repeat(Math.max(0, Number(m[2]) - 1))}<span>^</span></pre>`;
}

function renderTokens(el, r) {
  const toks = r.tokens.filter((t) => t.kind !== 'EOF');
  const kinds = {};
  toks.forEach((t) => { const k = /^[A-Z]+$/.test(t.kind) ? t.kind : 'operador'; kinds[k] = (kinds[k] || 0) + 1; });
  el.innerHTML = head('Análisis léxico',
    'La regex maestra recorre el texto de izquierda a derecha y agrupa caracteres en tokens. Espacios y comentarios se descartan, pero siguen moviendo la columna.',
    `<div class="chips">${Object.entries(kinds).map(([k, v]) => `<span class="chip">${esc(k)} <b>${v}</b></span>`).join('')}</div>`) +
    `<div class="two"><div class="table-wrap"><table><thead><tr><th class="num">#</th><th>Lexema</th><th>Token</th><th class="num">Línea</th><th class="num">Col.</th></tr></thead><tbody>${
      toks.map((t, i) => `<tr><td class="num">${i + 1}</td><td class="mono">${esc(t.value)}</td><td><span class="kind">${esc(t.kind)}</span></td><td class="num">${t.line}</td><td class="num">${t.column}</td></tr>`).join('')
    }</tbody></table></div>
    <div><h3>Autómatas finitos deterministas</h3><p class="muted small" style="margin:4px 0 10px">Cada identificador y número se vuelve a reconocer con el AFD de su tabla de transición, para ver los estados que recorre.</p>
    <div class="afd-list">${(r.automata || []).map((a) => `<div class="afd-row"><span class="lex">${esc(a.lexema)}</span>
      <span class="badge ${a.aceptado ? 'ok' : 'fail'}">${a.aceptado ? 'aceptado' : 'rechazado'}</span>
      <span class="afd-step">q0${a.transiciones.map((t) => ` <i>${esc(t.caracter)}</i>→ ${esc(t.hasta)}`).join('')}</span></div>`).join('')}</div></div></div>`;
}

/* AST: layout de árbol por anchos de subárbol, dibujado en SVG */
function astLabel(n) {
  const v = n.value;
  switch (n.kind) {
    case 'program': return ['programa', ''];
    case 'declare': return [`${v.type} ${v.name} =`, 'declaración'];
    case 'assign': return [`${v} =`, 'asignación'];
    case 'binary': return [String(v), 'binaria'];
    case 'not': return ['!', 'unaria'];
    case 'number': return [String(v), 'número'];
    case 'string': return [`"${v}"`, 'cadena'];
    case 'boolean': return [String(v), 'bool'];
    case 'variable': return [String(v), 'variable'];
    case 'function': return [`fn ${v}()`, 'función'];
    case 'call': return [`${v}()`, 'llamada'];
    case 'new': return [`new(${v})`, 'heap'];
    case 'free': return [`free(${v})`, 'heap'];
    default: return [n.kind, ''];
  }
}
function layoutAst(n) {
  const [label, sub] = astLabel(n);
  const w = Math.max(56, label.length * 7.6 + 22, sub.length * 6.2 + 16);
  const kids = (n.children || []).map(layoutAst);
  const kidsW = kids.reduce((s, k) => s + k.span, 0) + Math.max(0, kids.length - 1) * 14;
  return { n, label, sub, w, kids, span: Math.max(w, kidsW) };
}
function placeAst(t, x, depth, out) {
  t.x = x + t.span / 2;
  t.y = 20 + depth * 74;
  out.push(t);
  const kidsW = t.kids.reduce((s, k) => s + k.span, 0) + Math.max(0, t.kids.length - 1) * 14;
  let cx = t.x - kidsW / 2;
  t.kids.forEach((k) => { placeAst(k, cx, depth + 1, out); cx += k.span + 14; });
}
function renderAst(el, r) {
  const tree = layoutAst(r.ast);
  const nodes = [];
  placeAst(tree, 16, 0, nodes);
  const W = tree.span + 32;
  const H = Math.max(...nodes.map((n) => n.y)) + 60;
  let edges = '';
  let boxes = '';
  nodes.forEach((t) => {
    t.kids.forEach((k) => {
      const y1 = t.y + 38; const y2 = k.y; const my = (y1 + y2) / 2;
      edges += `<path class="ast-edge" d="M${t.x} ${y1} C${t.x} ${my} ${k.x} ${my} ${k.x} ${y2}"/>`;
    });
    boxes += `<g class="ast-node k-${t.n.kind}"><title>${esc(t.n.kind)} · línea ${t.n.line}, columna ${t.n.column}</title>
      <rect x="${t.x - t.w / 2}" y="${t.y}" width="${t.w}" height="38" rx="4"/>
      <text x="${t.x}" y="${t.y + (t.sub ? 16 : 23)}" text-anchor="middle">${esc(t.label)}</text>
      ${t.sub ? `<text class="sub" x="${t.x}" y="${t.y + 30}" text-anchor="middle">${esc(t.sub)}</text>` : ''}</g>`;
  });
  el.innerHTML = head('Árbol de sintaxis abstracta',
    'El parser descendente recursivo convierte la lista plana de tokens en un árbol. Los paréntesis y los punto y coma desaparecen: la forma del árbol ya codifica la precedencia (lo más profundo se calcula primero).',
    `<span class="chip">${nodes.length} nodos, profundidad ${Math.round((Math.max(...nodes.map((n) => n.y)) - 20) / 74) + 1}</span>`) +
    `<div class="ast-wrap"><svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="Árbol de sintaxis abstracta">${edges}${boxes}</svg></div>
     <details><summary class="small muted">Ver la gramática EBNF que implementa el parser</summary><pre class="listing" style="padding:10px 14px">${esc(r.grammar)}</pre></details>`;
  const wrap = el.querySelector('.ast-wrap');
  wrap.scrollLeft = (W - wrap.clientWidth) / 2;     // el árbol se abre centrado en la raíz
}

function renderSymbols(el, r) {
  const scopes = {};
  r.symbols.forEach((s) => { (scopes[s.scope] = scopes[s.scope] || []).push(s.name); });
  el.innerHTML = head('Tabla de símbolos y tipos',
    'El analizador semántico mantiene una pila de ámbitos: busca cada nombre del ámbito actual hacia el global, infiere el tipo de cada expresión y rechaza combinaciones incompatibles.',
    `<div class="chips">${Object.entries(scopes).map(([k, v]) => `<span class="chip">ámbito ${esc(k)} <b>${v.length}</b></span>`).join('')}</div>`) +
    (r.symbols.length ? `<div class="table-wrap"><table><thead><tr><th>Nombre</th><th>Tipo</th><th>Ámbito</th><th class="num">Línea</th><th class="num">Col.</th></tr></thead><tbody>${
      r.symbols.map((s) => `<tr><td class="mono">${esc(s.name)}</td><td><span class="kind">${esc(s.type)}</span></td><td>${esc(s.scope)}</td><td class="num">${s.line}</td><td class="num">${s.column ?? ''}</td></tr>`).join('')
    }</tbody></table></div>` : '<p class="empty">El programa no declara variables.</p>');
}

function quadCols(q) {
  const lit = (v) => (typeof v === 'string' ? JSON.stringify(v) : String(v));
  switch (q.op) {
    case 'CONST': return ['=', lit(q.a), '', q.dest];
    case 'MOV': return ['=', q.a, '', q.dest];
    case 'BIN': return [q.b[0], q.a, q.b[1], q.dest];
    case 'ALLOC': return ['alloc', q.a, '', q.dest];
    case 'RET': return ['return', q.a, '', ''];
    default: return [q.op.toLowerCase(), q.a ?? '', '', ''];
  }
}
function renderTac(el, r) {
  const temps = new Set(r.raw_quads.map((q) => q.dest).filter((d) => /^t\d+$/.test(d || '')));
  el.innerHTML = head('Código de tres direcciones',
    'El AST se aplana en una cinta lineal de instrucciones atómicas, guardadas como cuádruplas (operador, arg1, arg2, resultado). Los temporales suponen registros infinitos; reducirlos es tarea del back-end.',
    `<span class="chip">${temps.size} temporales</span>`) +
    `<div class="two"><div class="table-wrap"><table><thead><tr><th class="num">#</th><th>Operador</th><th>Arg 1</th><th>Arg 2</th><th>Resultado</th></tr></thead><tbody>${
      r.raw_quads.map((q, i) => { const c = quadCols(q); return `<tr><td class="num">${i}</td><td class="mono">${esc(c[0])}</td><td class="mono">${esc(c[1])}</td><td class="mono">${esc(c[2])}</td><td class="mono">${esc(c[3])}</td></tr>`; }).join('')
    }</tbody></table></div>
    <div><h3 style="margin-bottom:8px">Forma legible</h3><div class="listing">${r.tac.map((l) => `<div>${esc(l)}</div>`).join('')}</div></div></div>`;
}

function renderOpt(el, r) {
  const cats = [['simplificación algebraica', 'Algebraica'], ['propagación', 'Propagación'], ['plegado', 'Plegado'], ['muerto', 'Código muerto']];
  const counts = cats.map(([k, l]) => [l, r.optimizations.filter((n) => n.includes(k)).length]);
  const before = r.tac.length; const after = r.optimized_tac.length;
  const pct = before ? Math.round((1 - after / before) * 100) : 0;
  el.innerHTML = head('Optimización',
    'Tres pasadas locales que no cambian lo que el programa imprime: identidades algebraicas, propagación y plegado de constantes, y eliminación de temporales muertos.',
    `<div class="chips">${counts.map(([l, v]) => `<span class="chip">${l} <b>${v}</b></span>`).join('')}</div>`) +
    `<p class="small" style="margin:0">${before} → ${after} cuádruplas (${pct}% menos). ${$('#optimized').checked ? 'El back-end está usando la versión optimizada.' : 'El back-end está usando la versión original; activa <b>Optimizar</b> para que use esta.'}</p>
    <div class="two"><div><h3 style="margin-bottom:8px">Antes</h3><div class="listing">${r.tac.map((l) => `<div>${esc(l)}</div>`).join('')}</div></div>
    <div><h3 style="margin-bottom:8px">Después</h3><div class="listing">${r.optimized_tac.map((l) => `<div>${esc(l)}</div>`).join('')}</div></div></div>
    <div><h3 style="margin-bottom:8px">Qué se hizo y dónde</h3><div class="listing">${r.optimizations.length ? r.optimizations.map((l) => `<div>${esc(l)}</div>`).join('') : '<div class="c">No hubo nada que optimizar en este programa.</div>'}</div></div>`;
}

function asmLine(line, extraClass = '') {
  const [ins, comment] = line.split(/;(.*)/s);
  const [op, ...rest] = ins.trim().split(' ');
  const isSpill = /^(STORE|LOAD)$/.test(op);
  const isFrame = /^(ENTER|LEAVE|CALL|RET)$/.test(op);
  const cls = [isSpill ? 'spill' : '', isFrame ? 'frame' : '', extraClass].join(' ').trim();
  return `<div class="${cls}"><span class="op">${esc(op)}</span>${rest.length ? ' ' + esc(rest.join(' ')) : ''}${comment ? `<span class="c">  ;${esc(comment)}</span>` : ''}</div>`;
}
function renderAsm(el, r) {
  const slots = Object.entries(r.register_slots || {});
  el.innerHTML = head('Generación de código objetivo',
    `Cada cuádrupla se traduce a instrucciones de una ISA virtual con ${$('#registers').value} registros. Cuando no queda registro libre, el valor con menos usos futuros se expulsa a RAM (STORE) y se recarga después (LOAD).`,
    `<span class="badge spill">${r.spill_count} spill${r.spill_count === 1 ? '' : 's'}</span>`) +
    `<div class="two"><div class="listing">${r.assembly.map((l) => asmLine(l)).join('')}</div>
    <div><h3 style="margin-bottom:8px">Eventos del asignador de registros</h3>
    <div class="listing" style="max-height:300px">${r.register_events.length ? r.register_events.map((e) => `<div>${esc(e)}</div>`).join('') : '<div class="c">Sin spills: los registros alcanzaron.</div>'}</div>
    ${slots.length ? `<h3 style="margin:14px 0 8px">Direcciones de spill en RAM</h3><div class="table-wrap"><table><thead><tr><th>Valor</th><th>Dirección</th></tr></thead><tbody>${slots.map(([k, v]) => `<tr><td class="mono">${esc(k)}</td><td class="mono">${esc(v)}</td></tr>`).join('')}</tbody></table></div>` : ''}
    </div></div>`;
}

/* CPU paso a paso */
function renderCpu(el, r) {
  const trace = r.cpu_trace;
  el.innerHTML = head('CPU virtual',
    'La CPU ejecuta el ensamblador con el ciclo leer, decodificar y ejecutar. Avanza paso a paso para ver cómo cambian los registros, la RAM de spill, la pila de marcos y el heap.') +
    `<div class="cpu-controls">
      <button class="ghost" data-act="first" aria-label="Primer paso">Inicio</button>
      <button class="ghost" data-act="prev" aria-label="Paso anterior">◀ Anterior</button>
      <button class="ghost" data-act="next" aria-label="Paso siguiente">Siguiente ▶</button>
      <button class="ghost" data-act="play" id="play">Reproducir</button>
      <input type="range" id="step" min="0" max="${trace.length - 1}" value="${state.step}" aria-label="Paso de ejecución">
      <span class="small muted" id="step-label"></span>
    </div>
    <div class="cpu-now" id="cpu-now"></div>
    <div class="cpu-grid"><div class="listing" id="cpu-listing">${r.assembly.map((l) => asmLine(l)).join('')}</div>
    <div class="mem"><h4>Registros</h4><div class="regs" id="regs"></div>
    <h4>RAM de spill</h4><div id="ram"></div><h4>Pila de marcos (cima arriba)</h4><div class="frames" id="frames"></div><h4>Heap</h4><div id="heap"></div></div></div>`;
  el.querySelectorAll('[data-act]').forEach((b) => b.addEventListener('click', () => cpuAct(b.dataset.act)));
  $('#step').addEventListener('input', (e) => { stopPlay(); state.step = Number(e.target.value); paintStep(); });
  paintStep();
}
function cpuAct(act) {
  const n = state.result.cpu_trace.length;
  if (act === 'play') { if (state.timer) stopPlay(); else startPlay(); return; }
  stopPlay();
  if (act === 'first') state.step = 0;
  if (act === 'prev') state.step = Math.max(0, state.step - 1);
  if (act === 'next') state.step = Math.min(n - 1, state.step + 1);
  paintStep();
}
function startPlay() {
  const n = state.result.cpu_trace.length;
  if (state.step >= n - 1) state.step = 0;
  $('#play').textContent = 'Pausa';
  state.timer = setInterval(() => {
    if (state.step >= n - 1) { stopPlay(); return; }
    state.step += 1; paintStep();
  }, 500);
}
function stopPlay() {
  clearInterval(state.timer); state.timer = null;
  const p = $('#play'); if (p) p.textContent = 'Reproducir';
}
function paintStep() {
  const trace = state.result.cpu_trace;
  const i = state.step; const s = trace[i]; const prev = trace[i - 1];
  $('#step').value = i;
  $('#step-label').textContent = `Paso ${i + 1} de ${trace.length}`;
  $('#cpu-now').innerHTML = `PC ${s.pc}: <b>${esc(s.instruction)}</b>`;
  const rows = $('#cpu-listing').children;
  [...rows].forEach((row, k) => row.classList.toggle('current', k === s.pc));
  const cur = rows[s.pc];
  if (cur) { const L = $('#cpu-listing'); const top = cur.offsetTop - L.offsetTop; if (top < L.scrollTop || top > L.scrollTop + L.clientHeight - 40) L.scrollTop = top - L.clientHeight / 2; }
  $('#regs').innerHTML = Object.entries(s.registers).map(([k, v]) => {
    const hot = prev && JSON.stringify(prev.registers[k]) !== JSON.stringify(v);
    return `<div class="reg ${hot ? 'hot' : ''}"><div class="rn">${k}</div><div class="rv" title="${esc(v)}">${v === null ? '·' : esc(fmtVal(v))}</div></div>`;
  }).join('');
  const ram = Object.entries(s.ram);
  $('#ram').innerHTML = ram.length ? `<div class="table-wrap"><table><tbody>${ram.map(([k, v]) => {
    const hot = prev && JSON.stringify(prev.ram[k]) !== JSON.stringify(v);
    return `<tr${hot ? ' style="background:var(--ok-soft)"' : ''}><td class="mono">${esc(k)}</td><td class="mono">${esc(fmtVal(v))}</td></tr>`;
  }).join('')}</tbody></table></div>` : '<span class="small muted">vacía</span>';
  $('#frames').innerHTML = s.stack.length ? s.stack.map((f) => `<div class="frame-box">${esc(f)}</div>`).join('') : '<span class="small muted">vacía</span>';
  const heap = Object.entries(s.heap);
  $('#heap').innerHTML = heap.length ? heap.map(([k, v]) => `<span class="chip">${esc(k)}: ${esc(v)} bytes</span>`).join(' ') : '<span class="small muted">sin reservas</span>';
}
document.addEventListener('keydown', (e) => {
  if (views.pipeline.hidden || state.stage !== 'cpu' || !state.result?.cpu_trace || e.target === code || e.target.tagName === 'INPUT') return;
  if (e.key === 'ArrowRight') cpuAct('next');
  if (e.key === 'ArrowLeft') cpuAct('prev');
});

function fmtVal(v) {
  if (typeof v === 'number' && !Number.isInteger(v)) return String(Math.round(v * 1e6) / 1e6);
  if (typeof v === 'string') return JSON.stringify(v);
  return String(v);
}
function fmtMs(ms) { return ms < 1 ? `${(ms * 1000).toFixed(0)} µs` : `${ms.toFixed(ms < 10 ? 2 : 1)} ms`; }

/* ════════════════ RENDIMIENTO ════════════════ */
const PHASE_NAMES = { lexico: 'Léxico', sintactico: 'Sintaxis', semantico: 'Semántica', ir: 'TAC (IR)', optimizacion: 'Optimización', backend: 'Back-end', interprete: 'Intérprete TAC', cpu: 'CPU virtual' };
const charts = [];   // { el, draw } para redibujar al cambiar el tamaño

$('#bench-run').addEventListener('click', runBench);
async function runBench() {
  const btn = $('#bench-run');
  btn.disabled = true; btn.textContent = 'Midiendo…';
  try {
    const b = await api('/api/benchmark', { example: $('#bench-example').value, repeats: Number($('#bench-repeats').value) || 15 });
    renderBench(b);
  } catch (err) {
    $('#bench-out').innerHTML = `<div class="error-box">No se pudo medir: ${esc(err.message)}</div>`;
  } finally {
    btn.disabled = false; btn.textContent = 'Medir rendimiento';
  }
}

function renderBench(b) {
  const phases = Object.entries(b.phases).map(([k, v]) => ({ label: PHASE_NAMES[k] || k, value: v }));
  const slowest = phases.reduce((a, c) => (c.value > a.value ? c : a), phases[0]);
  const r3 = b.registers.find((x) => x.registers === 3);
  const size = b.sizes.find((s) => s.example === b.example);
  const red = size && size.asm ? Math.round((1 - size.asm_opt / size.asm) * 100) : 0;
  const sc = b.scaling;
  const s100 = sc.find((x) => x.n === 100); const s200 = sc.find((x) => x.n === 200);
  const ratio = s100 && s200 && s100.backend ? s200.backend / s100.backend : null;

  $('#bench-out').innerHTML = `
    <div class="kpis">
      <div class="sheet kpi"><div class="v">${fmtMs(b.total_ms)}</div><div class="l">Pipeline completo de «${esc(b.example)}» (mediana de ${b.repeats} corridas)</div></div>
      <div class="sheet kpi"><div class="v">${esc(slowest.label)}</div><div class="l">Fase más costosa: ${Math.round((slowest.value / b.total_ms) * 100)}% del tiempo</div></div>
      <div class="sheet kpi"><div class="v">${r3.sin_optimizar}<small>→ ${r3.optimizado}</small></div><div class="l">Spills con 3 registros, sin y con optimización</div></div>
      <div class="sheet kpi"><div class="v">${red}<small>%</small></div><div class="l">Menos instrucciones de ensamblador al optimizar (${size ? `${size.asm} → ${size.asm_opt}` : 'n/d'})</div></div>
    </div>
    <div class="charts">
      ${chartCard('c-phases', 'Tiempo por fase', `Mediana en milisegundos para «${esc(b.example)}».`)}
      ${chartCard('c-regs', 'Spills según registros disponibles', 'Con más registros hay menos presión y menos viajes a RAM. La optimización reduce temporales y elimina la presión.', [['Sin optimizar', 'var(--series-1)'], ['Optimizado', 'var(--series-2)']])}
      ${chartCard('c-sizes', 'Instrucciones de ensamblador por programa', 'Tamaño del código objetivo generado para cada ejemplo.', [['Sin optimizar', 'var(--series-1)'], ['Optimizado', 'var(--series-2)']])}
      ${chartCard('c-scale', 'Escalabilidad del compilador', ratio ? `Al pasar de 100 a 200 variables, el back-end tarda ${ratio.toFixed(1)} veces más: crecimiento cuadrático, porque para cada instrucción el asignador cuenta los usos futuros recorriendo el resto del programa.` : 'Tiempo frente al tamaño del programa.', [['Pipeline completo', 'var(--series-1)'], ['Solo back-end', 'var(--series-2)']])}
    </div>`;

  charts.length = 0;
  addChart('c-phases', (el) => hbarChart(el, phases, fmtMs),
    ['Fase', 'Mediana'], phases.map((p) => [p.label, fmtMs(p.value)]));
  addChart('c-regs', (el) => lineChart(el, b.registers.map((x) => x.registers), [
    { name: 'Sin optimizar', color: 'var(--series-1)', values: b.registers.map((x) => x.sin_optimizar) },
    { name: 'Optimizado', color: 'var(--series-2)', values: b.registers.map((x) => x.optimizado) },
  ], { xLabel: 'registros', fmt: (v) => `${v} spill${v === 1 ? '' : 's'}`, integer: true }),
  ['Registros', 'Sin optimizar', 'Optimizado'], b.registers.map((x) => [x.registers, x.sin_optimizar, x.optimizado]));
  addChart('c-sizes', (el) => groupedBars(el, b.sizes.map((s) => s.example), [
    { name: 'Sin optimizar', color: 'var(--series-1)', values: b.sizes.map((s) => s.asm) },
    { name: 'Optimizado', color: 'var(--series-2)', values: b.sizes.map((s) => s.asm_opt) },
  ], (v) => `${v} instrucciones`),
  ['Programa', 'Sin optimizar', 'Optimizado'], b.sizes.map((s) => [s.example, s.asm, s.asm_opt]));
  addChart('c-scale', (el) => lineChart(el, sc.map((x) => x.n), [
    { name: 'Pipeline completo', color: 'var(--series-1)', values: sc.map((x) => x.total) },
    { name: 'Solo back-end', color: 'var(--series-2)', values: sc.map((x) => x.backend) },
  ], { xLabel: 'variables en el programa', fmt: fmtMs, tick: (v) => `${fmtTick(v)} ms` }),
  ['Variables', 'Cuádruplas', 'Pipeline', 'Back-end'], sc.map((x) => [x.n, x.quads, fmtMs(x.total), fmtMs(x.backend)]));
}

function chartCard(id, title, note, legend) {
  return `<div class="sheet chart-card"><header><h3>${title}</h3><button class="ghost small" data-table="${id}">Ver tabla</button></header>
    <p class="note">${note}</p>
    ${legend ? `<div class="legend">${legend.map(([n, c]) => `<span style="--c:${c}">${n}</span>`).join('')}</div>` : ''}
    <div class="chart" id="${id}"></div></div>`;
}
function addChart(id, draw, header, rows) {
  const el = $(`#${id}`);
  const entry = { el, draw, header, rows, table: false };
  charts.push(entry);
  $(`[data-table="${id}"]`).addEventListener('click', (e) => {
    entry.table = !entry.table;
    e.target.textContent = entry.table ? 'Ver gráfica' : 'Ver tabla';
    paintChart(entry);
  });
  paintChart(entry);
}
function paintChart(c) {
  if (c.table) {
    c.el.innerHTML = `<div class="table-wrap"><table><thead><tr>${c.header.map((h) => `<th>${esc(h)}</th>`).join('')}</tr></thead><tbody>${
      c.rows.map((r) => `<tr>${r.map((v) => `<td>${esc(v)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
  } else {
    c.el.innerHTML = '';
    c.draw(c.el);
  }
}
function redrawCharts() { charts.forEach(paintChart); }
let resizeTimer;
window.addEventListener('resize', () => { clearTimeout(resizeTimer); resizeTimer = setTimeout(() => { if (!views.bench.hidden) redrawCharts(); if (state.stage === 'sintactico') renderDetail(); }, 150); });

/* ── primitivas de gráfica ── */
function niceMax(v) {
  if (v <= 0) return 1;
  const p = 10 ** Math.floor(Math.log10(v));
  const f = v / p;
  return (f <= 1 ? 1 : f <= 2 ? 2 : f <= 2.5 ? 2.5 : f <= 5 ? 5 : 10) * p;
}
function svgEl(w, h) {
  const s = document.createElementNS(SVGNS, 'svg');
  s.setAttribute('width', w); s.setAttribute('height', h); s.setAttribute('viewBox', `0 0 ${w} ${h}`);
  return s;
}
function tooltip(el) {
  const t = document.createElement('div'); t.className = 'tip'; el.appendChild(t);
  return {
    show(x, y, html) { t.innerHTML = html; t.style.left = `${x}px`; t.style.top = `${y}px`; t.classList.add('on'); },
    hide() { t.classList.remove('on'); },
  };
}
const fmtTick = (v) => (v >= 100 ? Math.round(v) : Math.round(v * 100) / 100);

function hbarChart(el, items, fmt) {
  const W = el.clientWidth || 500; const rowH = 28; const left = 116; const right = 70;
  const H = items.length * rowH + 28;
  const max = niceMax(Math.max(...items.map((i) => i.value)));
  const x = (v) => left + (v / max) * (W - left - right);
  const s = svgEl(W, H); const tip = tooltip(el);
  let g = '<g class="grid">';
  for (let k = 0; k <= 4; k++) { const v = (max / 4) * k; g += `<line x1="${x(v)}" x2="${x(v)}" y1="0" y2="${H - 22}"/><text class="lbl" x="${x(v)}" y="${H - 6}" text-anchor="middle">${k ? esc(fmt(v)) : 0}</text>`; }
  g += '</g>';
  let bars = '';
  items.forEach((it, i) => {
    const y = i * rowH + 5; const h = rowH - 10; const x1 = x(it.value); const r = Math.min(4, (x1 - left) / 2, h / 2);
    bars += `<text class="lbl" x="${left - 10}" y="${y + h / 2 + 4}" text-anchor="end">${esc(it.label)}</text>
      <path d="M${left} ${y}H${x1 - r}Q${x1} ${y} ${x1} ${y + r}V${y + h - r}Q${x1} ${y + h} ${x1 - r} ${y + h}H${left}Z" fill="var(--series-1)"/>
      <text class="val" x="${x1 + 6}" y="${y + h / 2 + 4}">${esc(fmt(it.value))}</text>
      <rect data-i="${i}" x="0" y="${i * rowH}" width="${W}" height="${rowH}" fill="transparent"/>`;
  });
  s.innerHTML = `${g}<line class="baseline" x1="${left}" x2="${left}" y1="0" y2="${H - 22}"/>${bars}`;
  s.addEventListener('mousemove', (e) => {
    const i = e.target.dataset?.i; if (i === undefined) { tip.hide(); return; }
    const it = items[i]; tip.show(x(it.value), Number(i) * rowH + 4, `<b>${esc(it.label)}</b>: ${esc(fmt(it.value))}`);
  });
  s.addEventListener('mouseleave', tip.hide);
  el.prepend(s);
}

function lineChart(el, xs, series, opt) {
  const W = el.clientWidth || 500; const H = 250; const m = { l: 58, r: 112, t: 14, b: 40 };
  const all = series.flatMap((s) => s.values);
  const max = opt.integer ? Math.max(4, Math.ceil(Math.max(...all) / 4) * 4) : niceMax(Math.max(...all));
  const tickFmt = opt.tick || ((v) => fmtTick(v));
  const xMin = Math.min(...xs); const xMax = Math.max(...xs);
  const x = (v) => m.l + ((v - xMin) / (xMax - xMin || 1)) * (W - m.l - m.r);
  const y = (v) => H - m.b - (v / max) * (H - m.t - m.b);
  const s = svgEl(W, H); const tip = tooltip(el);
  let g = '<g class="grid">';
  for (let k = 0; k <= 4; k++) { const v = (max / 4) * k; g += `<line x1="${m.l}" x2="${W - m.r}" y1="${y(v)}" y2="${y(v)}"/><text class="lbl" x="${m.l - 8}" y="${y(v) + 4}" text-anchor="end">${k ? esc(tickFmt(v)) : 0}</text>`; }
  g += '</g>';
  // Etiquetas directas al final de cada línea; si chocan, se separan verticalmente.
  const ends = series.map((sr) => ({ name: sr.name, y: y(sr.values[sr.values.length - 1]) })).sort((a, b) => a.y - b.y);
  for (let i = 1; i < ends.length; i++) if (ends[i].y - ends[i - 1].y < 15) ends[i].y = ends[i - 1].y + 15;
  const endLabels = ends.map((e) => `<text class="lbl" x="${W - m.r + 10}" y="${e.y + 4}">${esc(e.name)}</text>`).join('');
  const ticks = xs.map((v) => `<text class="lbl" x="${x(v)}" y="${H - m.b + 18}" text-anchor="middle">${v}</text>`).join('');
  const paths = series.map((sr) => `<path d="${sr.values.map((v, i) => `${i ? 'L' : 'M'}${x(xs[i])} ${y(v)}`).join('')}" fill="none" stroke="${sr.color}" stroke-width="2" stroke-linejoin="round"/>
    ${sr.values.map((v, i) => `<circle cx="${x(xs[i])}" cy="${y(v)}" r="4" fill="${sr.color}" stroke="var(--sheet)" stroke-width="2"/>`).join('')}`).join('');
  s.innerHTML = `${g}<line class="baseline" x1="${m.l}" x2="${W - m.r}" y1="${y(0)}" y2="${y(0)}"/>${ticks}
    <text class="lbl" x="${(m.l + W - m.r) / 2}" y="${H - 4}" text-anchor="middle">${esc(opt.xLabel)}</text>
    <line id="xh" x1="0" x2="0" y1="${m.t}" y2="${H - m.b}" stroke="var(--ink-3)" stroke-dasharray="3 3" opacity="0"/>${paths}${endLabels}
    <rect x="${m.l}" y="0" width="${W - m.l - m.r}" height="${H - m.b}" fill="transparent" class="hit"/>`;
  const xh = s.querySelector('#xh');
  s.addEventListener('mousemove', (e) => {
    const rect = s.getBoundingClientRect(); const px = e.clientX - rect.left;
    let best = 0; xs.forEach((v, i) => { if (Math.abs(x(v) - px) < Math.abs(x(xs[best]) - px)) best = i; });
    const cx = x(xs[best]);
    xh.setAttribute('x1', cx); xh.setAttribute('x2', cx); xh.setAttribute('opacity', '1');
    tip.show(cx, m.t + 10, `<b>${xs[best]} ${esc(opt.xLabel)}</b><br>${series.map((sr) => `${esc(sr.name)}: ${esc(opt.fmt(sr.values[best]))}`).join('<br>')}`);
  });
  s.addEventListener('mouseleave', () => { tip.hide(); xh.setAttribute('opacity', '0'); });
  el.prepend(s);
}

function groupedBars(el, cats, series, fmt) {
  const W = el.clientWidth || 500; const H = 250; const m = { l: 40, r: 10, t: 14, b: 44 };
  const max = Math.max(4, Math.ceil(Math.max(...series.flatMap((s) => s.values)) / 20) * 20);   // conteos: ticks enteros
  const band = (W - m.l - m.r) / cats.length; const gap = 2;
  const bw = Math.min(28, (band * 0.7 - gap) / series.length);
  const y = (v) => H - m.b - (v / max) * (H - m.t - m.b);
  const s = svgEl(W, H); const tip = tooltip(el);
  let g = '<g class="grid">';
  for (let k = 0; k <= 4; k++) { const v = (max / 4) * k; g += `<line x1="${m.l}" x2="${W - m.r}" y1="${y(v)}" y2="${y(v)}"/><text class="lbl" x="${m.l - 8}" y="${y(v) + 4}" text-anchor="end">${fmtTick(v)}</text>`; }
  g += '</g>';
  let bars = '';
  cats.forEach((c, ci) => {
    const gx = m.l + ci * band + (band - (bw * series.length + gap * (series.length - 1))) / 2;
    series.forEach((sr, si) => {
      const v = sr.values[ci]; const bx = gx + si * (bw + gap); const y0 = y(0); const y1 = y(v); const r = Math.min(4, bw / 2, (y0 - y1) / 2);
      bars += `<path d="M${bx} ${y0}V${y1 + r}Q${bx} ${y1} ${bx + r} ${y1}H${bx + bw - r}Q${bx + bw} ${y1} ${bx + bw} ${y1 + r}V${y0}Z" fill="${sr.color}"/>`;
    });
    bars += `<text class="lbl" x="${m.l + ci * band + band / 2}" y="${H - m.b + 16}" text-anchor="middle">${esc(c.length > 12 ? c.slice(0, 11) + '…' : c)}</text>
      <rect data-i="${ci}" x="${m.l + ci * band}" y="0" width="${band}" height="${H - m.b + 20}" fill="transparent"/>`;
  });
  s.innerHTML = `${g}<line class="baseline" x1="${m.l}" x2="${W - m.r}" y1="${y(0)}" y2="${y(0)}"/>${bars}`;
  s.addEventListener('mousemove', (e) => {
    const i = e.target.dataset?.i; if (i === undefined) { tip.hide(); return; }
    const top = Math.min(...series.map((sr) => y(sr.values[i])));
    tip.show(m.l + i * band + band / 2, top, `<b>${esc(cats[i])}</b><br>${series.map((sr) => `${esc(sr.name)}: ${esc(fmt(sr.values[i]))}`).join('<br>')}`);
  });
  s.addEventListener('mouseleave', tip.hide);
  el.prepend(s);
}

/* ════════════════ ARQUITECTURA ════════════════ */
let sysCache = null;
async function getSystem() { if (!sysCache) sysCache = await api('/api/system'); return sysCache; }

async function renderArch() {
  const out = $('#arch-out');
  if (out.dataset.done) return;
  const sys = await getSystem();
  const maxLines = Math.max(...sys.modules.map((m) => m.lines));
  const mod = (name, desc, cls = '') => `<div class="mod ${cls}"><b>${name}</b><span>${desc}</span></div>`;
  const col = (title, body) => `<div class="col"><h3>${title}</h3><div class="stack">${body}</div></div>`;
  const role = {
    'compiler.py': 'Lexer, parser, semántica, TAC, optimizador, back-end e intérprete',
    'automata.py': 'AFD por tabla de transición y gramática EBNF',
    'virtual_cpu.py': 'CPU virtual: leer, decodificar, ejecutar',
    'native_backend.py': 'Traducción a C11 y llamada a GCC/Clang',
    'gui.py': 'Interfaz de escritorio Tkinter',
    'main.py': 'Interfaz de consola',
    'dashboard.py': 'Servidor de este panel',
    'coverage.py': 'Matriz teoría ↔ código',
  };
  out.innerHTML = `
    <div class="sheet">
      <div class="detail-head" style="margin-bottom:14px"><div><h2>Arquitectura por fases</h2>
      <p>Tres interfaces de usuario comparten un único orquestador. El compilador no sabe quién lo llama: la misma función produce lo que ves en la consola, en Tkinter y en este panel.</p></div></div>
      <div class="arch">
        ${col('Interfaces', mod('dashboard.py', 'panel web local') + mod('gui.py', 'escritorio, Tkinter') + mod('main.py', 'consola'))}
        <div class="arrow"></div>
        ${col('Orquestador', mod('compile_source()', 'encadena las fases y mide su tiempo', 'core'))}
        <div class="arrow"></div>
        ${col('Front-end', mod('lex()', 'tokens, semana 2') + mod('Parser', 'AST, semanas 3 y 4') + mod('Semantic', 'ámbitos y tipos, 5 y 6'))}
        <div class="arrow"></div>
        ${col('Middle-end', mod('IRBuilder', 'cuádruplas TAC, semana 7') + mod('optimize()', '3 pasadas, semana 9'))}
        <div class="arrow"></div>
        ${col('Back-end', mod('Backend', 'registros y spill, semana 10') + mod('VirtualCPU', 'ejecuta el ensamblador') + mod('native_backend', 'C11 + GCC, opcional', 'alt'))}
      </div>
    </div>
    <div class="arch-grid">
      <div class="sheet"><h3 style="margin-bottom:10px">Módulos y tamaño</h3>
        <div class="table-wrap" style="max-height:none"><table><thead><tr><th>Archivo</th><th>Responsabilidad</th><th>Líneas de código</th></tr></thead><tbody>${
          sys.modules.map((m) => `<tr><td class="mono">${m.file}</td><td style="white-space:normal">${esc(role[m.file] || '')}</td><td><div class="bar-cell"><i style="width:${Math.round((m.lines / maxLines) * 120)}px"></i>${m.lines}</div></td></tr>`).join('')
        }</tbody></table></div>
        <p class="small muted" style="margin:8px 0 0">Líneas sin contar vacías ni comentarios de línea completa. Más ${sys.test_count} pruebas automáticas y ${sys.examples} programas de ejemplo.</p>
      </div>
      <div class="sheet"><h3 style="margin-bottom:12px">Tecnologías</h3><div class="tech">
        <div class="tech-item"><b>Python ${esc(sys.python)}</b><p>Todo el compilador, solo con la biblioteca estándar: <code>re</code> para el lexer, <code>dataclasses</code> para Token, Node y Quad, <code>collections.Counter</code> para contar usos futuros, <code>ast.literal_eval</code> en la CPU y <code>http.server</code> para este panel.</p></div>
        <div class="tech-item"><b>unittest</b><p>${sys.test_count} pruebas: cada fase, cada tipo de error y la concordancia entre el intérprete TAC y la CPU virtual.</p></div>
        <div class="tech-item"><b>C11 con GCC o Clang</b><p>Destino opcional para producir un ejecutable real. ${sys.c_compiler ? `Detectado en <code>${esc(sys.c_compiler)}</code>.` : 'No está instalado en este equipo; la ruta nativa se desactiva sola y el resto funciona igual.'}</p></div>
        <div class="tech-item"><b>Tkinter</b><p>Interfaz de escritorio original (<code>gui.py</code>).</p></div>
        <div class="tech-item"><b>HTML, CSS y JavaScript</b><p>Este panel, sin librerías y sin internet: el árbol AST y las gráficas se dibujan a mano en SVG.</p></div>
        <div class="tech-item"><b>Sistema</b><p>${esc(sys.platform)}</p></div>
      </div></div>
    </div>
    <div class="decisions">${[
      ['Regex maestra en el lexer', 'Una sola pasada con grupos con nombre; el orden de las alternativas es la tabla de prioridades.', 'Descartado: un AFD escrito a mano para todo el lenguaje. Se conserva como demostración en automata.py.'],
      ['Descenso recursivo', 'Una función por regla de la gramática; la precedencia sale de la profundidad de las llamadas y no hace falta una tabla.', 'Descartado: LR/LALR con tablas (Yacc, Bison). Más potente, pero ilegible sin un generador.'],
      ['TAC en cuádruplas', 'Independiente de la máquina. Como cada temporal se asigna una sola vez, el optimizador puede razonar localmente.', 'Descartado: tripletas, que no tienen campo de resultado y son más difíciles de reordenar.'],
      ['Asignación local de registros', 'A demanda, con víctima de spill según los usos futuros. Es correcta mientras el lenguaje no tenga saltos.', 'Costo: crecimiento cuadrático (ver Rendimiento). Alternativa: coloreado de grafos de Chaitin-Briggs.'],
      ['Validación cruzada', 'El TAC se ejecuta en un intérprete y el ensamblador en la CPU virtual; si las salidas difieren, la compilación falla.', 'Así un error del back-end nunca pasa desapercibido.'],
      ['C11 como segundo destino', 'GCC hace la selección de instrucciones y la asignación de registros reales para x86 o ARM.', 'Descartado: emitir x86 directamente, fuera del alcance del curso.'],
    ].map(([t, w, a]) => `<div class="sheet decision"><h3>${t}</h3><p>${w}</p><p class="alt">${a}</p></div>`).join('')}</div>`;
  out.dataset.done = '1';
}

/* ════════════════ arranque ════════════════ */
(async function init() {
  renderCinta();
  renderDetail();
  try {
    const sys = await getSystem();
    $('#sysinfo').innerHTML = `<span>Python ${esc(sys.python)}</span><span>${sys.c_compiler ? 'GCC/Clang disponible' : 'Sin compilador C'}</span><span>${sys.test_count} pruebas</span>`;
    await loadExamples();
    await compile();
  } catch (err) {
    $('#detail').innerHTML = `<div class="error-box">No se pudo iniciar el panel: ${esc(err.message)}. Ábrelo con <code>python dashboard.py</code>.</div>`;
  }
})();
