from spyre import server

import pandas as pd
import urllib2
import matplotlib.pyplot as plt

class StockExample(server.App):
  title = "Inputs"

  inputs = [{   "type":'dropdown',
                "label": 'Index  ',
                "options" : [ {"label": "VCI", "value":"VCI"},
                                {"label": "TCI", "value":"TCI"},
                                {"label": "VHI", "value":"VHI"},],
                "key": 'index',
                "action_id": "update_data"},

              { "type":'dropdown',
                "label": 'Region',
                "options" : [ {"label": "Vinnitsya", "value":"01"},
                                  {"label": "Volyn", "value":"02"},
                                  {"label": "Dnipropetrovsk", "value":"03"},
                                  {"label": "Donetsk", "value":"04"},
                                  {"label": "Zhytomyr", "value":"05"},
                                  {"label": "Transcarpathia", "value":"06"},
                                  {"label": "Zaporizhzhya", "value":"07"},
                                  {"label": "Ivano-Frankivsk", "value":"08"},
                                  {"label": "Kiev", "value":"09"},
                                  {"label": "Kirovohrad", "value":"10"},
                                  {"label": "Luhansk", "value":"11"},
                                  {"label": "Lviv", "value":"12"},
                                  {"label": "Mykolayiv", "value":"13"},
                                  {"label": "Odessa", "value":"14"},
                                  {"label": "Poltava", "value":"15"},
                                  {"label": "Rivne", "value":"16"},
                                  {"label": "Sumy", "value":"17"},
                                  {"label": "Ternopil", "value":"18"},
                                  {"label": "Kharkiv", "value":"19"},
                                  {"label": "Kherson", "value":"20"},
                                  {"label": "Khmelnytskyy", "value":"21"},
                                  {"label": "Cherkasy", "value":"22"},
                                  {"label": "Chernivtsi", "value":"23"},
                                  {"label": "Chernihiv", "value":"24"},
                                  {"label": "Crimea", "value":"25"},
                                  {"label": "Kiev City", "value":"26"},
                                  {"label": "Sevastopol", "value":"27"}],
                "key": 'region',
                "action_id": "update_data"},

              { "input_type":"text",
                "variable_name":"year",
                "label": "Year",
                "value":1981,
                "key": 'year',
                "action_id":"update_data"},

              { "type":'slider',
                "label": 'First week',
                "min" : 1,"max" : 52,"value" : 35,
                "key": 'first',
                "action_id": 'update_data'},

              { "type":'slider',
                "label": 'Last week',
                "min" : 1,"max" : 52,"value" : 35,
                "key": 'last',
                "action_id": 'update_data'},

              { "type":'slider',
                "label": 'Percent of area',
                "min" : 0,"max" : 100,"value" : 0,
                "key": 'percent',
                "action_id": 'update_data'},

              { "type":'slider',
                "label": 'Minimum VHI',
                "min" : 0,"max" : 100,"value" : 0,
                "key": 'minimum',
                "action_id": 'update_data'},

              { "type":'slider',
                "label": 'Maximum VHI',
                "min" : 0,"max" : 100,"value" : 100,
                "key": 'maximum',
                "action_id": 'update_data'},]

  controls = [{   "type" : "hidden",
                  "id" : "update_data"}]

  tabs = ["Plot", "Table", "Drought", "Extremes", "Size"]

  outputs = [{  "type" : "plot",
                "id" : "plot",
                "control_id" : "update_data",
                "tab" : "Plot"},
              { "type" : "table",
                "id" : "table",
                "control_id" : "update_data",
                "tab" : "Table"},
              { "type" : "html",
                "id" : "drought",
                "control_id" : "update_data",
                "tab" : "Drought"},
              { "type" : "table",
                "id" : "table1",
                "control_id" : "update_data",
                "tab" : "Extremes"},
              { "type" : "html",
                "id" : "data_size",
                "control_id" : "update_data",
                "tab" : "Size"}]

  def table(self, params):
    index = params['index']
    region = params['region']
    year = params['year']
    first = params['first']
    last = params['last']

    path = '../lab1/clean_data/06_03_5pm{}.csv'.format(region)

    df = pd.read_csv(path, index_col=False, header=9,
                     names=['year', 'week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'VHI<15', 'VHI<35'])
    df1 = df[(df['year'] == int(year)) & (df['week'] >= int(first)) & (df['week'] <= int(last))]
    df1 = df1[['week', index]]
    return df1

  def getPlot(self, params):
    index = params['index']
    year = params['year']
    first = params['first']
    last = params['last']
    df = self.table(params).set_index('week')
    plt_obj = df.plot()
    plt_obj.set_ylabel(index)
    plt_obj.set_title('Index {index} for {year} from {first} to {last} weeks'.format(index=index,
      year=int(year), first=int(first), last=int(last)))
    fig = plt_obj.get_figure()
    return fig

  def drought(self, params):
    region = params['region']
    minimum = params['minimum']
    maximum = params['maximum']
    percent = params['percent']

    path = '../lab1/clean_data/06_03_5pm{}.csv'.format(region)
    df = pd.read_csv(path, index_col=False, header=9,
                     names=['year', 'week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'VHI<15', 'VHI<35'])
    df1 = df[(df['VHI'] < int(maximum)) & (df['VHI'] > int(minimum)) & (df['VHI<15'] > int(percent))]
    df1 = df1[['year', 'VHI', 'VHI<15']]
    return 'Years with percent of area > {percent} with drought: {years}'.format(percent=int(percent),
      years = pd.unique(df1.year.ravel()))

  def table1(self, params):
      index = params['index']
      region = params['region']
      year = params['year']

      path = '../lab1/clean_data/06_03_5pm{}.csv'.format(region)

      df = pd.read_csv(path, index_col=False, header=9,
                       names=['year', 'week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'VHI<15', 'VHI<35'])
      return df.loc[pd.concat((df.groupby(['year'])['VHI'].idxmax(), df.groupby(['year'])['VHI'].idxmin()))]

  def data_size(self, params):
      region = params['region']
      path = '../lab1/clean_data/06_03_5pm{}.csv'.format(region)

      df = pd.read_csv(path, index_col=False, header=9,
                       names=['year', 'week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'VHI<15', 'VHI<35'])

      return 'Size of dataframe: {size}'.format(size=df.shape)


app = StockExample()
app.launch(host='0.0.0.0')
