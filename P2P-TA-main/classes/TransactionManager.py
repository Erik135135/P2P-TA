import pandas as pd
from collections import OrderedDict
import numpy as np
import random
from datetime import datetime, timedelta

class TransactionsManager(object):
    """
    An interaface to store and
    manage all transactions.
    Transactions are the minimal unit to represent
    the outcome of a market.

    Attributes
    -----------
    name_col: list of str
        Name of the columns to use in the dataframe
        returned.
    n_trans: int
        Number of transactions currently in the Manager
    trans: list of tuples
        List of the actual transactions available
    """

    name_col = ['bid', 'quantity', 'price', 'source', 'active']

    def __init__(self):
        """
        """
        self.n_trans = 0
        self.trans = []
        self.trans_dict = {}



    def add_transaction(self, bid, quantity, price, source, active):
        """Add a transaction to the transactions list

        Parameters
        ----------
        bid : int
            Unique identifier of the bid
        quantity : float
            transacted quantity
        price : float
            transacted price
        source : int
            Identifier of the second party in the trasaction,
            -1 if there is no clear second party, such as
            in a double auction.
        active :
            True` if the bid is still active after the
            transaction.

        Returns
        --------
        trans_id: int
            id of the added transaction, -1 if fails

        Examples
        ---------

        1
        """
        new_trans = (bid, quantity, price, source, active)
        self.trans.append(new_trans)
        self.n_trans += 1

        return self.trans

    def sort_timesteps(self, df, time_start, time_Stop, prec=5):
        l = []

        def datetime_range(start, end, delta):
            current = start
            while current < end:
                yield current
                current += delta

        # unique_user = np.unique(df['username'])

        # start_ = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        # end_ = datetime.now().replace(day=datetime.now().day+1,hour=0, minute=0, second=0, microsecond=0)

        # start_ = datetime.fromtimestamp(time_start)
        #
        # end_ = datetime.fromtimestamp(time_Stop)

        start_ = time_start

        end_ = time_Stop


        dts = [dt.strftime('%Y-%m-%d %H:%M:%S') for dt in
               datetime_range(start_, end_, timedelta(minutes=15))]

        for t in dts:
            df_new = df[df["time"] == t]
            l.append(df_new)
        #
        # for i in range(0, len(l)):
        #     if len(l[i].username) != len(set(l[i].username)):
        #         for j in range(0,len(unique_user)):
        #             if (l[i].username == unique_user[j]):


        return l, dts

    def p2p(self, bids,time_start,time_stop, p_coef=0.5, r=None):

        l, dts = self.sort_timesteps(bids, time_start, time_stop, prec=5)


        length_bids = len(l)
        t = 0
        list_trans_seller = []
        list_trans_seller1 =[]
        list_bids = []
        list_trans_buyer = []
        trans_buyer_dict = {}

        for t in range(0, length_bids):
            r = np.random.RandomState() if r is None else r
            buying = l[t][l[t].buying]
            selling = l[t][l[t].buying == False]
            bs_list = list(buying.user.values) + list(selling.user.values)
            Nb, Ns = buying.shape[0], selling.shape[0]

            quantities = list()
            prices = list()

            for user in bs_list:
                quantities.append(l[t][l[t].user==user].quantity.item())
                prices.append(l[t][l[t].user==user].price.item())


            inactive_buying = []
            inactive_selling = []

            # Enumerate all possible trades (By only allowing
            pairs = np.ones((Nb + Ns, Nb * Ns), dtype=bool)
            pairs_inv = []
            i = 0
            for b in buying.user:
                index_b = bs_list.index(b)
                for s in selling.user:
                    index_s = bs_list.index(s)
                    pairs[index_b, i] = False  # Row b has 0s whenever the pair involves b
                    pairs[index_s, i] = False  # Same for s
                    pairs_inv.append((index_b, index_s))
                    i += 1

            active = np.ones(Nb * Ns, dtype=bool)
            tmp_active = active.copy()
            general_trading_list = []
            # Loop while there is quantities to trade or not all
            # possibilities have been tried
            while sum(quantities) > 0 and tmp_active.sum() > 0:
                trading_list = []
                while tmp_active.sum() > 0:  # We can select a pair
                    where = np.where(tmp_active == 1)[0]
                    x = r.choice(where)
                    trade = pairs_inv[x]
                    active[x] = False  # Pair has already traded
                    trading_list.append(trade)
                    tmp_active &= pairs[trade[0], :]  # buyer and seller already used
                    tmp_active &= pairs[trade[1], :]

                general_trading_list.append(trading_list)

                for (b, s) in trading_list:
                    if prices[b] >= prices[s]:
                        q = min(quantities[b], quantities[s])
                        p = prices[b] * p_coef + (1 - p_coef) * prices[s]
                        trans_b = (b, q, p, s, (quantities[b] - q) >= 0)
                        trans_s = (bs_list[s], q, p, bs_list[b], (quantities[s] - q) > 0)
                        quantities[b] -= q
                        quantities[s] -= q
                    else:
                        trans_b = (b, 0, 0, s, True)
                        trans_s = (bs_list[s], 0, 0, bs_list[b], True)
                    # self.add_transaction(*trans_b)
                    self.add_transaction(*trans_s)
                    #trans_buyer_all, trans_buyer = self.add_transaction(*trans_s)
                    #list_trans_seller1.append(self.trans)
                    #trans_seller = self.add_transaction(*trans_s)

                bs_list_buyers = bs_list[:len(buying)]
                bs_list_sellers = bs_list[len(buying):]
                inactive_buying = [b for b in range(0,len(bs_list_buyers)) if quantities[b] == 0]
                inactive_selling = [s for s in range(len(bs_list_buyers),len(bs_list)) if quantities[s] == 0]


                tmp_active = active.copy()
                for inactive in inactive_buying + inactive_selling:
                    tmp_active &= pairs[inactive, :]

            trans_buyer_dict[t] = self.trans
            self.trans = []
            # trans_buyer_dict[t].update(list_trans_seller1)

            extra = {'trading_list': general_trading_list}
            # list_trans_buyer.append(trans_buyer)
            list_trans_seller.append(self.trans)

            list_bids.append(extra)
            self.list_transaction_seller = list_trans_seller

        return trans_buyer_dict, dts

        # return list_bids, l, list_trans_buyer, list_trans_seller


    def get_df_trans(self, p2p_dict, dts):
        list_of_trans = []
        for key in p2p_dict.keys():
            df_trans = pd.DataFrame(p2p_dict[key], columns=['Seller', 'Volume', 'Price', 'Buyer', 'More trades'])
            df_trans['datetime'] = dts[key]
            list_of_trans.append(df_trans)

        df_trans = pd.concat(list_of_trans)

        df_trans = df_trans.reset_index()

        del df_trans['index']

        return df_trans
