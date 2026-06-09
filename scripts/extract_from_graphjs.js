// Extract people / institutions / edges from graph.js into JSONL.
// Runs the Alpine.js component function in a sandbox, captures the return.

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const WORKSPACE = '<workspace>';
const GRAPH_JS = path.join(WORKSPACE, 'evil-robots-series/website/static/tech/revolving-door/graph.js');
const OUT_DIR = path.join(WORKSPACE, 'evil-robots-series/research/ratchet-mcp/server/data');

const src = fs.readFileSync(GRAPH_JS, 'utf8');

// graph.js declares `function revolvingDoorGraph()` and registers it on
// `document.addEventListener('alpine:init', ...)`. We only need the function.
// Strip the addEventListener block (and anything after the function definition
// that depends on browser globals) by evaluating the function body in a vm
// context with a stubbed `document` + `Alpine`.
const sandbox = {
  document: { addEventListener: () => {} },
  Alpine: { data: () => {} },
  window: {},
  console,
};
vm.createContext(sandbox);
vm.runInContext(src, sandbox);

const graph = sandbox.revolvingDoorGraph();

fs.mkdirSync(OUT_DIR, { recursive: true });

const write = (file, rows, kind) => {
  const f = fs.openSync(path.join(OUT_DIR, file), 'w');
  for (const row of rows) {
    if (kind) row.kind = kind;
    fs.writeSync(f, JSON.stringify(row) + '\n');
  }
  fs.closeSync(f);
};

// graph.js shape varies — match what's actually returned.
const institutions = graph.institutions || [];
const people = graph.people || [];
const edges = graph.links || graph.edges || [];

write('institutions.jsonl', institutions, 'institution');
write('people.jsonl', people, 'person');

// Edges are plain [source, target] tuples or {source, target} objects.
{
  const f = fs.openSync(path.join(OUT_DIR, 'edges.jsonl'), 'w');
  for (const e of edges) {
    if (Array.isArray(e)) {
      fs.writeSync(f, JSON.stringify({ source: e[0], target: e[1] }) + '\n');
    } else {
      fs.writeSync(f, JSON.stringify(e) + '\n');
    }
  }
  fs.closeSync(f);
}

console.log(
  `Wrote ${institutions.length} institutions, ${people.length} people, ${edges.length} edges to`
);
console.log(OUT_DIR);
