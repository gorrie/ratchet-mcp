// Minimal D3 force-directed viewer for the Ratchet dataset. Fetches the
// JSONL files served at /data/ and renders a node-link diagram. Click a
// node to populate the side panel.

const SECTOR_COLORS = {
  gov: "#4a8edb", fin: "#2ec47b", imf: "#b56fff", cfr: "#cc0000",
  tank: "#e8a83a", intel: "#ff5050", def: "#888899", tech: "#3acc99",
  multi: "#a05fff", judiciary: "#dca64a",
  // Foreign-state institutional cluster — distinct from primary cohort
  // colors so the eye reads "external influence vector" not "another sector"
  "china-state": "#8b0000",
  "russia-state": "#566573",
};

async function loadJsonl(url) {
  const r = await fetch(url);
  const text = await r.text();
  return text.split("\n").filter(Boolean).map((line) => JSON.parse(line));
}

async function main() {
  const status = document.getElementById("status");
  status.textContent = "Loading data...";
  const [people, institutions, edges] = await Promise.all([
    loadJsonl("/data/people.jsonl"),
    loadJsonl("/data/institutions.jsonl"),
    loadJsonl("/data/edges.jsonl"),
  ]);
  status.textContent = `${people.length} people · ${institutions.length} institutions · ${edges.length} edges`;

  const nodes = [...people, ...institutions];
  const links = edges.map((e) => Array.isArray(e) ? { source: e[0], target: e[1] } : e);

  const svg = d3.select("#graph");
  const width = svg.node().clientWidth;
  const height = parseInt(svg.attr("height"), 10);

  const sim = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).id((d) => d.id).distance(60))
    .force("charge", d3.forceManyBody().strength(-120))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force("collision", d3.forceCollide(12));

  const linkG = svg.append("g").attr("stroke", "#444").attr("stroke-opacity", 0.5);
  const link = linkG.selectAll("line").data(links).join("line");

  const nodeG = svg.append("g");
  const node = nodeG.selectAll("circle").data(nodes).join("circle")
    .attr("r", (d) => d.kind === "institution" ? 10 : 6)
    .attr("fill", (d) => SECTOR_COLORS[d.sector] || "#888")
    .attr("stroke", "#16161a")
    .attr("stroke-width", 1.5)
    .style("cursor", "pointer")
    .on("click", (event, d) => showDetail(d));

  node.append("title").text((d) => d.label || d.id);

  sim.on("tick", () => {
    link.attr("x1", (d) => d.source.x).attr("y1", (d) => d.source.y)
        .attr("x2", (d) => d.target.x).attr("y2", (d) => d.target.y);
    node.attr("cx", (d) => d.x).attr("cy", (d) => d.y);
  });
}

function showDetail(d) {
  const panel = document.getElementById("detail");
  panel.hidden = false;
  document.getElementById("detail-name").textContent = d.label || d.id;
  document.getElementById("detail-role").textContent = d.role || "";
  const tags = document.getElementById("detail-tags");
  tags.innerHTML = "";
  for (const field of ["sector", "admin", "networks", "plays", "actors"]) {
    const v = d[field];
    if (!v) continue;
    const li = document.createElement("li");
    li.textContent = `${field}: ${Array.isArray(v) ? v.join(", ") : v}`;
    tags.appendChild(li);
  }
  const srcs = document.getElementById("detail-sources");
  srcs.innerHTML = "";
  for (const s of (d.sources || [])) {
    const li = document.createElement("li");
    const a = document.createElement("a");
    a.href = s.url; a.target = "_blank"; a.rel = "noopener";
    a.textContent = `[${s.type}] ${s.url}`;
    li.appendChild(a);
    srcs.appendChild(li);
  }
}

main().catch((e) => {
  document.getElementById("status").textContent = "Error: " + e.message;
});
