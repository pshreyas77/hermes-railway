# Shreyas's Second Brain — Professional Knowledge Graph
# ===========================-===========================
# D3.js force-directed graph with dark theme, domain coloring,
# hub glow, tooltips, zoom/pan, and search.
# Output: obsidian_graph.html (open in any browser)
#
# Run: python professional_graph.py
# Or:   "C:/Users/shrey/AppData/Local/Programs/Python/Python314/python.exe" professional_graph.py

import re, json
from pathlib import Path
import networkx as nx
from collections import Counter

VAULT   = Path("E:/_Knowledge/ObsidianVault")
OUT     = VAULT / "obsidian_graph.html"
MAX_NODES = 600   # cap for smooth physics

DOMAIN_PALETTE = {
    "Indian Political History":  "#e74c3c",
    "Dravidian Politics / Tamil Nadu": "#c0392b",
    "Aryan Migration / IVC / DNA": "#9b59b6",
    "RSS / Hindutva / Sangh Parivar": "#e67e22",
    "Philosophy & Religion": "#8e44ad",
    "Buddhism / Shramana": "#d35400",
    "Anti-Caste / Ambedkar / Phule": "#95a5a6",
    "AI & Technology / PKM": "#3498db",
    "Health & Fitness": "#27ae60",
    "Agentic Systems": "#f39c12",
    "Maps / MOCs": "#5f27cd",
    "Daily Notes / Logs": "#54a0ff",
    "Sources / Literature": "#feca57",
    "Output / Analyses": "#00cec9",
    "Projects / PARA": "#ff6b81",
    "System / Infrastructure": "#1dd1a1",
    "Second Brain / LLM Wiki": "#00b4d8",
    "tag": "#ffffff",
    "default": "#636e72",
}

def classify_node(name: str) -> str:
    n = name.lower()
    if n.startswith("#"):
        return "tag"
    # Add your own domain classification rules here
    if any(k in n for k in ["moc","map of content","maps","index"]):
        return "Maps / MOCs"
    if any(k in n for k in ["aryan","indus valley","ivc","steppe","rakhigarhi"]):
        return "Aryan Migration / IVC / DNA"
    if any(k in n for k in ["buddhism","buddha","buddhist","dhamma","sangha"]):
        return "Buddhism / Shramana"
    if any(k in n for k in ["anti-caste","ambedkar","dalit","phule","jyotirao"]):
        return "Anti-Caste / Ambedkar / Phule"
    if any(k in n for k in ["rss","hindutva","sangh","hindu"]):
        return "RSS / Hindutva / Sangh Parivar"
    if any(k in n for k in ["ai","llm","claude","obsidian","second brain","zettel","pkm","wiki"]):
        return "AI & Technology / PKM"
    if any(k in n for k in ["health","fitness","supplement","workout","gym"]):
        return "Health & Fitness"
    if any(k in n for k in ["agentic","autonomous agent","genericagent","night shift"]):
        return "Agentic Systems"
    if any(k in n for k in ["04 - daily","daily note","night-shift-log"]):
        return "Daily Notes / Logs"
    if any(k in n for k in ["01 - literature","literature","articles","research"]):
        return "Sources / Literature"
    if any(k in n for k in ["06 - outputs","outputs","analysis","synthesis"]):
        return "Output / Analyses"
    if any(k in n for k in ["03 - projects","project","cross-domain"]):
        return "Projects / PARA"
    if any(k in n for k in ["07 - system","system","vault-health","ai-first"]):
        return "System / Infrastructure"
    return "default"

def get_links(text):
    return re.findall(r'\[\[(.*?)\]\]', text)

def get_tags(text):
    return re.findall(r'(?<!\\w)#([\w/-]+)', text)

EXCLUDE = {'.obsidian', '.smart-env', '.git', 'node_modules', '_trash', '.graphify', 'trash', '.trash'}

G = nx.Graph()
nodes_meta = {}

