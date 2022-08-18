import pandas as pd
from collections import OrderedDict
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image

import plotly.graph_objects as go
import plotly.express as px

import plotly.figure_factory as ff

class Illustration(object):

    def __init__(self):
        """
        """
        self.n_trans = 0

    def draw_trans(self, df_trans):
        list_trans = list(df_trans.values)

        list_of_users_trans = {}

        for j in np.unique([df_trans["Seller"].values, df_trans["Buyer"].values]):
            trans_user = []
            for t in range(0, len(list_trans)):
                if list_trans[t][0] == j:
                    trans_user.append(list_trans[t])
                elif list_trans[t][3] == j:
                    trans_user.append(list_trans[t])
            list_of_users_trans[j] = trans_user
        # for key in list_of_users_trans.keys():
        list_fig = []
        for key in np.unique(np.unique([df_trans["Seller"].values, df_trans["Buyer"].values])):
            list_of_byers = []
            list_of_sellers = []
            list_quantity_seller = []
            list_price_seller = []
            list_quantity_buyer = []
            list_price_buyer = []
            for i in range(0, len(list_of_users_trans[key])):
                list_of_sellers.append(' ' + list_of_users_trans[key][i][0] + ' ')
                list_of_byers.append(list_of_users_trans[key][i][3])
                if list_of_users_trans[key][i][0] == key:
                    list_quantity_buyer.append(round(list_of_users_trans[key][i][1], 6))
                    list_price_buyer.append(round(list_of_users_trans[key][i][2], 6))
                elif list_of_users_trans[key][i][3] == key:
                    list_quantity_seller.append(round(list_of_users_trans[key][i][1], 6))
                    list_price_seller.append(round(list_of_users_trans[key][i][2], 6))

            while key in list_of_byers:
                list_of_byers.remove(key)

            key11 = ' ' + key + ' '

            while key11 in list_of_sellers:
                list_of_sellers.remove(key11)

            list_sort_quantity_buy = dict()
            for j in list_of_byers:
                list_sort_quantity_buy[j] = 0

            list_sort_price_buy = dict()
            for j in list_of_byers:
                list_sort_price_buy[j] = 0

            for i in range(0, len(list_of_byers)):
                key_ = list_of_byers[i]
                quantity = list_quantity_buyer[i]
                price = list_price_buyer[i]
                list_sort_quantity_buy[key_] = list_sort_quantity_buy[key_] + quantity
                list_sort_price_buy[key_] = list_sort_price_buy[key_] + (price * quantity)

            list_sort_quantity_buy[key] = 0
            list_sort_price_buy[key] = 0

            list_sort_quantity_sell = dict()
            for j in list_of_sellers:
                list_sort_quantity_sell[j] = 0

            list_sort_price_sell = dict()
            for j in list_of_sellers:
                list_sort_price_sell[j] = 0

            for i in range(0, len(list_of_sellers)):
                key__ = list_of_sellers[i]
                quantity = list_quantity_seller[i]
                price = list_price_seller[i]
                list_sort_quantity_sell[key__] = list_sort_quantity_sell[key__] + quantity
                list_sort_price_sell[key__] = list_sort_price_sell[key__] + (price * quantity)

            list_sort_price_sell[key] = 0
            list_sort_quantity_sell[key] = 0

            quantity_dict = list_sort_quantity_sell.copy()  # start with keys and values of x
            quantity_dict.update(list_sort_quantity_buy)  # modifies z with keys and values of y

            price_dict = list_sort_price_sell.copy()
            price_dict.update(list_sort_price_buy)

            nodes_buyers = list(dict.fromkeys(list_of_byers))
            nodes_sellers = list(dict.fromkeys(list_of_sellers))

            # merged_list_sell = [(str(key), str(list_of_byers[i])) for i in range(0, len(list_of_byers))]
            # merged_list_buy = [(' '+ str( + list_of_sellers[i]) + ' ', str(key)) for i in range(0, len(list_of_sellers))]

            merged_list_sell = [(key, nodes_buyers[i]) for i in range(0, len(nodes_buyers))]
            merged_list_buy = [(nodes_sellers[i], key) for i in range(0, len(nodes_sellers))]

            G = nx.DiGraph()

            G.add_edges_from(merged_list_buy)
            G.add_edges_from(merged_list_sell)

            elarge = G.edges

            fixed_positions = {}

            if len(nodes_buyers) == 0:
                len_max_nodes = len(nodes_sellers)
            elif len(nodes_sellers) == 0:
                len_max_nodes = len(nodes_buyers)
            elif len(nodes_sellers) > 0 & len(nodes_buyers) > 0:
                len_max_nodes = max(len(nodes_buyers), len(nodes_sellers))

            fixed_positions[str(key)] = (len_max_nodes / 2, 0)

            for i in range(0, len(nodes_buyers)):
                fixed_positions[str(nodes_buyers[i])] = (i, -2)
            for j in range(0, len(nodes_sellers)):
                fixed_positions[str(nodes_sellers[j])] = (j, 2)

            fixed_nodes = fixed_positions.keys()

            pos = nx.spring_layout(G, pos=fixed_positions, fixed=fixed_nodes)

            Xn = [pos[k][0] for k in pos]
            Yn = [pos[k][1] for k in pos]
            labels = [k for k in pos]

            list_quantity = []

            for i in range(0, len(labels)):
                for key1 in quantity_dict.keys():
                    if key1 == labels[i]:
                        list_quantity.append(str(quantity_dict[key1]) + ' Wh')
                    else:
                        None

            list_price = []
            for i in range(0, len(labels)):
                for key2 in price_dict.keys():
                    if key2 == labels[i]:
                        list_price.append(str(price_dict[key2]) + ' €')
                    else:
                        None

            labels_node = []
            for i in range(0, len(list_price)):
                labels_node.append(list_quantity[i] + ',   ' + list_price[i])

            nodes = dict(type='scatter',
                         x=Xn,
                         y=Yn,
                         mode='markers+text',
                         hovertext=labels_node,
                         marker=dict(size=40, color='#A9F5A9'),
                         textfont=dict(size=18, color='#190707'),
                         text=labels,
                         hoverinfo='text')

            Xaxis = dict(showline=False, zeroline=False, showgrid=False, showticklabels=True,
                         mirror='allticks', ticks='inside', ticklen=5, tickfont=dict(size=14),
                         title='')

            Yaxis = dict(showline=False, zeroline=False, showgrid=False, showticklabels=True,
                         mirror='allticks', ticks='inside', ticklen=5, tickfont=dict(size=14),
                         title='')

            # annotateESmall = [
            #     dict(showarrow=True, arrowsize=1.5, arrowwidth=2, arrowhead=5, opacity=0.5, standoff=14, startstandoff=4,
            #          ax=pos[arrow[0]][0], ay=pos[arrow[0]][1], axref='x', ayref='y',
            #          x=pos[arrow[1]][0], y=pos[arrow[1]][1], xref='x', yref='y'
            #          ) for arrow in esmall]

            layout = dict(width=800, height=600,
                          showlegend=False,
                          xaxis=Xaxis,
                          yaxis=Yaxis,
                          hovermode='closest',
                          plot_bgcolor='#FFFFFF',
                          annotations=annotateELarge,  # arrows
                          )

            plotly_fig = dict(data=[nodes], layout=layout)

            fig = go.Figure(data=[nodes],
                            layout=layout)
            fig.update_xaxes(visible=False)
            fig.update_yaxes(visible=False)
            list_fig.append(fig)
        return list_fig

    def draw_trans_user1(self, p2p_dict, user_names, timesteps):

        user_names = user_names
        p2p_dict_time = {}

        for j in range(0, len(p2p_dict)):
            list_trans1 = []
            for i in range(0, len(p2p_dict[j])):
                list_trans1.append((*p2p_dict[j][i], (timesteps[j])))
            p2p_dict_time[j] = pd.DataFrame(list_trans1)

        df_trans_time = pd.concat(p2p_dict_time)
        df_trans_time = df_trans_time.set_axis(['seller', 'quantity', 'price', 'buyer','?', 'time'], axis=1, inplace=False)
        df_trans_time = df_trans_time[df_trans_time['quantity'] > 0]
        df_trans_time = df_trans_time.reset_index()
        del df_trans_time['level_0'], df_trans_time['level_1']

        # df_trans = df_trans.replace({1472663: 'Erik', 1462672: 'Joakim', 1472669: 'Eduardo', 1501313: 'Pedro'})

        list_trans = list(df_trans_time.values)

        list_of_fig = []

        list_of_users_trans = {}

        for j in user_names:
            trans_user = []
            for t in range(0, len(list_trans)):
                if list_trans[t][0] == j:
                    trans_user.append(list_trans[t])
                elif list_trans[t][3] == j:
                    trans_user.append(list_trans[t])
            list_of_users_trans[j] = trans_user

        for key in user_names:
            list_of_byers = []
            list_of_sellers = []
            list_quantity_seller = []
            list_price_seller = []
            list_quantity_buyer = []
            list_price_buyer = []
            for i in range(0, len(list_of_users_trans[key])):
                list_of_sellers.append(' ' + list_of_users_trans[key][i][0] + ' ')
                list_of_byers.append(list_of_users_trans[key][i][3])
                if list_of_users_trans[key][i][0] == key:
                    list_quantity_buyer.append(round(list_of_users_trans[key][i][1], 6))
                    list_price_buyer.append(round(list_of_users_trans[key][i][2], 6))
                elif list_of_users_trans[key][i][3] == key:
                    list_quantity_seller.append(round(list_of_users_trans[key][i][1], 6))
                    list_price_seller.append(round(list_of_users_trans[key][i][2], 6))

            while key in list_of_byers:
                list_of_byers.remove(key)

            key11 = ' ' + key + ' '

            while key11 in list_of_sellers:
                list_of_sellers.remove(key11)

            list_sort_quantity_buy = dict()
            for j in list_of_byers:
                list_sort_quantity_buy[j] = 0

            list_sort_price_buy = dict()
            for j in list_of_byers:
                list_sort_price_buy[j] = 0

            for i in range(0, len(list_of_byers)):
                key_ = list_of_byers[i]
                quantity = list_quantity_buyer[i]
                price = list_price_buyer[i]
                list_sort_quantity_buy[key_] = list_sort_quantity_buy[key_] + quantity
                list_sort_price_buy[key_] = list_sort_price_buy[key_] + (price * quantity)

            list_sort_quantity_buy[key] = 0
            list_sort_price_buy[key] = 0

            list_sort_quantity_sell = dict()
            for j in list_of_sellers:
                list_sort_quantity_sell[j] = 0

            list_sort_price_sell = dict()
            for j in list_of_sellers:
                list_sort_price_sell[j] = 0

            for i in range(0, len(list_of_sellers)):
                key__ = list_of_sellers[i]
                quantity = list_quantity_seller[i]
                price = list_price_seller[i]
                list_sort_quantity_sell[key__] = list_sort_quantity_sell[key__] + quantity
                list_sort_price_sell[key__] = list_sort_price_sell[key__] + (price * quantity)

            list_sort_price_sell[key] = 0
            list_sort_quantity_sell[key] = 0

            quantity_dict = list_sort_quantity_sell.copy()  # start with keys and values of x
            quantity_dict.update(list_sort_quantity_buy)  # modifies z with keys and values of y

            price_dict = list_sort_price_sell.copy()
            price_dict.update(list_sort_price_buy)

            nodes_buyers = list(dict.fromkeys(list_of_byers))
            nodes_sellers = list(dict.fromkeys(list_of_sellers))

            merged_list_sell = [(key, nodes_buyers[i]) for i in range(0, len(nodes_buyers))]
            merged_list_buy = [(nodes_sellers[i], key) for i in range(0, len(nodes_sellers))]

            G = nx.DiGraph()

            G.add_edges_from(merged_list_buy)
            G.add_edges_from(merged_list_sell)

            elarge = G.edges

            fixed_positions = {}

            if len(nodes_buyers) == 0:
                len_max_nodes = len(nodes_sellers)
            elif len(nodes_sellers) == 0:
                len_max_nodes = len(nodes_buyers)
            elif (len(nodes_sellers) > 0 & len(nodes_buyers)) > 0:
                len_max_nodes = max(len(nodes_buyers), len(nodes_sellers))

            fixed_positions[str(key)] = (len_max_nodes / 2, 0)

            for i in range(0, len(nodes_buyers)):
                fixed_positions[str(nodes_buyers[i])] = (i, -2)
            for j in range(0, len(nodes_sellers)):
                fixed_positions[str(nodes_sellers[j])] = (j, 2)

            fixed_nodes = fixed_positions.keys()

            pos = nx.spring_layout(G, pos=fixed_positions, fixed=fixed_nodes)

            Xn = [pos[k][0] for k in pos]
            Yn = [pos[k][1] for k in pos]
            labels = [k for k in pos]

            list_quantity = []

            for i in range(0, len(labels)):
                for key1 in quantity_dict.keys():
                    if key1 == labels[i]:
                        list_quantity.append(str(round(quantity_dict[key1], 6)) + ' Wh')
                    else:
                        None

            list_price = []
            for i in range(0, len(labels)):
                for key2 in price_dict.keys():
                    if key2 == labels[i]:
                        list_price.append(str(round(price_dict[key2], 6)) + ' EUR')
                    else:
                        None

            labels_node = []
            for i in range(0, len(list_price)):
                labels_node.append(list_quantity[i] + ',   ' + list_price[i])

            nodes = dict(type='scatter',
                         x=Xn,
                         y=Yn,
                         mode='markers+text',
                         hovertext=labels_node,
                         marker=dict(size=40, color='#A9F5A9'),
                         textfont=dict(size=18, color='#000000'),
                         text=labels,
                         hoverinfo='text')

            Xaxis = dict(showline=False, zeroline=False, showgrid=False, showticklabels=True,
                         mirror='allticks', ticks='inside', ticklen=5, tickfont=dict(size=14),
                         title='')

            Yaxis = dict(showline=False, zeroline=False, showgrid=False, showticklabels=True,
                         mirror='allticks', ticks='inside', ticklen=5, tickfont=dict(size=14),
                         title='')


            annotateELarge = [
                dict(showarrow=True, arrowsize=0.7, arrowwidth=4, arrowhead=5, standoff=14, startstandoff=4,
                     ax=pos[arrow[0]][0], ay=pos[arrow[0]][1]-0.07, axref='x', ayref='y',
                     x=pos[arrow[1]][0], y=pos[arrow[1]][1]+0.07, xref='x', yref='y') for arrow in elarge]


            layout = dict(width=1200, height=500,
                          showlegend=False,
                          xaxis=Xaxis,
                          yaxis=Yaxis,
                          hovermode='closest',
                          plot_bgcolor='rgba(0,0,0,0)',
                          annotations=annotateELarge,
                          # arrows
                          )

            fig = go.Figure(data=[nodes], layout=layout)
            fig.update_xaxes(visible=False)
            fig.update_yaxes(visible=False)
            fig.layout.paper_bgcolor = 'rgba(0,0,0,0)'
            fig.update_layout(
                font_color="white",
                title_font_color="white",
                legend_title_font_color="white",
                # arrowcolor="red",
                margin={
                    "r": 150,
                    "t": 20,
                    "b": 0,
                    "l": 150,
                }
            )
            fig.update_layout({'paper_bgcolor':'rgba(0,0,0,0)'})
            list_of_fig.append(fig)

        return list_of_fig

    def draw_demand_user(self, df_bids, user_names, spot_price, timesteps):

        list_user_net_load = []
        spot_price = spot_price
        spot_price = spot_price.reset_index()
        spot_price.rename(columns={'index': 'Date'}, inplace=True)
        spot_price['Date'] = pd.to_datetime(spot_price.Date).dt.tz_localize(None)

        start_ = spot_price[spot_price.Date == df_bids['time'].iloc[0]]
        start_index = start_.index[0]
        slutt_index = 96             #For 15 min intervals


        for i in user_names:
            df_bids_user = df_bids[df_bids['user'] == i]
            df_bids_user.loc[df_bids_user['buying'] == True, 'quantity'] = df_bids_user['quantity'] * -1
            fig = go.Figure([go.Scatter(x=df_bids_user['time'], y=df_bids_user['quantity'] , name='Net load, user: ' + i)])
            fig.update_layout({'paper_bgcolor':'rgba(0,0,0,0)'})

            list_user_net_load.append(fig)


        return list_user_net_load

    def draw_demand_user_with_P2P(self, df_bids, df_trans, user_names, timesteps):
        p2p_dict = df_trans
        p2p_dict_time = {}
        list_user_net_load_p2p = []

        for j in range(0, len(p2p_dict)):
            list_trans1 = []
            for i in range(0, len(p2p_dict[j])):
                list_trans1.append((*p2p_dict[j][i], (timesteps[j])))
            p2p_dict_time[j] = pd.DataFrame(list_trans1)

        df_trans_time = pd.concat(p2p_dict_time)
        df_trans_time = df_trans_time.set_axis(['seller', 'quantity', 'price', 'buyer','?', 'time'], axis=1, inplace=False)
        df_trans_time = df_trans_time[df_trans_time['quantity'] > 0]
        df_trans_time = df_trans_time.reset_index()
        del df_trans_time['level_0'], df_trans_time['level_1']
        df_trans_time['time'] = pd.to_datetime(df_trans_time['time'])


        list_of_seller_p2p = {}
        list_of_buyer_p2p = {}

        for i in user_names:
            df_trans_seller = df_trans_time[df_trans_time['seller']== i]
            df_trans_seller['time'] = pd.to_datetime(df_trans_seller['time'])
            df_trans_buyer = df_trans_time[df_trans_time['buyer']== i]
            list_of_seller_p2p[i] = df_trans_seller
            list_of_buyer_p2p[i] = df_trans_buyer
            df_bids_user = df_bids[df_bids['user'] == i]
            df_bids_user.loc[df_bids_user['buying'] == True, 'quantity'] = df_bids_user['quantity'] * -1
            df_trans_buyer1 = df_trans_buyer.groupby('time', as_index=False)['quantity'].sum()
            df_trans_seller1 = df_trans_seller.groupby('time', as_index=False)['quantity'].sum()
            df_p2p_user = df_bids_user.merge(df_trans_buyer1, left_on='time', right_on='time', suffixes=('bids', 'buy'),how='outer').merge(df_trans_seller1, left_on='time', right_on='time', suffixes=('buy', 'sell'),how='outer')
            df_p2p_user['quantitybuy'].replace(np.nan, 0, inplace=True)
            # df_p2p_user['pricebuy'].replace(np.nan, 0, inplace=True)
            df_p2p_user['quantity'].replace(np.nan, 0, inplace=True)
            # df_p2p_user['price'].replace(np.nan, 0, inplace=True)
            df_p2p_user['quantityP2P'] = df_p2p_user["quantitybids"] + df_p2p_user["quantitybuy"] - df_p2p_user["quantity"]


            fig = go.Figure([go.Scatter(x=df_p2p_user['time'], y=df_p2p_user['quantitybids'], name='Net import, user: ' + i)])
            fig.add_scatter(x=df_p2p_user['time'], y=df_p2p_user['quantityP2P'], name='Net import P2P, user: ' + i)
            fig.add_bar(x=df_p2p_user['time'], y=df_p2p_user["quantitybuy"] - df_p2p_user["quantity"], name='P2P sold/bought')
            fig.update_layout({'paper_bgcolor':'rgba(0,0,0,0)'})
            list_user_net_load_p2p.append(fig)

        return list_user_net_load_p2p


    def draw_table(self, df_bids, user_names, df_trans, spot_price, timesteps):

        list_user_table = []
        spot_price = spot_price
        spot_price = spot_price.reset_index()
        spot_price.rename(columns={'index': 'Date'}, inplace=True)
        spot_price.rename(columns={0: 'Spot_price'}, inplace=True)
        spot_price['Spot_price'] = spot_price['Spot_price']
        spot_price['Date'] = pd.to_datetime(spot_price.Date).dt.tz_localize(None)

        start_ = spot_price[spot_price.Date == df_bids['time'].iloc[0]]
        start_index = start_.index[0]
        slutt_index = 96                                #For 15 min intervals
        spot_price_time = spot_price.iloc[start_index:start_index+slutt_index]
        spot_price_time = spot_price_time.reset_index()
        del spot_price_time['index']


        ######## Trans
        p2p_dict = df_trans
        p2p_dict_time = {}
        list_user_net_load_p2p = []

        for j in range(0, len(p2p_dict)):
            list_trans1 = []
            for i in range(0, len(p2p_dict[j])):
                list_trans1.append((*p2p_dict[j][i], (timesteps[j])))
            p2p_dict_time[j] = pd.DataFrame(list_trans1)

        df_trans_time = pd.concat(p2p_dict_time)
        df_trans_time = df_trans_time.reset_index()
        del df_trans_time['level_0'], df_trans_time['level_1']
        df_trans_time = df_trans_time.set_axis(['seller', 'quantity', 'price', 'buyer', '?', 'time'], axis=1, inplace=False)
        df_trans_time = df_trans_time[df_trans_time['quantity']>0]
        df_trans_time['time'] = pd.to_datetime(df_trans_time['time'])
        for i in user_names:
            df_bids_user = df_bids[df_bids['user'] == i]
            df_bids_user.loc[df_bids_user['buying'] == True, 'quantity'] = df_bids_user['quantity'] * -1
            df_bids_user = df_bids_user.merge(spot_price_time, left_on='time', right_on='Date', how='outer')

            df_bids_user_profit = df_bids_user['quantity']*df_bids_user['price']


            # Payment

            df_bought = df_bids_user[df_bids_user['quantity']<=0]

            df_trans_user_time_buy = df_trans_time[df_trans_time['buyer'] == i]

            df_p2p_user_buy = df_bought.merge(df_trans_user_time_buy, left_on='time', right_on='time', suffixes=('', 'buy'), how='outer')
            df_p2p_user_buy['quantitybuy'].replace(np.nan, 0, inplace=True)
            df_p2p_user_buy['pricebuy'].replace(np.nan, 0, inplace=True)

            df_p2p_user_buy['quantitywithP2P'] = df_p2p_user_buy['quantity'] + df_p2p_user_buy['quantitybuy']
            df_p2p_user_buy['Total_payment_spot'] = df_p2p_user_buy['quantitywithP2P']* df_p2p_user_buy['Spot_price']
            df_p2p_user_buy['Total_payment_p2p'] = df_p2p_user_buy['quantitybuy'] * df_p2p_user_buy['pricebuy']
            df_p2p_user_buy['Total_payment'] = df_p2p_user_buy['Total_payment_spot'] + df_p2p_user_buy['Total_payment_p2p']



            # Income
            df_sold = df_bids_user[df_bids_user['quantity']>0]

            df_trans_user_time_sell = df_trans_time[df_trans_time['seller'] == i]

            df_p2p_user_sell = df_sold.merge(df_trans_user_time_sell, left_on='time', right_on='time', suffixes=('', 'sell'), how='outer')
            df_p2p_user_sell['quantitysell'].replace(np.nan, 0, inplace=True)
            df_p2p_user_sell['pricesell'].replace(np.nan, 0, inplace=True)

            df_p2p_user_sell['quantitywithP2P'] = df_p2p_user_sell['quantity'] + df_p2p_user_sell['quantitysell']
            df_p2p_user_sell['Total_payment_spot'] = df_p2p_user_sell['quantitywithP2P']* df_p2p_user_sell['Spot_price']
            df_p2p_user_sell['Total_payment_p2p'] = df_p2p_user_sell['quantitysell'] * df_p2p_user_sell['pricesell']
            df_p2p_user_sell['Total_payment'] = df_p2p_user_sell['Total_payment_spot'] + df_p2p_user_sell['Total_payment_p2p']

            # No P2P

            df_bids_user['Tot_profit_no_P2P'] = df_bids_user['quantity'] * df_bids_user['Spot_price']


            df_tot_sell = df_p2p_user_sell['Total_payment'].sum()
            df_tot_buy = df_p2p_user_buy['Total_payment'].sum()
            df_tot_profit = df_tot_sell + df_tot_buy
            df_p2p_sold = df_p2p_user_sell['Total_payment_p2p'].sum()
            df_p2p_buy = df_p2p_user_buy['Total_payment_p2p'].sum()
            df_no_p2p = df_bids_user['Tot_profit_no_P2P'].sum()

            df_table = pd.DataFrame([df_tot_buy, df_tot_sell, df_p2p_sold, df_p2p_buy, df_tot_profit, df_no_p2p])
            df_table = df_table.reset_index()
            df_table['index'] = ['Bought from grid', 'Sold to grid', 'P2P sold', 'P2P bought','Total profit', 'Total profit without P2P']
            df_table.rename(columns={0: 'Cost'}, inplace=True)
            df_table['Cost'] = round(df_table['Cost'],4)
            import plotly.express as px
            fig_bar = px.bar(df_table, x='index', y='Cost', title="Total profit for user: " + i, barmode='stack')
            fig_bar.update_layout(xaxis_title='', yaxis_title= 'EUR',)
            fig_bar.update_layout({'paper_bgcolor':'rgba(0,0,0,0)'})
            fig_bar.update_traces(hovertemplate='%{x}, <br>Profit/Cost: %{y} EUR') 
            list_user_table.append(fig_bar)
        return list_user_table

    def draw_table_bids(self, df_bids, user_names, spot_price, timesteps):

        list_user_table = []
        spot_price = spot_price
        spot_price = spot_price.reset_index()
        spot_price.rename(columns={'index': 'Date'}, inplace=True)
        spot_price.rename(columns={0: 'Spot_price'}, inplace=True)
        spot_price['Spot_price'] = spot_price['Spot_price']
        spot_price['Date'] = pd.to_datetime(spot_price.Date).dt.tz_localize(None)

        start_ = spot_price[spot_price.Date == df_bids['time'].iloc[0]]
        start_index = start_.index[0]
        slutt_index = 96                                #For 15 min intervals
        spot_price_time = spot_price.iloc[start_index:start_index+slutt_index]
        spot_price_time = spot_price_time.reset_index()
        del spot_price_time['index']

        for i in user_names:
            df_bids_user = df_bids[df_bids['user'] == i]
            df_bids_user.loc[df_bids_user['buying'] == True, 'quantity'] = df_bids_user['quantity'] * -1
            df_bids_user = df_bids_user.merge(spot_price_time, left_on='time', right_on='Date', how='outer')


            df_bids_bought = df_bids_user[df_bids_user['quantity']<0]
            df_bids_bought['total_payment'] = df_bids_bought['quantity']*df_bids_user['Spot_price']
            df_bids_sold = df_bids_user[df_bids_user['quantity']>0]
            df_bids_sold['total_income'] = df_bids_sold['quantity']*(df_bids_user['Spot_price'] * 0.7)
            df_bids_user_total_profit = df_bids_sold['total_income'].sum() + df_bids_bought['total_payment'].sum()

            df_table = pd.DataFrame([df_bids_user_total_profit, df_bids_bought['total_payment'].sum(), df_bids_sold['total_income'].sum()])
            df_table = df_table.reset_index()
            df_table['index'] = ['Total Profit', 'Total bought', 'Total sold']
            df_table.rename(columns={0: 'Cost'}, inplace=True)
            df_table['Cost'] = round(df_table['Cost'],4)
            import plotly.express as px
            fig_bar = px.bar(df_table, x='index', y='Cost', title="Total profit for user: " + i)
            fig_bar.update_layout(yaxis_title= 'EUR', xaxis_title = "")
            fig_bar.update_layout({'paper_bgcolor':'rgba(0,0,0,0)'})
            fig_bar.update_traces(hovertemplate='%{x}, <br>Profit/Cost: %{y} EUR') 
            list_user_table.append(fig_bar)
        return list_user_table

    def txt_austria(self):
        text_file = 'Hello people'

        return text_file

    def draw_empty(self, user_names):

        list_empty = []
        for i in user_names:
            import plotly.graph_objects as go

            import plotly.io as pio
            # pio.renderers.default = 'svg'
            pio.renderers.default = 'browser'

            x = ['']
            y = [20]

            fig = go.Figure(data=[go.Bar(
                x=x, y=y,
                textfont=dict(
                    family="sans serif",
                    size=18,
                    color="rgba(0,0,0,0)"
                )
            )])
            fig.update_traces(marker_color='rgba(0,0,0,0)', marker_line_color='rgba(0,0,0,0)',
                              marker_line_width=0, opacity=0)

            fig.update_layout(
                {'paper_bgcolor': 'rgba(0,0,0,0)', "plot_bgcolor": "rgba(0,0,0,0)", "width": 10, "height": 10})
            fig.update_yaxes(visible=False, showticklabels=False)
            # fig.show()
            list_empty.append(fig)

        return list_empty
    
    #%% Text for the webpage 
    
    
    def txt_demand_user(self):

        P2P_fig_text = str("The line chart below showing the net import/export for each user. If the blue line is zero or below on the y-axis the user has to buy power. \
                           Due to it is no transactions in the P2P market at the current time all the demand is covered by buying power from the grid.")

        return P2P_fig_text
    
    def txt_demand_user_with_P2P(self):

        P2P_fig_text = str("The line chart below is showing the net import/export for each user. \
                           The blue line is showing the net load, if net load is positive the user is producing more than it is consuming. \
                           The red line is showing net import/export with P2P market included. Note that the red and blue line might be overlapping \
                           at some timestep, you therefore need to hide one of the lines to see the other. This can be done by clicking on the marker to the right of the figure. \
                           The green bar is showing the amount each user are buying or selling to the P2P market. Hold the pointer over the bar to see the amount \
                           and time the user are selling. Negative value indicate that the user is selling and positive value indicate that the user is buying. ")

        return P2P_fig_text
    
    
    def txt_table_bids(self):
    
    
    
        fig_bar_text = str("The bar chart is showing costs and profit for each user. The slider can be used to decide which user you want to investigate. \
        If the total profit bar is negative the user is buying for more money than what it is selling for. Since it is no transactions in the P2P market \
            will all the deficit demand be covered by buying from the grid.")
        
        return fig_bar_text
    
    def txt_table_bids_with_P2P(self):
    
    
    
        fig_bar_text = str("The bar chart is showing profit and costs for each user. Use the slider to decide which user you want to investigate. \
        If the total profit bar is negative the user is buying for more money than what it is selling for. Since it is transactions in the market will some users \
        buy from or sell to the P2P market. An overview of each user in the P2P market can be found by looking at the bars for the P2P market. ")
        
        return fig_bar_text
    
    
    
    def txt_notransp2p(self):

        nop2ptransactions = str("")

        return nop2ptransactions 
    
    def txt_notransp2pH5(self):

        nop2ptransactionsH5 = str("")

        return nop2ptransactionsH5
    
    def txt_H5trading(self):

        H5trading = str("Trading overview")

        return H5trading
    
    def txt_nxplot(self):

        nx_text = str("The network plot below is showing the user have traded with in the P2P market during the day. \
                                Hold your pointer over the different nodes to see the amount you are trading with \
                                the other participants.")

        return nx_text
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    