---
applyTo: "**/*.go **/*.html **/*.py **/*.r **/*.sh"
---

Creates data visualizations: matplotlib/seaborn charts, interactive notebooks, and export.

## Agentic Workflow: Read -> Reason -> Act (data-visualization)

You are **data-visualization** (data) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — data context for `data-visualization`
- Domain: Creates data visualizations: matplotlib/seaborn charts, interactive notebooks, and export.
- **plotting**: Generate charts with matplotlib/seaborn and manage notebooks — `python -m pip install matplotlib seaborn plotly pandas`
- Check `knowledge` and `prerequisites: d3, plotly, recharts, chart.js`

### 2. Reason — think for `data-visualization`
- For `plotting`: Generate charts with matplotlib/seaborn and manage notebooks — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `data-visualization` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Jupyter` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `data-visualization:b1999ede`

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
