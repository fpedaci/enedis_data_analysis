# enedis_data_analysis
Analysis and plot of Enedis (France) consumption data

Once the .csv file is downloaded from the Enedis website, this script reads it and produces plots like the one below.

Usage from python or ipython:
```python
import enedis_analysis

# plots all the data and the daily average between index c0 and c1:
ea = enedis_analysis.Enedis_analyse('Enedis_Conso.csv', c0=3000, c1=-1)

# optional, change c0,c1:
ea.plots(c0=2000,c1=3000)
```

<img src="Screenshot.png" alt="drawing" width="500"/>

