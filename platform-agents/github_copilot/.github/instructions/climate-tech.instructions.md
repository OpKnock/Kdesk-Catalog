---
applyTo: "**/*.py **/*.r **/*.sh"
---

# climate-tech

Analyzes climate and energy data with Python ecosystem: pandas, xarray, rasterio, and emissions computation workflows.

## Instructions

# Climate Tech

Analyze climate, weather, and energy data.

## When to Use

- Processing NetCDF/CMIP model output
- Emissions accounting and scenario analysis
- Geospatial raster analysis (land cover, solar irradiance)
- Building energy and grid data pipelines

## Commands

```bash
pip install pandas xarray netcdf4 rasterio

# Inspect a NetCDF dataset
python -c "import xarray as xr; ds=xr.open_dataset('data.nc'); print(ds)"

# Time-averaged means
python -c "import xarray as xr; print(xr.open_dataset('data.nc').mean(dim='time'))"

# Emissions aggregation
python -c "import pandas as pd; df=pd.read_csv('emissions.csv'); print(df.groupby('year').co2.sum())"

# GWP-weighted CO2e
python -c "import pandas as pd; df=pd.read_csv('emissions.csv'); df['co2e']=df.co2*df.gwp; print(df.groupby('sector').co2e.sum())"

# Raster inspection
python -c "import rasterio; print(rasterio.open('raster.tif'))"
```

## Analysis Example

```python
import xarray as xr

ds = xr.open_dataset("temp_2m.nc")
annual_mean = ds.t2m.groupby("time.year").mean()
print(annual_mean.isel(year=-1))
```

## Best Practices

- Check units and coordinate systems before arithmetic
- Use xarray for labeled N-D data, pandas for tabular
- Prefer chunked reads for large CMIP files
- Record data provenance (source, version, processing steps)
- Validate against published figures before reporting
- Pin scientific package versions for reproducibility

## Capabilities

### climate-data
Process climate and weather datasets.

**Commands:**
- `pip install pandas xarray netcdf4`
- `python -c "import xarray as xr; ds=xr.open_dataset(\"data.nc\"); print(ds)"`
- `python -c "import pandas as pd; print(pd.read_csv(\"emissions.csv\").head())"`
- `pip install rasterio`
- `python -c "import rasterio; print(rasterio.open(\"tif/raster.tif\"))"`

**Examples:**
- python -c "import xarray as xr; print(xr.open_dataset(\"data.nc\").mean(dim=\"time\"))"
- python -c "import pandas as pd; df=pd.read_csv(\"emissions.csv\"); print(df.groupby(\"year\").co2.sum())"

### emissions-accounting
Compute and report emissions metrics.

**Commands:**
- `python -c "import pandas as pd; df=pd.read_csv(\"emissions.csv\"); df[\"co2e\"]=df.co2*df.gwp; print(df.groupby(\"sector\").co2e.sum())"`
- `python -m venv .venv && source .venv/bin/activate`
- `pip install openpyxl`
- `python -c "import pandas as pd; pd.DataFrame({\"x\":[1]}).to_excel(\"report.xlsx\"); print(\"ok\")"`

**Examples:**
- python -c "import pandas as pd; df=pd.read_csv(\"emissions.csv\"); print(df.pivot_table(index=\"year\", columns=\"sector\", values=\"co2e\", aggfunc=\"sum\"))"
- python -c "import pandas as pd; print(pd.read_excel(\"report.xlsx\"))"
