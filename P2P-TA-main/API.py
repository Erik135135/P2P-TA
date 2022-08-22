from classes.BidManager_Sender import *
from classes.TransactionManager import *
from classes.IllustrationManager import *
from functions.API_spot_price import spot_market_API_enstoe
import pandas as pd
import warnings
#warnings.filterwarnings('ignore')

import datetime
# warnings.filterwarnings('ignore')
# warnings.filterwarnings('ignore', category=GuessedAtParserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

import plotly.graph_objects as go

pd.options.mode.chained_assignment = None

text_all = []

### Check list######

####implement the data to #########
####I need the units of the different information#####
#### Draw the P2P trades for end-users

im = Illustration()

Input_Data = pd.read_excel(r'data\Input_data.xlsx')
one_day_forecast= str(Input_Data['Time_alternative(Defined time, Today, All data)'][0])
frequency_data = str(Input_Data['Minute frequency on API data (5,10,…60)'][0]) + 'T'
frequency_market = str(Input_Data['Minute frequency P2P market (5,10,.. 60)'][0]) + 'T'
api_key = str(Input_Data['Enstoe_API-key'][0])
frequency_ratio = int(Input_Data['Minute frequency P2P market (5,10,.. 60)'][0] / Input_Data['Minute frequency on API data (5,10,…60)'][0])
Country_code = str(Input_Data['Country_code_for_spot_price'][0])
excel_data = str(Input_Data['Energy data source (API/Excel)'][0])


dt_spot_low = datetime.datetime.strptime('2015-01-01', '%Y-%m-%d')
data_match = 'Yes'
Time_start_equal = 'No'
Time_end_equal = 'No'
data_no_spot = 'False'
market = 'True'
today_ = 'True'
time_start = datetime.datetime.now() - timedelta(days=0)
time_start_date = time_start.date()
time_start = time_start.strftime("%Y%m%d")
time_end = datetime.datetime.now() + timedelta(days=2)
time_end = time_end.strftime("%Y%m%d")
df_spot_price = spot_market_API_enstoe(contry_code=Country_code, startdate=time_start, enddate=time_end, apiKey=api_key)
dt_spot_high = df_spot_price.index[-1]


Api_data_production = str(Input_Data['Energy data API adress PV'][0])
Api_data_demand = str(Input_Data['Energy data API adress demand'][0])
if excel_data == 'Excel':
    production = pd.read_excel('data/Production_data.xlsx')
    demand = pd.read_excel('data/Demand_data.xlsx')
else:
    production = pd.read_json(Api_data_production)
    demand = pd.read_json(Api_data_demand)

date_name_production = production.head(0).columns[0]
date_name_demand = demand.head(0).columns[0]
time_start_production = production[date_name_production].iloc[0]
time_end_production = production[date_name_production].iloc[-1]
time_start_demand = demand[date_name_demand].iloc[0]
time_end_demand = demand[date_name_demand].iloc[-1]

# print('Start date of production data is: ', time_start_production, ', and start date of demand data is: ', time_start_demand)
# print('End date of production data is: ', time_end_production, ', and end date of demand data is: ', time_end_demand)
text_all = []

text_all.append('You have chosen the time alternative: ' + one_day_forecast + '.')
if excel_data == 'Excel':
    text_all.append('Data provided is from Excel. Production data: ' + str(time_start_production.tz_localize(None)) + ' - ' + str(time_end_production.tz_localize(None)) + '. Demand data: ' + str(time_start_demand.tz_localize(None)) + ' - ' + str(time_end_demand.tz_localize(None)) +'.')
else:
    text_all.append('Data provided is from API. Production data: ' + str(time_start_production.tz_localize(None)) + ' - ' + str(time_end_production.tz_localize(None)) + '. Demand data: ' + str(time_start_demand.tz_localize(None)) + ' - ' + str(time_end_demand.tz_localize(None)) +'.')
if time_start_production == time_start_demand:
    Time_start_equal = 'Yes'
if time_end_production == time_end_demand:
    Time_end_equal = 'Yes'
