# Graphectory: HypG Command-Level Trajectory Visualization

This repository extends **Graphectory** to support visualization of **HypG trajectories**.

The original Graphectory visualization was designed for SWE-agent trajectories. This extension adds a HypG graph builder that parses shell commands inside `run_bash_hypg_simple` and converts them into command-level graph nodes while reusing Graphectory's existing graph semantics.

## Features

- Support for HypG trajectory files
- Command-level graph construction
- Parsing of shell commands inside `run_bash_hypg_simple`
- Reuse of Graphectory's existing SWE-agent graph semantics
- Repeated-command merging
- Loop and revisit visualization
- Intra-step command-order visualization
- Hierarchical file-view visualization
- Interactive browser-based graph viewer

## Graph Semantics

### Edge Types

**Execution Edge (solid gray)**

Represents the execution flow between trajectory steps.

- Arrow size is proportional to the thought length.
- The number on the edge is the trajectory step index.

Example:

```
view (step 1) ──2──▶ view (step 2)
```

where **2** is the trajectory step index.

---

**Execution Edge (gray dashed)**

Represents an execution transition where the thought length is **0**.

---

**Intra-step Edge (blue dashed)**

Represents the execution order of multiple shell commands inside a single
`run_bash_hypg_simple` call.

Example:

```
echo
   ⇢
git add
   ⇢
git diff
```

---

**Hierarchy Edge (green dashed)**

Represents structural containment between compatible file-view operations.

Example:

```
view(file.py, L1–300)
          ⇢
view(file.py, L120–180)
```

meaning the first view contains the second.

---

### Node Colors

| Color | Phase | Examples |
|-------|-------|----------|
| 🟪 Purple | Localization | `view`, `ls`, `find`, `grep` |
| 🟧 Orange | Patch | `edit`, `str_replace`, `apply_patch` |
| 🟦 Blue | Validation | `pytest`, `python test.py` |
| ⬜ Gray | General | `think`, `submit`, other operations |

---

### Repeated Nodes

If the same command appears multiple times in a trajectory, Graphectory merges
them into a single node.

For example,

```
Step 2, Step 20
```

displayed on one node means the command was executed in both **step 2** and
**step 20**.

## HypG Input Format

The HypG loader expects matching files in the trajectory directory:

```text
<instance_id>.labelled.json
<instance_id>.fix.traj.json
```

For example:

```text
django__django-11848.labelled.json
django__django-11848.fix.traj.json
```

Both files must use the same instance ID.

## Requirements

Install the Python dependencies from the project root:

```powershell
pip install -e .
```

The viewer uses the files inside `graph_construction`, including:

```text
graph_template.html
graph_renderer.js
styles.css
server/
```

## How to Run

Open PowerShell and enter the clean repository directory:

```powershell
cd C:\Projects\Graphectory_trajectory_clean
```

Start the HypG trajectory visualization server:

```powershell
python graph_construction\live_graph_server.py --agent_type hypg --trajs "C:\Projects\hypgsimple-merged-manual"
```

Replace:

```text
C:\Projects\hypgsimple-merged-manual
```

with the directory containing your HypG `.labelled.json` and `.fix.traj.json` files.

After the server starts, the terminal should display:

```text
Trajectory Graph Server
Agent      : HYPG
URL        : http://localhost:8000
```

Open this address in a browser:

```text
http://localhost:8000
```

The left panel will display the available HypG instances. Select an instance to render its trajectory graph.

## Example Command

```powershell
cd C:\Projects\Graphectory_trajectory_clean

python graph_construction\live_graph_server.py `
  --agent_type hypg `
  --trajs "C:\Projects\hypgsimple-merged-manual"
```

PowerShell also accepts the command on one line:

```powershell
python graph_construction\live_graph_server.py --agent_type hypg --trajs "C:\Projects\hypgsimple-merged-manual"
```

## Stopping the Server

Return to the PowerShell window and press:

```text
Ctrl+C
```

## Optional Arguments

Use a different port:

```powershell
python graph_construction\live_graph_server.py --agent_type hypg --trajs "C:\Projects\hypgsimple-merged-manual" --port 8080
```

Then open:

```text
http://localhost:8080
```

An evaluation report can also be supplied:

```powershell
python graph_construction\live_graph_server.py `
  --agent_type hypg `
  --trajs "C:\Projects\hypgsimple-merged-manual" `
  --eval_report "path\to\report.json"
```

The evaluation report is optional. Without it, status badges are not displayed.

## Project Structure

```text
graph_construction/
├── buildGraph.py
├── commandParser.py
├── fix_traj_parser.py
├── generatejson.py
├── graph_renderer.js
├── graph_template.html
├── live_graph_server.py
├── mapPhase.py
├── styles.css
└── server/
    ├── __init__.py
    ├── graph_builder.py
    ├── graph_renderer.py
    ├── handler.py
    └── static/
```

## Main HypG Implementation

The main HypG-related code is located in:

```text
graph_construction/server/graph_builder.py
graph_construction/server/graph_renderer.py
graph_construction/graph_renderer.js
graph_construction/live_graph_server.py
graph_construction/fix_traj_parser.py
graph_construction/buildGraph.py
```

## Implementation Summary

The HypG extension:

- Loads paired HypG trajectory files
- Extracts commands from `run_bash_hypg_simple`
- Parses chained shell commands into separate nodes
- Preserves execution order
- Marks commands in the same bash call using blue dashed edges
- Creates hierarchy edges for compatible file-view operations
- Merges repeated commands into shared nodes
- Makes loops and revisits visible
- Reuses Graphectory's existing node phases and rendering semantics

## Relationship to SWE-agent

This repository does not require SWE-agent trajectory files when running in HypG mode.

However, the HypG visualization reuses the graph representation originally developed for Graphectory's SWE-agent trajectories, including:

- Phase-based node colors
- Execution edges
- Multi-command intra-step edges
- Hierarchical file-view edges
- Repeated-node merging
- Thought-length and observation visual encodings

This allows HypG and SWE-agent trajectories to be represented with comparable graph semantics.
