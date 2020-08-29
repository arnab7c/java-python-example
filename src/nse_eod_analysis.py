import numpy as np
import pandas as pd
import os
import datetime

# set date
date_time_obj = datetime.date.today ()

date_str = '27-08-2020'
date_time_obj = datetime.datetime.strptime ( date_str, '%d-%m-%Y' )

str_date = date_time_obj.strftime ( "%d%m%y" )

# get yesterday
wkday = date_time_obj.weekday ()
if wkday == 0:
    yesterday = date_time_obj - datetime.timedelta ( days=3 )
elif wkday == 6:
    yesterday = date_time_obj - datetime.timedelta ( days=2 )
else:
    yesterday = date_time_obj - datetime.timedelta ( days=1 )

str_ydate = yesterday.strftime ( "%d%m%y" )

file_path = "/Users/arnab/Documents/data/NSE_Data/"

op_file_dir = os.path.join ( file_path, 'output/', str_date )
y_op_file_dir = os.path.join ( file_path, 'output/', str_ydate )

if os.path.isdir ( op_file_dir ):
    pass
else:
    try:
        os.mkdir ( op_file_dir )
    except OSError as error:
        print ( error )

    # read csv data
df = pd.read_csv ( file_path + "PR" + str_date + "/" + "Pd" + str_date + ".csv" )
# clean sheet with only EQ and take only required coulmns
clean_df = df[ df[ "SERIES" ] == 'EQ' ][
    [ 'SYMBOL', 'SECURITY', 'PREV_CL_PR', 'OPEN_PRICE', 'CLOSE_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'NET_TRDVAL',
      'NET_TRDQTY', 'TRADES', 'HI_52_WK', 'LO_52_WK' ] ]
# convert numerical columns
cols = clean_df.columns.drop ( [ 'SYMBOL', 'SECURITY' ] )
clean_df[ cols ] = clean_df[ cols ].apply ( pd.to_numeric, errors='coerce' )

# filter EQ which ended in +ve, copy slice in new dataframe
my_choice = clean_df[ (clean_df[ "CLOSE_PRICE" ] > clean_df[ "OPEN_PRICE" ]) ].copy ()
# Condition - number of trade instruction > 10,000
my_choice_trades = clean_df[
    (clean_df[ "TRADES" ] > 10000) & (clean_df[ "CLOSE_PRICE" ] > clean_df[ "OPEN_PRICE" ]) ].copy ()
# Condition - number of trade quanitity > 500,000
my_choice_trdqty = clean_df[
    (clean_df[ "NET_TRDQTY" ] > 500000) & (clean_df[ "CLOSE_PRICE" ] > clean_df[ "OPEN_PRICE" ]) ].copy ()
# Condition - number of trade value > 100,000,000
my_choice_trdval = clean_df[
    (clean_df[ "NET_TRDVAL" ] > 100000000) & (clean_df[ "CLOSE_PRICE" ] > clean_df[ "OPEN_PRICE" ]) ].copy ()

# calculate % price change
my_choice.loc[ :, 'PARCENTAGE' ] = my_choice.eval ( '((CLOSE_PRICE - OPEN_PRICE)/OPEN_PRICE)*100' )
my_choice[ 'PARCENTAGE' ] = my_choice[ 'PARCENTAGE' ].round ( 2 )
my_choice.to_csv ( op_file_dir + "/" + 'My_Choice_' + str_date + '.csv' )

my_choice_trades.loc[ :, 'PARCENTAGE' ] = my_choice_trades.eval ( '((CLOSE_PRICE - OPEN_PRICE)/OPEN_PRICE)*100' )
my_choice_trades[ 'PARCENTAGE' ] = my_choice_trades[ 'PARCENTAGE' ].round ( 2 )
my_choice_trades.to_csv ( op_file_dir + "/" + 'My_Choice_Trades' + str_date + '.csv' )

my_choice_trdqty.loc[ :, 'PARCENTAGE' ] = my_choice_trdqty.eval ( '((CLOSE_PRICE - OPEN_PRICE)/OPEN_PRICE)*100' )
my_choice_trdqty[ 'PARCENTAGE' ] = my_choice_trdqty[ 'PARCENTAGE' ].round ( 2 )
my_choice_trdqty.to_csv ( op_file_dir + "/" + 'My_Choice_TrdQty' + str_date + '.csv' )

