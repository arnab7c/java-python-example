import numpy as np
import pandas as pd
# set date
import datetime
today=datetime.date.today()
yesterday = datetime.date.today()- datetime.timedelta(days=1)
str_date=yesterday.strftime("%d%m%y")
file_path="/Users/arnab/Documents/data/NSE_Data/"
# read csv data
df=pd.read_csv(file_path+"PR"+str_date+"/"+"Pd"+str_date+".csv")
# clean sheet with only EQ and take only required coulmns
clean_df=df[df["SERIES"]=='EQ'][['SYMBOL','SECURITY','PREV_CL_PR','OPEN_PRICE','CLOSE_PRICE','HIGH_PRICE','LOW_PRICE','NET_TRDVAL','NET_TRDQTY','TRADES','HI_52_WK','LO_52_WK']]
# convert numerical columns
cols=clean_df.columns.drop(['SYMBOL','SECURITY'])
clean_df[cols] = clean_df[cols].apply(pd.to_numeric,errors='coerce')
# filter EQ which ended in +ve, copy slice in new dataframe
#my_choice=clean_df[(clean_df["CLOSE_PRICE"] > clean_df["OPEN_PRICE"])].copy()
# Condition - number of trade instruction > 10,000
#my_choice=clean_df[(clean_df["TRADES"] > 10000) & (clean_df["CLOSE_PRICE"] > clean_df["OPEN_PRICE"])].copy()
# Condition - number of trade quanitity > 500,000
#my_choice=clean_df[(clean_df["NET_TRDQTY"] > 500000) & (clean_df["CLOSE_PRICE"] > clean_df["OPEN_PRICE"])].copy()
# Condition - number of trade value > 100,000,000
my_choice=clean_df[(clean_df["NET_TRDVAL"] > 100000000) & (clean_df["CLOSE_PRICE"] > clean_df["OPEN_PRICE"])].copy()
# calculate % price change
my_choice.loc[:,'PARCENTAGE'] = my_choice.eval('((CLOSE_PRICE - OPEN_PRICE)/OPEN_PRICE)*100')
my_choice['PARCENTAGE']=my_choice['PARCENTAGE'].round(2)
my_choice.to_csv('/Users/arnab/Documents/data/NSE_Data/output/'+'My_Choice_'+str_date+'.csv')
# get top 10 stocks
top10=my_choice.sort_values('PARCENTAGE',ascending=False).head(10)
# arrange column position
top10_cols=top10.columns.to_list()
top10_cols=top10_cols[0:2]+top10_cols[-1:]+top10_cols[2:12]
top10=top10[top10_cols]
# copy data in csv file
top10.to_csv(file_path+'output/'+'Top_Stock_'+str_date+'.csv')
# read corporate action file - Dividend list
corp_df=pd.read_csv(file_path+"PR"+str_date+"/"+"Bc"+str_date+".csv")
corp_clean=corp_df[(corp_df["SERIES"]=='EQ') & (corp_df["PURPOSE"].str.contains('DIV'))]
corp_clean.to_csv('/Users/arnab/Documents/data/NSE_Data/output/'+'Dividend_'+str_date+'.csv')
print(top10)