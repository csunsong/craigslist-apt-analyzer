import csv
import time
import re
import numpy as np
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
from operator import itemgetter

from CL_apt_scraper.items import AptData
from CL_apt_scraper.spiders.CLScraper import ClScraper

Apartment_List = [['price', 'bedrooms', 'area']]
metric = []
url = []

def write_to_file(filename, data_sample):
    example = csv.writer(open(filename, 'w'), dialect='excel')
    example.writerows(data_sample)

def open_with_csv(filename, d=','):
    data = []
    with open(filename) as tsvin:
        tie_reader = csv.reader(tsvin, delimiter=d)
        for line in tie_reader:
            data.append(line)

    return data

def plot_results(data_set):
    data = [go.Bar(
        x=[x[0] for x in data_set],
        y=[x[1] for x in data_set])
    ]

    layout = go.Layout(
        title=metric[0].capitalize() + ' Rental Prices: ' + url[0],
        xaxis=dict(
            tickangle=-45,
            title='Neighborhood',
            tickfont=dict(
                size=8,
            ),
        ),
        yaxis=dict(
            title='$/Month'
        ),
    )

    fig = go.Figure(data=data, layout=layout)
    plot_url = py.plot(fig, filename='basic-bar')

def parse_apt_data(data_sample, metric):
    price = data_sample[0].index('price')
    br = data_sample[0].index('bedrooms')
    area = data_sample[0].index('area')

    apts = []
    for row in data_sample[1:]:
        try:
            apts.append([row[area].lower(), int(
                row[price].replace("$", '')), row[br]])
        except ValueError:
            print("Error in data format: ", [row[area], row[price], row[br]])

    apt_data = {
        'location': [el[0] for el in apts],
        'price': [el[1]for el in apts],
        'uniq': [str(el[0]) + str(el[1]) + str(el[2]) for el in apts]
    }

    apt_dataframe = pd.DataFrame(apt_data).drop_duplicates(subset=['uniq'])
    apt_dataframe = apt_dataframe.groupby(
        by="location").filter(lambda x: len(x['location']) > 1)

    if metric == 'median':
        apt_dataframe = apt_dataframe.groupby(by="location").median()
    elif metric == 'mean':
        apt_dataframe = apt_dataframe.groupby(by="location").mean()
    else:
        raise Exception("Error: metric argument can only accept 'median' or 'mean'. You put '%s' " % metric)

    apt_dataframe.to_csv(path_or_buf='apt_grouped_prices.csv', sep=',',)

    vals = [int(val) for val in apt_dataframe.values]
    areas = [area for area in apt_dataframe.axes[0]]

    analyzed_list = [[areas[i], vals[i]] for i in range(0, len(areas))]
    analyzed_list = sorted(analyzed_list, key=itemgetter(1), reverse=True)
    plot_results(analyzed_list)


class CLAptScrapePipeline(object):

    def open_spider(self, spider):
        metric.append(spider.metric)
        url.append(spider.regional_url)

    def process_item(self, item, spider):
        Apartment_List.append(
            [item['price'], item['room_count'], re.sub(r'[^\w\s]', '', item['area'])])
        return item

    def close_spider(self, spider):
        write_to_file('full_apt_data.csv', Apartment_List)
        parse_apt_data(Apartment_List, metric[0])
