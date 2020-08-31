__version__ = '0.1'
__author__ = 'Arnab Chatterjee'

import numpy as np
import pandas as pd
import datetime as dt
import os


class DateVal:

    def __init__(self, date=dt.datetime.now().strftime('%d-%m-%Y')):
        self.date = dt.datetime.strptime ( date, '%d-%m-%Y' )

    def setToday(self):
        return self.date.strftime("%d%m%y")

    def setYesterDay(self):
        wkday = self.date.weekday ()
        if wkday == 0:
            yesterday = self.date - dt.timedelta ( days=3 )
        elif wkday == 6:
            yesterday = self.date - dt.timedelta ( days=2 )
        else:
            yesterday = self.date - dt.timedelta ( days=1 )

        yesterday: str = yesterday.strftime ( "%d%m%y" )

        return yesterday


class DataOperation:

    def __init__(self,today,yesterday):
        self.today=today
        self.yesterday=yesterday
        self.file_path = "/Users/arnab/Documents/data/NSE_Data/"

    def setDirectory(self):
        op_file_dir = os.path.join ( self.file_path, 'output/', self.today )
        if os.path.isdir ( op_file_dir ):
            pass
        else:
            try:
                os.mkdir ( op_file_dir )
            except OSError as error:
                print ( error )

    @property
    def getTodayOPDir(self) -> str:
        today_dir=os.path.join ( self.file_path, 'output/', self.today )
        return today_dir

    @property
    def getYesterdayOPDir(self) -> str:
        yesterday_dir=os.path.join ( self.file_path, 'output/', self.yesterday )
        return yesterday_dir

    def cleanPDDataFile(self):
        # read initial downloaded csv data
        init_df = pd.read_csv ( self.file_path + "PR" + self.today + "/" + "Pd" + self.today + ".csv" )

        # clean sheet with only EQ and take only required columns
        clean_df = init_df[ init_df[ "SERIES" ] == 'EQ' ][
            [ 'SYMBOL', 'SECURITY', 'PREV_CL_PR', 'OPEN_PRICE', 'CLOSE_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'NET_TRDVAL',
              'NET_TRDQTY', 'TRADES', 'HI_52_WK', 'LO_52_WK' ] ]

        # convert numerical columns
        cols = clean_df.columns.drop ( [ 'SYMBOL', 'SECURITY' ] )
        clean_df[ cols ] = clean_df[ cols ].apply ( pd.to_numeric, errors='coerce' )

        return clean_df

    def calculatePercentage(self, base_df,kind):
        self.setDirectory ()

        base_df.loc[ :, 'PERCENTAGE' ] = base_df.eval ( '((CLOSE_PRICE - OPEN_PRICE)/OPEN_PRICE)*100' )
        base_df[ 'PERCENTAGE' ] = base_df[ 'PERCENTAGE' ].round ( 2 )
        base_df.to_csv ( self.getTodayOPDir + "/" + 'My_Choice_' + kind + '-' + self.today + '.csv' )
        #return base_df

    def setTopStocks(self,base_df,kind):
        self.setDirectory ()
        self.calculatePercentage(base_df,kind)

        df=pd.read_csv(self.getTodayOPDir + "/" + 'My_Choice_' + kind + '-' + self.today + '.csv')
        top10_df = df.sort_values ( 'PERCENTAGE', ascending=False ).head ( 10 )
        # arrange column position
        top10_cols = top10_df.columns.to_list ()
        top10_cols = top10_cols[ 0:2 ] + top10_cols[ -1: ] + top10_cols[ 2:12 ]
        top10_df = top10_df[ top10_cols ]
        # copy data in csv file
        top10_df.to_csv ( self.getTodayOPDir + "/" + 'Top_Stock_' + kind + '-' + self.today + '.csv' )


# Main process start
dt_obj = DateVal ("26-08-2020")
curr_dt= dt_obj.setToday()
y_dt = dt_obj.setYesterDay ()

do = DataOperation(curr_dt,y_dt)
clean_pd_df=do.cleanPDDataFile()

# filter EQ which ended in +ve, copy slice in new dataframe
my_choice = clean_pd_df[ (clean_pd_df[ "CLOSE_PRICE" ] > clean_pd_df[ "OPEN_PRICE" ]) ].copy ()
# Condition - number of trade instruction > 10,000
my_choice_trades = clean_pd_df[
    (clean_pd_df[ "TRADES" ] > 10000) & (clean_pd_df[ "CLOSE_PRICE" ] > clean_pd_df[ "OPEN_PRICE" ]) ].copy ()
# Condition - number of trade quantity > 500,000
my_choice_trdqty = clean_pd_df[
    (clean_pd_df[ "NET_TRDQTY" ] > 500000) & (clean_pd_df[ "CLOSE_PRICE" ] > clean_pd_df[ "OPEN_PRICE" ]) ].copy ()
# Condition - number of trade value > 100,000,000
my_choice_trdval = clean_pd_df[
    (clean_pd_df[ "NET_TRDVAL" ] > 100000000) & (clean_pd_df[ "CLOSE_PRICE" ] > clean_pd_df[ "OPEN_PRICE" ]) ].copy ()

do.setTopStocks(my_choice,"ALL")