if time_start_production > time_end_demand:
    # print('The production and demand data you have provided do not correspond. The production data starts: ', time_start_production, '. This is after the end time of the demand data: ', time_end_demand)
    # data_match = 'No'
    # print('The P2P market will not run because the data you provided do not match in time')
    text_all.append('The production and demand data you have provided do not correspond. The production data starts: ' + str(time_start_production.tz_localize(None)) + '. This is after the end time of the demand data: ' + str(time_end_demand.tz_localize(None)) + '.')
    data_match = 'No'
    text_all.append('The P2P trading algorithm will not run because the data you provided do not match. Please provide data within the same time.')
elif time_start_demand > time_end_production:
    text_all.append('The production and demand data you have provided do not correspond at all. The demand data starts: ' + str(time_start_demand.tz_localize(None)) +'. This is after the end time of the production data: ' + str(time_end_production.tz_localize(None)) +'. Please correct you data.')
    data_match = 'No'
    text_all.append('The P2P trading algorithm will not run because the data you provided do not match. Please provide data within the same time.')
if time_end_production.tz_localize(None) < dt_spot_low:
    text_all.append('It is not possible to collect Day-ahead prices for the time of your data, please provide data after ' + str(dt_spot_low) + '.')
    data_no_spot = 'True'
    text_all.append('The P2P trading algorithm will not run because there do not exist spot-prices for the data you provided')
elif time_end_demand.tz_localize(None) < dt_spot_low:
    text_all.append('It is not possible to collect Day-ahead prices for the time of your data, please provide data after ' + str(dt_spot_low) + '.')
    data_no_spot = 'True'
    text_all.append('The P2P trading algorithm will not run because there do not exist spot-prices for the data you provided.')
elif time_start_demand.tz_localize(None) < dt_spot_low or time_start_production.tz_localize(None) < dt_spot_low or time_start_demand.tz_localize(None) > dt_spot_high.tz_localize(None) or time_start_production.tz_localize(None) > dt_spot_high.tz_localize(None):
    text_all.append('Some of the data you have provided is not possible to collect spot-prices for, please provide all data after ' + str(dt_spot_low) + ' and before ' + str(dt_spot_high) + '.')
    data_no_spot = 'True'
    text_all.append('It is not possible to collect Day-ahead prices for the time of your data.')

if one_day_forecast == 'Today':
    if (datetime.datetime.today().date() <= time_start_production) and (time_end_production >= datetime.datetime.today().date()):
        text_all.append('You have not provided any production data for today')
        today_ = 'Not True'
    elif (datetime.datetime.today().date() >= time_start_production) and (time_end_production <= datetime.datetime.today().date()):
        text_all.append('You have not provided any production data for today')
        today_ = 'Not True'
    if (datetime.datetime.today().date() <= time_start_demand) and (time_end_demand >= datetime.datetime.today().date()):
        text_all.append('You have not provided any demand data for today')
        today_ = 'Not True'
    elif (datetime.datetime.today().date() >= time_start_production) and (time_end_production <= datetime.datetime.today().date()):
        text_all.append('You have not provided any demand data for today')
        today_ = 'Not True'

