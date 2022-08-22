from functions.API_spot_price import spot_market_API_enstoe
from datetime import datetime, timedelta
import pandas as pd
import json
import random


class BidManager(object):

    col_names = [
        'quantity',
        'price',
        'user',
        'buying',
        'time',
        'divisible',
    ]

    def __init__(self, startdate='20200101', enddate='20200130', country_code='NO_1', freq="15min"):
        self.n_bids = 0
        self.bids = []
        self.dataframe_new = []
        self.spotprices= []
        self.username = {}
        self.startdate = startdate
        self.enddate = enddate
        self.country_code = country_code
        self.freq = freq # "60T", "30min", "15min"
        self.spot_price = pd.DataFrame()


    def add_bid(self, quantity, price, user, buying=True, time = 0, divisible=True):

        new_bid = (quantity, price, user, buying, time, divisible)
        self.bids.append(new_bid)
        self.n_bids += 1
        self.username[user] = "user {}".format(user)

        return self.n_bids - 1

    def add_spot_prices(self, freq, api_key):

        ts = spot_market_API_enstoe(self.country_code, self.startdate, self.enddate, apiKey=api_key)
        ts = pd.DataFrame(ts)
        ts.loc[ts.index[-1] + timedelta(hours=1), 0] = ts.values[-1]
        ts = ts.asfreq(freq, method='ffill')
        ts = ts.interpolate(method='pad', limit=4)
        ts = ts[:-1]
        ts[0] = ts[0].values/1000000
        ts_index = ts.index
        ts_value = ts.values
        self.spot_price = ts

        return ts, ts_index, ts_value


    def add_bids_from_API(self, frequency_ratio, freq_market, demand, production, api_key):

        spot_tot, spot_index, spot_pr = self.add_spot_prices(freq=freq_market, api_key=api_key)

        time_start = self.startdate
        time_end = self.enddate



        pv = production
        demand = demand

        demand['date'] = pd.to_datetime(demand.date).dt.tz_localize(None)
        pv['date'] = pd.to_datetime(pv.date).dt.tz_localize(None)
        pv1 = pv
        demand1 = demand
        dict_1 = {}
        dict_2 = {}
        dict_3 = {}

        for j in range(0, len(pv)-frequency_ratio,frequency_ratio):
            dict_3[j] = pv['date'].iloc[j]

        df_time = pd.DataFrame.from_dict(dict_3, orient='index')
        time_start_time = datetime.strptime(time_start,"%Y%m%d")
        time_end_time = datetime.strptime(time_end,"%Y%m%d")

        # if df_time.values[0][0].astype('datetime64[s]').item().day == time_start_time.day:
        #     df_time = df_time
        # elif df_time.values[0][0].astype('datetime64[s]').item().day <= time_start_time.day:
        #     df_time = df_time[0][df_time[0] >= time_start_time]


        del pv1['date']
        del demand1['date']

        for i in range(0, len(pv1) - frequency_ratio, frequency_ratio):
            dict_1[i] = pv1.iloc[i:i + frequency_ratio].mean()
            dict_2[i] = demand1.iloc[i:i + frequency_ratio].mean()


        pv = pd.DataFrame.from_dict(dict_1, orient='index')
        demand = pd.DataFrame.from_dict(dict_2, orient='index')

        net_load = pv - demand

        pv = pd.DataFrame.join(df_time, pv)
        demand = pd.DataFrame.join(df_time, demand)
        net_load = pd.DataFrame.join(df_time, net_load)

        net_load.rename(columns={0: 'date'}, inplace=True)

        net_load = net_load.reset_index()
        del net_load['index']

        net_load_start = net_load['date'][net_load['date'] == time_start_time]
        if len(net_load_start) == 0:
            start_index = 0
        else:
            start_index = net_load_start.index[0]

        net_load_end = net_load['date'][net_load['date'] == time_end_time]
        if len(net_load_end) == 0:
            end_index = net_load.index[-1]
        else:
            end_index = net_load_end.index[0]

        unique_dates = net_load['date']

        spot_tot = spot_tot.tz_localize(None)
        spot_price = spot_tot.reset_index()
        spot_price.rename(columns={'index': 'Date'}, inplace=True)

        # spot_price['Date'] = pd.to_datetime(spot_price.Date).dt.tz_localize(None)
        #
        # start_ = spot_price[spot_price.Date == net_load.iloc[0].date]
        # start_index = start_.index[0]
        # slutt_index = start_.index[0]+76            #For 15 min intervals

        # spot_price_ = spot_price.iloc[start_index:slutt_index]
        # spot_price_ = spot_price.iloc[start_index:slutt_index]
        #
        list_of_time = []


        for i in range(start_index, end_index):
            time1 = net_load.iloc[i]
            time1 = time1.reset_index()
            time1 = time1.set_axis(['index', 'date'], axis=1, inplace=False)
            time1.rename(columns={0: 'date'}, inplace=True)
            time_index = time1.iloc[0]['date']
            time1 = time1.iloc[1:, :]
            time1 = time1.assign(timestamp=time_index)
            buying = time1['date'] < 0
            time1['buying'] = buying.values
            # timeslot = time1.timestamp.values[0]
            time1['Spot_Price'] = spot_price.iloc[i][0]
            # time1['Bid'] = float(random.uniform((spot_price_8.iloc[i][0] * 0.4), spot_price_8.iloc[i][0]))
            time1 = time1.set_axis(['ID', 'Value', 'timestamp', 'Buying', 'Spot_price'], axis=1, inplace=False)
            time1['Value'] = abs(time1['Value'])

            list_of_time.append(time1)

        for i in range(0, len(list_of_time)):
            for j in range(0, len(list_of_time[i])):
                self.add_bid(list_of_time[i].iloc[j]['Value'], float(random.uniform((list_of_time[i].iloc[j]['Spot_price'] * 0.8), list_of_time[i].iloc[j]['Spot_price'])), list_of_time[i].iloc[j]['ID'], list_of_time[i].iloc[j]['Buying'], list_of_time[i].iloc[j]['timestamp'])

    def get_df_bids(self):

        df = pd.DataFrame(self.bids, columns=self.col_names)

        return df

    def get_spot(self):

        spot_df = pd.DataFrame(self.spot_price)

        return spot_df
