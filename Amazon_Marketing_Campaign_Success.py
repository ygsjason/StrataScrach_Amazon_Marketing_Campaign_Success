# Import your libraries
import pandas as pd

# Start writing code
df1 = marketing_campaign.drop_duplicates()

df2 = df1.sort_values(['user_id', 'created_at'])
df3 = df2.drop_duplicates(subset = ['user_id', 'created_at', 'product_id'])

##--find the users who make multiple purchases on the same day and no more additional purchase after that multiple-purchase date, then remove them
# group by id and date, then caculate the n of prc >1 on same day (using size() as two col. grouped)
df4 = df3.groupby(['user_id','created_at']).size().reset_index(name = 'n_prc_dy').query('n_prc_dy > 1')

#go back to raw (d3) to filter ids in df4, then group by id and date, then caculate the n of prc on same day
df5 = df3[df3.user_id.isin(df4.user_id)]
df6 = df5.groupby(['user_id', 'created_at']).size().reset_index(name='n_prc_dy')

#find the count of dates in df6 is equal to 1, which means these customers never came back after initial purchase
df7 = df6.groupby('user_id')['created_at'].count().reset_index(name = 'prc_dt_ctn').query('prc_dt_ctn == 1')
#inspect id in d3 with n_prc_same_product >1, confirm to filter out
df12 = df3[df3.user_id.isin(df7.user_id)]

##--find the user make only the same purchases over time, remove them
#group by id and product, count the n of purchases for same product
df8 = df3.groupby(['user_id','product_id'])['created_at'].count().reset_index(name = 'n_prc_same_product').query('n_prc_same_product > 1')
#inspect id in d3 with n_prc_same_product >1, confirm to filter out
df3[df3.user_id.isin(df8.user_id)]
df8
##--find the users who make single purchase on the same day and no more additional purchase after that single-purchase date
#group by id and dt, count n of prc on that dy = 1 (single purchase on that day)
#df9 = df3.groupby(['user_id','created_at']).size().reset_index(name = 'n_prc_dy')
#group by id, cont n of active dy = 1, which means these customers never came back after initial purchase
df10 = df3.groupby('user_id')['created_at'].count().reset_index(name = "n_active_dy").query('n_active_dy ==1')
#inspect those ids in d3 with single purchase
df11 = df3[df3.user_id.isin(df10.user_id)]
df11



#apply 3 filters (the user_id in df7, df8 and d11) on raw(d3) based on the creterias
df12 = df3[~df3.user_id.isin(df7.user_id)]

df13 = df12[~df12.user_id.isin(df8.user_id)]

df14 = df13[~df13.user_id.isin(df11.user_id)]

df14.user_id.unique()
df8

df3['d_rank1'] = df3.groupby(['user_id', 'product_id'])['created_at'].rank('dense')

df5

marketing_campaign['many_visit']=marketing_campaign.groupby("user_id")["created_at"].rank("dense")
r1 = marketing_campaign.groupby("user_id")["created_at"].rank("dense")>1
##products purchased for the first time will have a rank==1
marketing_campaign['first_visit']=marketing_campaign.groupby(["user_id" ,"product_id"])["created_at"].rank("dense")
r2 = marketing_campaign.groupby(["user_id" ,"product_id"])["created_at"].rank("dense") == 1
marketing_campaign[r1][r2]
marketing_campaign

#marketing_campaign[ranking1>1][ranking2==1]["user_id"].unique()
#df10.user_id.nunique()

#df3
#df6 = df5[~df5.user_id.isin(df4.user_id)]

#df2
#or
#df_drop = pd.concat([df3.user_id, df4.user_id])
#df6 = df2[~df2.user_id.isin(df_drop.to_frame().user_id)]

# find the user_id that made additional in-app purchase due to the success of marketing campaign
#df6.groupby('user_id')['product_id'].diff().reset_index()

#(any visit after the first will have a rank>1)