if data_no_spot == 'False' and data_match == 'Yes':
    if Time_start_equal == 'Yes' and Time_end_equal == 'Yes':
        if one_day_forecast == 'Defined time':
            time_start = str(Input_Data['Start_time (yyyymmdd)'][0])
            time_end = str(Input_Data['End_time (yyyymmdd)'][0])
            time_start_date = datetime.datetime.strptime(time_start, "%Y%m%d")
            time_end_date = datetime.datetime.strptime(time_end, "%Y%m%d")
            if excel_data == 'Excel':
                text_all.append('In the excel file you have set the dates between ' + str(time_start_date) + ' - ' + str(time_end_date) + '.')
            if time_start_date.date() < time_start_production.date() or time_start_date.date() < time_end_production.date():
                time_start_date = time_start_production.date()
                time_start = datetime.datetime.strftime(time_start_date, "%Y%m%d")
                text_all.append('Your defined start date do not correspond with your data, your new start date is based on the start time of your data ' + str(time_start_production.date()) + '.')
            if time_end_date.date() > time_end_production.date() or time_end_date.date() < time_start_production.date():
                time_end_date_ = time_end_production.date()
                time_end = datetime.datetime.strftime(time_end_date_, "%Y%m%d")
                text_all.append('Your defined end date do not correspond with your data, your new end date is based on the end date of your data ' + str(time_end_production.date()) + '.')
            if time_end_production.date() > dt_spot_high.date():
                time_end_date = dt_spot_high.date() + datetime.timedelta(days=1)
                time_end = time_end_date.strftime("%Y%m%d")
                text_all.append('There is no spot_price after ' + str(dt_spot_high.date()) + ' 23:55. So the market will not operate longer.')
        elif one_day_forecast == 'Today':
            # Find yesterday date, and today
            time_start = datetime.datetime.now() - timedelta(days=0)
            time_start_date = time_start.date()
            time_start = time_start.strftime("%Y%m%d")
            time_end = datetime.datetime.now() + timedelta(days=1)
            time_end_date = time_end.date()
            time_end = time_end_date.strftime("%Y%m%d")
            if (time_start_date < time_start_production.date() and time_end_date < time_start_production.date()) or (time_start_date > time_start_production.date() and time_end_date > time_start_production.date()):
                text_all.append('The data provided do not contain any data from today: ' + str(time_start_date) + '.')
                text_all.append('You do not have data for running the P2P market for today. Try to use Defined time or All data, or change the datetime of your data.')
        elif one_day_forecast == 'All data':
            time_start = time_start_production.date()
            time_start = time_start.strftime("%Y%m%d")
            time_end_date = time_end_production.date()
            time_end = time_end_date.strftime("%Y%m%d")
            if time_end_demand.tz_localize(None) > dt_spot_high.tz_localize(None):
                time_end_date = dt_spot_high.date() + datetime.timedelta(days=1)
                time_end = time_end_date.strftime("%Y%m%d")
                text_all.append('There is no spot_price after ' + str(dt_spot_high.date()) + ' 23:55. So the market will not operate longer.')
    else:
        if one_day_forecast == 'Defined time':
            time_start = str(Input_Data['Start_time (yyyymmdd)'][0])
            time_end = str(Input_Data['End_time (yyyymmdd)'][0])
            time_start_date = datetime.datetime.strptime(time_start, "%Y%m%d")
            time_end_date = datetime.datetime.strptime(time_end, "%Y%m%d")
            if excel_data == 'Excel':
                text_all.append('In the excel file you have set the dates between ' + time_start_date + '-' + time_end_date)
            if time_start_date.date() < time_start_production.date() and time_start_date.date() < time_start_demand.date():
                time_start_date = max(time_start_production.date(), time_start_demand.date())
                time_start = datetime.datetime.strftime(time_start_date, "%Y%m%d")
                text_all.append('Your defined start date do not correspond with your data, the new start date is ' + str(time_start_date) + '.')
            if time_end_date.date() > time_end_production.date() and time_end_date.date() > time_end_demand.date():
                time_end_date = min(time_end_production.date(), time_end_demand.date())
                time_end = datetime.datetime.strftime(time_end_date, "%Y%m%d")
                text_all.append('Your defined end date do not correspond with your data, your new end date is based on the data ' + str(time_end_date) + '.')
            if min(time_end_demand.tz_localize(None), time_end_production.tz_localize(None)) > dt_spot_high.tz_localize(None):
                time_end_date = dt_spot_high.date() + datetime.timedelta(days=1)
                time_end = time_end_date.strftime("%Y%m%d")
                text_all.append('There is no spot_price after ' + str(dt_spot_high.date()) + ' 23:55. So the market will not operate longer.')
        elif one_day_forecast == 'Today':
            # Find yesterday date, and today
            time_start = datetime.datetime.now() - datetime.timedelta(days=0)
            time_start_date = time_start.date()
            time_start = time_start.strftime("%Y%m%d")
            time_end = datetime.datetime.now() + datetime.timedelta(days=1)
            time_end_date = time_end.date()
            time_end = time_end_date.strftime("%Y%m%d")
            if (time_start_date < time_start_production.date() and time_end_date < time_start_production.date()) or (time_start_date < time_start_demand.date() and time_end_date < time_start_demand.date()):
                text_all.append('The data provided do not contain any data from today ' + str(time_start_date) + '.Please check that the production and demand data.')
            text_all.append('The data provided do not contain any data from today ' + str(time_start_date) + 'Please check that the production and demand data.')
        elif one_day_forecast == 'All data':
            time_start_date = max(time_start_production.date(), time_start_demand.date())
            time_start = time_start_date.strftime("%Y%m%d")
            time_end_date = min(time_end_production.date(), time_end_demand.date())
            time_end = time_end_date.strftime("%Y%m%d")
            if time_end_demand.tz_localize(None) > dt_spot_high.tz_localize(None) or time_end_production.tz_localize(None) > dt_spot_high.tz_localize(None):
                time_end_date = dt_spot_high.date()
                time_end = time_end_date.strftime("%Y%m%d")
                text_all.append('There is not spot_price after ' + str(time_end_date) + 'so the end time is set to this time.')
            text_all.append('Your defined end date do not correspond with your data, your new end date is set to ' + str(time_end_date) + '.')