for md in VAULT.glob("**/*.md"):
    name = str(md.relative_to(VAULT)).replace(".md", "")
    if any(e in name for e in EXCLUDE):
        continue
    try:
        text = md.read_text(encoding="utf-8", errors="ignore")
        domain = classify_node(name)
        nodes_meta[name] = {"domain": domain, "links": [], "tags": []}
        G.add_node(name)
        for tag in get_tags(text):
            tn = f"#{tag}"
            if tn not in nodes_meta:
                G.add_node(tn)
                nodes_meta[tn] = {"domain": "tag", "links": [], "tags": []}
            G.add_edge(name, tn)
            nodes_meta[name]["tags"].append(tag)
        for link in get_links(text):
            target = link.split("|")[0].split("#")[0].strip()
            if target:
                G.add_edge(name, target)
                nodes_meta[name]["links"].append(target)
    except Exception:
        pass

deg = dict(G.degree())
all_nodes = sorted(G.nodes(), key=lambda n: deg.get(n, 0), reverse=True)
if len(all_nodes) > MAX_NODES:
    keep = set(all_nodes[:MAX_NODES])
    for n in list(G.nodes()):
        if n not in keep:
            G.remove_node(n)

for n in G.nodes():
    nodes_meta.setdefault(n, {"domain": classify_node(n), "links": [], "tags": []})
    nodes_meta[n]["degree"] = deg.get(n, 0)

try:
    import community as community_louvain
    communities = community_louvain.best_partition(G.to_undirected())
    modularity  = community_louvain.modularity(communities, G.to_undirected())
except Exception:
    communities = {n: i % 10 for i, n in enumerate(G.nodes())}
    modularity = 0

for n, cid in communities.items():
    nodes_meta.setdefault(n, {"domain": "default", "links": [], "tags": []})
    nodes_meta[n]["community"] = cid

node_list, edge_list = [], []
for n in G.nodes():
    m = nodes_meta.get(n, {})
    domain = m.get("domain", "default")
    color   = DOMAIN_PALETTE.get(domain, DOMAIN_PALETTE["default"])
    deg_val = m.get("degree", 1)
    is_tag  = n.startswith("#")
    size    = 4 if is_tag else max(5, min(35, 5 + deg_val * 1.5))
    label   = n.split("/")[-1][:70]
    node_list.append({
        "id": n, "label": label, "domain": domain, "color": color,
        "size": size, "degree": deg_val, "community": m.get("community", 0),
        "links": m.get("links", [])[:10], "tags": m.get("tags", [])[:8],
    })

for u, v in G.edges():
    edge_list.append({"source": u, "target": v, "weight": 1})

graph_data = {"nodes": node_list, "links": edge_list}