my_choice_trdval.loc[ :, 'PARCENTAGE' ] = my_choice_trdval.eval ( '((CLOSE_PRICE - OPEN_PRICE)/OPEN_PRICE)*100' )
my_choice_trdval[ 'PARCENTAGE' ] = my_choice_trdval[ 'PARCENTAGE' ].round ( 2 )
my_choice_trdval.to_csv ( op_file_dir + "/" + 'My_Choice_TrdVal' + str_date + '.csv' )

# get top 10 stocks
top10 = my_choice.sort_values ( 'PARCENTAGE', ascending=False ).head ( 10 )
# arrange column position
top10_cols = top10.columns.to_list ()
top10_cols = top10_cols[ 0:2 ] + top10_cols[ -1: ] + top10_cols[ 2:12 ]
top10 = top10[ top10_cols ]
# copy data in csv file
top10.to_csv ( op_file_dir + "/" + 'Top_Stock-' + str_date + '.csv' )

# get top 10 stocks - Trades
top10_trades = my_choice_trades.sort_values ( 'PARCENTAGE', ascending=False ).head ( 10 )
# arrange column position
top10_cols = top10_trades.columns.to_list ()
top10_cols = top10_cols[ 0:2 ] + top10_cols[ -1: ] + top10_cols[ 2:12 ]
top10_trades = top10_trades[ top10_cols ]
# copy data in csv file
top10_trades.to_csv ( op_file_dir + "/" + 'Top_Stock_Trades-' + str_date + '.csv' )

# get top 10 stocks - Trades Quantity
top10_trdqty = my_choice_trdqty.sort_values ( 'PARCENTAGE', ascending=False ).head ( 10 )
# arrange column position
top10_cols = top10_trdqty.columns.to_list ()
top10_cols = top10_cols[ 0:2 ] + top10_cols[ -1: ] + top10_cols[ 2:12 ]
top10_trdqty = top10_trdqty[ top10_cols ]
# copy data in csv file
top10_trdqty.to_csv ( op_file_dir + "/" + 'Top_Stock_Trade_Qty-' + str_date + '.csv' )

# get top 10 stocks - Trades Values
top10_trdval = my_choice_trdval.sort_values ( 'PARCENTAGE', ascending=False ).head ( 10 )
# arrange column position
top10_cols = top10_trdval.columns.to_list ()
top10_cols = top10_cols[ 0:2 ] + top10_cols[ -1: ] + top10_cols[ 2:12 ]
top10_trdval = top10_trdval[ top10_cols ]
# copy data in csv file
top10_trdval.to_csv ( op_file_dir + "/" + 'Top_Stock_Trade_Val-' + str_date + '.csv' )

# combine all report in one file
top10_combo = pd.concat ( [ top10, top10_trades, top10_trdqty, top10_trdval ], axis=0 )
# sorting by SYMBOL
# top10_combo.sort_values("SYMBOL", inplace = True)

# dropping duplicte values
top10_combo.drop_duplicates ( subset="SYMBOL", keep='first', inplace=True )
# top10_combo.sort_values("PARCENTAGE",ascending=False)
top10_combo.to_csv ( op_file_dir + "/" + 'Top_Stock_Combo-' + str_date + '.csv' )

# read corporate action file - Dividend list
corp_df = pd.read_csv ( file_path + "PR" + str_date + "/" + "Bc" + str_date + ".csv" )
corp_clean = corp_df[ (corp_df[ "SERIES" ] == 'EQ') & (corp_df[ "PURPOSE" ].str.contains ( 'DIV' )) ].sort_values (
    "SYMBOL" )
corp_clean.to_csv ( op_file_dir + "/" + 'Dividend-' + str_date + '.csv' )

my_choice[ "SYMBOL" ].to_csv ( op_file_dir + "/Positive_Symbol.csv", header=None, index=None )

my_prev_choice = pd.read_csv ( y_op_file_dir + "/Increasing.csv", names=[ "SYMBOL" ] )
const_gain = pd.merge ( my_choice[ "SYMBOL" ], my_prev_choice[ "SYMBOL" ], how='inner' )
const_gain.to_csv ( op_file_dir + "/" + 'Increasing.csv' )