if data_no_spot == 'True':
    market = 'False'
    user_names = ['No Users']
    p2p_fig = im.draw_empty(user_names=user_names)
    P2P_fig_text = ' '
    fig_bar = im.draw_empty(user_names=user_names)
    fig_bar_text = ' '
    p2p_trans_fig = im.draw_empty(user_names=user_names)
    textp2p_transfig = ' '
    textp2p_transfigH5 = ' '

elif today_ == 'Not True':
    market = 'False'
    user_names = ['No Users']
    p2p_fig = im.draw_empty(user_names=user_names)
    P2P_fig_text = ' '
    fig_bar = im.draw_empty(user_names=user_names)
    fig_bar_text = ' '
    p2p_trans_fig = im.draw_empty(user_names=user_names)
    textp2p_transfig = ' '
    textp2p_transfigH5 = ' '

if data_no_spot == 'False' and data_match == 'Yes' and today_ == 'True':
    text_all.append('The P2P-market will operate from ' + time_start + ' until ' + time_end + '.')
    bm = BidManager(startdate=time_start, enddate=time_end, country_code='AT', freq=frequency_market)
    bm.add_bids_from_API(frequency_ratio=frequency_ratio, freq_market=frequency_market, demand=demand, production=production, api_key=api_key)
    #
    spot_tot, a, b = bm.add_spot_prices(freq=frequency_market, api_key=api_key)

    df_bids = bm.get_df_bids()

    #### Define how many timesteps we will match #########

    time_start1 = df_bids['time'][0]
    time_slutt1 = df_bids.iloc[-1]['time']

    tm = TransactionsManager()

    p2p_dict, timesteps = tm.p2p(df_bids, time_start=time_start1, time_stop=time_slutt1)

    user_names = df_bids['user'].unique().tolist()

    if any(p2p_dict.values()) == False:
        p2p_fig = im.draw_demand_user(df_bids=df_bids, user_names=user_names, spot_price=spot_tot, timesteps=timesteps)
        P2P_fig_text = im.txt_demand_user()
        fig_bar = im.draw_table_bids(df_bids=df_bids, user_names=user_names, timesteps=timesteps, spot_price=spot_tot)
        fig_bar_text = im.txt_table_bids()
        p2p_trans_fig = im.draw_empty(user_names=user_names)
        textp2p_transfig = im.txt_notransp2p()
        textp2p_transfigH5 = im.txt_notransp2pH5()
    else:
        p2p_fig = im.draw_demand_user_with_P2P(df_bids=df_bids, df_trans=p2p_dict, user_names=user_names,timesteps=timesteps)
        P2P_fig_text = im.txt_demand_user_with_P2P()
        fig_bar = im.draw_table(df_bids=df_bids, df_trans=p2p_dict, user_names=user_names, timesteps=timesteps,spot_price=spot_tot)
        fig_bar_text = im.txt_table_bids_with_P2P()
        p2p_trans_fig = im.draw_trans_user1(p2p_dict, user_names=user_names, timesteps=timesteps)
        textp2p_transfig = im.txt_nxplot()
        textp2p_transfigH5 = im.txt_H5trading()

text_full = '\n'.join(text_all)
text_main_p2p = "Here you can see the results from the Peer-to-Peer trading algorithm. In the first figure one can see the energy demand or production for each participant, and how when they did their trades. In the second figure the economic gains with or without P2P market. In the third, one can see how much and who one sold/bought from."




