# Mapping the Workforce: A Social Network Analysis of Job Interconnectivity

Two occupations are linked if the Pearson correlation between their O*NET skill importance profiles exceeds 0.95. If two jobs rank their skills in a similar order and priority, they are connected.

### Group Members: Natesh Oad, Umesh Oad, Haziq Khawaja
---

## Requirements

Install dependencies:
```
pip install pandas numpy matplotlib seaborn networkx
```

Download the following files from [O*NET 30.2](https://www.onetcenter.org/database.html) as **Text/Tab-delimited** and place them in the project root:
- `Occupation Data.txt`
- `Skills.txt`

---

## How to Run

### Step 1 — Build the Network
Run `NetworkConstruction/LargeScope_Question1.ipynb`.

This reads `Occupation Data.txt` and `Skills.txt` and outputs:
- `occ_nodes.csv` — node table
- `occ_edges.csv` — edge table

### Step 2 — Import into Gephi
1. Open Gephi and import `occ_nodes.csv` and `occ_edges.csv`
2. Run **Modularity** under Statistics to detect communities
3. Export the node table as `Nodes.csv` (this adds the `modularity_class` and `betweenesscentrality` columns used by the scripts below)

### Step 3 — Run Analysis Scripts
The scripts below are standalone versions of the notebook analyses, converted to `.py` format for cleaner execution. Each runs independently. Make sure `Nodes.csv` and `Skills.txt` are in the same folder.

| Script | What it produces |
|---|---|
| `bridge_heatmap.py` | `Ranked_Bridge_Heatmap_Professional.png` |
| `modularity.py` | Prints skill averages per community to terminal |
| `transition_skill.py` | `Highly_Transitionable_Skills.png` |
| `visualize.py` | `Macro_Cluster_Heatmap.png`, `Small_Multiples_Radar_8.png`, `Master_Combined_Radar_8.png` |

Run any script with:
```
python bridge_heatmap.py
python modularity.py
python transition_skill.py
python visualize.py
```

### Step 4 — Notebooks
The notebooks below cover the same analyses as the scripts above, plus additional investigations. They can be run independently in Jupyter after Step 2 is complete:
- `DegreeDistribution.ipynb` — degree distribution of the network
- `notebooks_Charts_Question_7-4.ipynb` — additional chart analysis
- `notebooks_Random_Job_Removal_Analysis_Notebook.ipynb` — robustness under random job removal
- `notebooks_Routine_Workforce_Analysis_Notebook.ipynb` — routine vs. non-routine workforce breakdown

---

## Data Sources

- [O*NET 30.2 Database](https://www.onetcenter.org/database.html) — occupational skill data
- [Gephi](https://gephi.org/) — network visualization and community detection
