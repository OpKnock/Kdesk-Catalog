---
applyTo: "**/*.go **/*.html **/*.py **/*.r **/*.sh"
---

Creates data visualizations: matplotlib/seaborn charts, interactive notebooks, and export.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `python -m pip install matplotlib seaborn plotly pandas`
- Check `knowledge` references and prerequisites before proceeding

### 2. Reason
Analyze and plan:
- Compare current state vs desired state (drift, checksums, policy)
- Evaluate trust, compatibility, and risk: use `kdesk trust` and `kdesk doctor` patterns
- Decide: which capabilities/tools are needed, which can be skipped

### 3. Act
Execute with guards:
- Run only `allowed-tools` (see frontmatter); use `safe_path` for writes
- Prefer `Bash` with explicit binaries (`curl`, `kubectl`, `kdesk`) over generic shell
- Record evidence: file paths, checksums, and tool outputs for verification

# Data Visualization

Turns data into clear charts: matplotlib/seaborn for static figures, Jupyter for
interactive exploration and reports.

## When to Use

- Explaining metrics to stakeholders
- Exploring datasets interactively
- Producing exportable report figures

## Real Commands

```bash
# Install
sudo python -m pip install matplotlib seaborn plotly pandas

# Static chart from a script
python charts/sales.py --output charts/sales.png

# Quick inline chart
python -c "import matplotlib.pyplot as plt; plt.plot([1,2,3],[1,4,9]); plt.savefig('trend.png')"

# Interactive notebooks
sudo jupyter lab --no-browser --port 8888

# Execute and export
sudo jupyter nbconvert --execute --inplace analysis.ipynb
sudo jupyter nbconvert --to html analysis.ipynb --output-dir reports/

# Slides export
sudo jupyter nbconvert --to slides analysis.ipynb
```

## Chart Choice Guide

- Time series: line chart
- Distribution: histogram / KDE
- Categories: bar chart
- Relationship: scatter with trend line
- Parts of a whole: stacked bar or donut (rarely pie)

## Best Practices

- Label axes and units; title charts with context
- Use consistent colors; check colorblind-safe palettes
- Keep the chart honest: start axes at zero for bars
- Save at high DPI: `plt.savefig('x.png', dpi=200)`
- Put the takeaway in the caption

## Example Response

Produces the requested charts, saves them to files, and explains the pattern the
visualization reveals with interpretation notes.

## Capabilities

### plotting
Generate charts with matplotlib/seaborn and manage notebooks

**Parameters:**
- `output` (string): Output file path for the chart
- `execute` (boolean): Execute the notebook during conversion
- `output-dir` (string): Directory for converted notebooks

**Commands:**
- `python -m pip install matplotlib seaborn plotly pandas`
- `python charts/sales.py --output charts/sales.png`
- `jupyter lab --no-browser --port 8888`
- `jupyter nbconvert --to html analysis.ipynb --output-dir reports/`
- `jupyter nbconvert --to slides analysis.ipynb --SlidesExporter.reveal_theme=serif`

**Examples:**
- python -c "import matplotlib.pyplot as plt; plt.plot([1,2,3],[1,4,9]); plt.savefig('p.png')"
- jupyter nbconvert --execute --inplace analysis.ipynb
- python charts/dashboard.py --style darkgrid --size 16x9

## References
- [matplotlib docs](https://matplotlib.org/)
- [seaborn docs](https://seaborn.pydata.org/)
- [Jupyter nbconvert docs](https://nbconvert.readthedocs.io/)