# ── HTML TEMPLATE (D3.js dark-theme knowledge graph) ──────────────────────────
html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Shreyas's Second Brain — Knowledge Graph</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
  body { background: #080b14; font-family: 'Inter', sans-serif; color: #e2e8f0; overflow: hidden; height: 100vh; }

  #header { position: fixed; top: 0; left: 0; right: 0; height: 52px; background: rgba(8,11,20,0.92);
    border-bottom: 1px solid rgba(255,255,255,0.06); display: flex; align-items: center;
    padding: 0 20px; z-index: 100; backdrop-filter: blur(12px); }
  #header h1 { font-size: 14px; font-weight: 700; color: #e2e8f0; letter-spacing: 0.04em; flex: 1; }
  #header h1 span { color: #00cec9; }
  #stats { font-size: 11px; color: #64748b; margin-right: 20px; }
  #controls { display: flex; gap: 10px; align-items: center; }
  #search { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
    border-radius: 6px; color: #e2e8f0; padding: 5px 12px; font-size: 12px;
    font-family: 'Inter', sans-serif; width: 200px; outline: none; transition: border 0.2s; }
  #search:focus { border-color: #00cec9; }
  #search::placeholder { color: #475569; }
  .btn { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);
    border-radius: 6px; color: #94a3b8; font-size: 11px; font-family: 'Inter', sans-serif;
    padding: 5px 12px; cursor: pointer; transition: all 0.15s; }
  .btn:hover { background: rgba(255,255,255,0.1); color: #e2e8f0; }

  #graph { position: fixed; top: 52px; left: 0; right: 0; bottom: 0; }

  #legend { position: fixed; bottom: 24px; left: 24px; background: rgba(8,11,20,0.88);
    border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 16px 20px;
    z-index: 100; backdrop-filter: blur(16px); min-width: 220px; }
  #legend h3 { font-size: 10px; font-weight: 700; color: #475569; letter-spacing: 0.1em;
    text-transform: uppercase; margin-bottom: 12px; }
  .legend-item { display: flex; align-items: center; gap: 8px; margin-bottom: 6px;
    font-size: 11px; color: #94a3b8; cursor: pointer; border-radius: 4px;
    padding: 2px 4px; transition: background 0.15s; }
  .legend-item:hover { background: rgba(255,255,255,0.05); }
  .legend-item.inactive { opacity: 0.35; }
  .legend-dot { width: 9px; height: 9px; border-radius: 50%; flex-shrink: 0;
    box-shadow: 0 0 6px currentColor; }

  #tooltip { position: fixed; display: none; background: rgba(15,18,30,0.96);
    border: 1px solid rgba(255,255,255,0.12); border-radius: 10px; padding: 14px 18px;
    z-index: 200; max-width: 320px; backdrop-filter: blur(20px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.5); pointer-events: none; }
  #tooltip h4 { font-size: 13px; font-weight: 600; color: #f1f5f9; margin-bottom: 6px; line-height: 1.3; }
  #tooltip .domain-badge { display: inline-block; font-size: 9px; font-weight: 700;
    letter-spacing: 0.06em; text-transform: uppercase; padding: 2px 8px;
    border-radius: 20px; margin-bottom: 10px; }
  #tooltip .meta { font-size: 11px; color: #64748b; line-height: 1.7; }
  #tooltip .meta strong { color: #94a3b8; }
  #tooltip .links-row, #tooltip .tags-row { margin-top: 6px; font-size: 10px;
    color: #64748b; word-break: break-all; }
  #tooltip .links-row span, #tooltip .tags-row span { background: rgba(255,255,255,0.06);
    border-radius: 4px; padding: 1px 5px; margin: 1px; display: inline-block; color: #94a3b8; }

  #zoom-hint { position: fixed; bottom: 24px; right: 24px; font-size: 10px; color: #334155; z-index: 100; }

  #loading { position: fixed; inset: 0; display: flex; flex-direction: column;
    align-items: center; justify-content: center; background: #080b14; z-index: 999;
    transition: opacity 0.5s; }
  #loading.fade { opacity: 0; pointer-events: none; }
  .loading-title { font-size: 18px; font-weight: 700; color: #e2e8f0; margin-bottom: 8px; }
  .loading-title span { color: #00cec9; }
  .loading-sub { font-size: 12px; color: #475569; margin-bottom: 24px; }
  .spinner { width: 36px; height: 36px; border: 3px solid rgba(0,206,201,0.15);
    border-top-color: #00cec9; border-radius: 50%; animation: spin 0.8s linear infinite; }
  @keyframes spin { to { transform: rotate(360deg); } }
</style>
</head>
<body>

<div id="loading">
  <div class="loading-title">Shreyas's <span>Second Brain</span></div>
  <div class="loading-sub">Rendering knowledge graph…</div>
  <div class="spinner"></div>
</div>

<div id="header">
  <h1>🧠 <span>Second Brain</span> — Knowledge Graph</h1>
  <div id="stats"></div>
  <div id="controls">
    <input id="search" type="text" placeholder="🔍 Search notes…">
    <button class="btn" id="reset-zoom">Reset</button>
    <button class="btn" id="toggle-tags">Tags: On</button>
  </div>
</div>

<div id="graph"></div>
<div id="legend"><h3>Domains</h3><div id="legend-items"></div></div>
<div id="zoom-hint">Scroll to zoom · Drag to pan · Hover for details</div>

<div id="tooltip">
  <h4 id="tt-title"></h4>
  <div id="tt-domain"></div>
  <div class="meta" id="tt-meta"></div>
  <div class="links-row" id="tt-links"></div>
  <div class="tags-row" id="tt-tags"></div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
<script>
const GRAPH_DATA = __GRAPH_DATA__;
const nodes = GRAPH_DATA.nodes.map(n => ({...n}));
const links = GRAPH_DATA.links.map(l => ({...l}));
const DOMAIN_COLORS = __DOMAIN_COLORS_JSON__;
const allDomains = Object.keys(DOMAIN_COLORS).filter(d => d !== 'tag' && d !== 'default');
const activeDomains = new Set(allDomains);

document.getElementById('stats').textContent =
  `${nodes.length} nodes  ·  ${links.length} links  ·  ${allDomains.length} domains`;

// Legend
const legendEl = document.getElementById('legend-items');
allDomains.forEach(domain => {
  const color = DOMAIN_COLORS[domain] || '#636e72';
  const item = document.createElement('div');
  item.className = 'legend-item';
  item.dataset.domain = domain;
  item.innerHTML = `<div class="legend-dot" style="background:${color};color:${color}"></div><span>${domain}</span>`;
  item.addEventListener('click', () => {
    if (activeDomains.has(domain)) { activeDomains.delete(domain); item.classList.add('inactive'); }
    else { activeDomains.add(domain); item.classList.remove('inactive'); }
    updateVisibility();
  });
  legendEl.appendChild(item);
});

// SVG setup
const width = window.innerWidth, height = window.innerHeight - 52;
const svg = d3.select('#graph').append('svg').attr('width', width).attr('height', height)
  .style('background', 'radial-gradient(ellipse at 50% 40%, #0f1525 0%, #080b14 70%)');
const defs = svg.append('defs');

const glow = defs.append('filter').attr('id','glow').attr('x','-50%').attr('y','-50%').attr('width','200%').attr('height','200%');
glow.append('feGaussianBlur').attr('stdDeviation','3').attr('result','blur');
glow.append('feComposite').attr('in','SourceGraphic').attr('in2','blur').attr('operator','over');

const tagGrad = defs.append('radialGradient').attr('id','tag-grad');
tagGrad.append('stop').attr('offset','0%').attr('stop-color','#ffffff').attr('stop-opacity','0.9');
tagGrad.append('stop').attr('offset','100%').attr('stop-color','#94a3b8').attr('stop-opacity','0.6');

// Background stars
const starGroup = svg.append('g');
for (let i = 0; i < 120; i++) {
  const x = Math.random() * width, y = Math.random() * height, r = Math.random() * 1.2 + 0.2;
  starGroup.append('circle').attr('cx', x).attr('cy', y).attr('r', r)
    .attr('fill', 'white').attr('opacity', Math.random() * 0.25 + 0.05);
}

const g = svg.append('g');
const zoom = d3.zoom().scaleExtent([0.08, 12]).on('zoom', e => g.attr('transform', e.transform));
svg.call(zoom);
d3.select('#reset-zoom').on('click', () => svg.transition().duration(600).call(zoom.transform, d3.zoomIdentity));

const link = g.append('g').selectAll('line').data(links).join('line')
  .attr('stroke', 'rgba(100,116,139,0.2)').attr('stroke-width', d => Math.sqrt(d.weight || 1) * 0.6)
  .attr('stroke-opacity', 0.4);

const node = g.append('g').selectAll('circle').data(nodes).join('circle')
  .attr('r', d => d.size)
  .attr('fill', d => d.id.startsWith('#') ? 'url(#tag-grad)' : d.color)
  .attr('stroke', d => d.id.startsWith('#') ? 'rgba(255,255,255,0.3)' : 'rgba(255,255,255,0.15)')
  .attr('stroke-width', d => d.id.startsWith('#') ? 0.5 : 1)
  .attr('filter', d => d.degree > 15 ? 'url(#glow)' : null)
  .attr('cursor', 'pointer');

const label = g.append('g').selectAll('text').data(nodes.filter(n => n.degree > 8 && !n.id.startsWith('#')))
  .join('text').text(d => d.label)
  .attr('font-size', d => Math.min(11, 7 + d.degree * 0.2))
  .attr('font-family', 'Inter, sans-serif').attr('font-weight', '600')
  .attr('fill', d => d.color).attr('opacity', 0.85)
  .attr('pointer-events', 'none').attr('text-anchor', 'middle').attr('dy', d => -d.size - 4);

// Tooltip
const tooltip = document.getElementById('tooltip');
node.on('mousemove', (event, d) => {
  tooltip.style.display = 'block';
  tooltip.style.left = (event.clientX + 16) + 'px';
  tooltip.style.top  = (event.clientY - 10) + 'px';
  document.getElementById('tt-title').textContent = d.label;
  document.getElementById('tt-domain').innerHTML = `<span class="domain-badge" style="background:${d.color}22;color:${d.color};border:1px solid ${d.color}44">${d.domain}</span>`;
  document.getElementById('tt-meta').innerHTML = `<strong>Degree</strong> ${d.degree} &nbsp;·&nbsp; <strong>Community</strong> ${d.community}`;
  const linkNames = d.links.slice(0, 6).map(l => `<span>${l.split('|')[0].split('/').pop().substring(0, 30)}</span>`).join('');
  document.getElementById('tt-links').innerHTML = linkNames ? `<strong>Links:</strong> ${linkNames}` : '';
  const tagNames = d.tags.slice(0, 6).map(t => `<span>#${t}</span>`).join('');
  document.getElementById('tt-tags').innerHTML = tagNames ? `<strong>Tags:</strong> ${tagNames}` : '';
  const rect = tooltip.getBoundingClientRect();
  if (rect.right > window.innerWidth)  tooltip.style.left = (event.clientX - rect.width - 16) + 'px';
  if (rect.bottom > window.innerHeight) tooltip.style.top  = (event.clientY - rect.height - 10) + 'px';
}).on('mouseleave', () => { tooltip.style.display = 'none'; });

// Drag
const drag = d3.drag()
  .on('start', (e, d) => { if (!e.active) sim.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; })
  .on('drag', (e, d) => { d.fx = e.x; d.fy = e.y; })
  .on('end', (e, d) => { if (!e.active) sim.alphaTarget(0); d.fx = null; d.fy = null; });
node.call(drag);

// Simulation
const sim = d3.forceSimulation(nodes)
  .force('link',      d3.forceLink(links).id(d => d.id).distance(80).strength(0.4))
  .force('charge',    d3.forceManyBody().strength(-200).distanceMax(400))
  .force('center',    d3.forceCenter(width / 2, height / 2).strength(0.08))
  .force('collide',   d3.forceCollide(d => d.size + 4).strength(0.7))
  .force('x',         d3.forceX(width  / 2).strength(0.03))
  .force('y',         d3.forceY(height / 2).strength(0.03))
  .on('tick', () => {
    link.attr('x1', d => d.source.x).attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x).attr('y2', d => d.target.y);
    node.attr('cx', d => d.x).attr('cy', d => d.y);
    label.attr('x', d => d.x).attr('y', d => d.y);
  });

// Search
const searchEl = document.getElementById('search');
searchEl.addEventListener('input', () => {
  const q = searchEl.value.toLowerCase().trim();
  node.attr('opacity', d => !q ? 1 : (d.label.toLowerCase().includes(q) || d.domain.toLowerCase().includes(q) ? 1 : 0.08));
  label.attr('opacity', d => !q ? 0.85 : (d.label.toLowerCase().includes(q) ? 1 : 0.04));
});

// Tags toggle
let tagsVisible = true;
d3.select('#toggle-tags').on('click', function() {
  tagsVisible = !tagsVisible;
  this.textContent = `Tags: ${tagsVisible ? 'On' : 'Off'}`;
  node.attr('opacity', d => d.id.startsWith('#') ? (tagsVisible ? 0.85 : 0) : 1);
});

function updateVisibility() {
  node.attr('opacity', d => {
    if (d.id.startsWith('#')) return tagsVisible ? 0.85 : 0;
    return activeDomains.has(d.domain) ? 1 : 0.06;
  });
  label.attr('opacity', d => activeDomains.has(d.domain) ? 0.85 : 0);
}

setTimeout(() => {
  const el = document.getElementById('loading');
  el.classList.add('fade');
  setTimeout(() => el.remove(), 500);
}, 800);
</script>
</body>
</html>"""

domain_colors_json = json.dumps(DOMAIN_PALETTE, indent=2)
html = html.replace("__GRAPH_DATA__", json.dumps(graph_data, indent=2))
html = html.replace("__DOMAIN_COLORS_JSON__", domain_colors_json)

OUT.write_text(html, encoding="utf-8")
print(f"\n✅ Saved: {OUT}")
print(f"   Open: file:///{OUT.as_posix().replace(chr(92), '/')}")
print(f"   {len(node_list)} nodes · {len(edge_list)} links")