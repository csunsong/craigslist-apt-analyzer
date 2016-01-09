Provides an easy Scrapy-based tool to search, collect, and analyze apartment rental prices in regional markets.

<b>Requirements:</b> 
<ul>
<li> Working version of Python 2.7</li>
<li> Working version of <a href='http://scrapy.org/download/'>Scrapy</a> </li>
<li> <a href='https://plot.ly/python/getting-started/'>Plotly for Python <a></li>
<li> <a href='http://pandas.pydata.org/'>Pandas</a> and <a href='http://www.scipy.org/scipylib/download.html'>Numpy</a> 
</ul>

<b>Usage:</b>

```
$ cd Craigslist_Apt_Analyzer
```
Pass in a regional craigslist apartment listing URL as an argument:
```
$ scrapy crawl cl_apt -a regional_url=http://sfbay.craigslist.org/search/sby/apa
```

Specify apartment size with 'br' argument (defaults to 1):
```
$ scrapy crawl cl_apt -a regional_url=http://sfbay.craigslist.org/search/sby/apa -a br=2 
```

Specify the analysis metric with 'metric' argument (Accepts either mean or median; defaults to median):
```
$ scrapy crawl cl_apt -a regional_url=http://sfbay.craigslist.org/search/sby/apa -a br=2 -a metric=mean
```

Specify the page depth to search with 'search_depth' aregument (default: 25, max: 25, min: 2):
```
$ scrapy crawl cl_apt -a regional_url=http://sfbay.craigslist.org/search/sby/apa -a br=2 -a search_depth=20
```

Raw and analyzed Apartment data will write to separate CSV files. Plotly bar chart data opens in new window. 
