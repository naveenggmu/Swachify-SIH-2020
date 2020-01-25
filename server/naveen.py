import pandas as pd
import numpy as np
import os
import math


print("Start")

def centreFinder(in_max_lat,in_min_lat,in_max_long,in_min_long):
    # print(df.shape)
    df = pd.read_csv('/home/naveenggmu/Downloads/NASA data/VIIRS_98825/fire_archive_V1_98825.csv')
    df = df.drop(['instrument'],axis=1)
    df = df.loc[(df['latitude']>in_min_lat) & (df['latitude']<in_max_lat) & (df['longitude']>in_min_long) & (df['longitude']<in_max_long) & (df['type']==0)]
    df['acq_date'] = df['acq_date'].astype('datetime64[ns]')
    # print(df.shape)
    
    lat_max = df['latitude'].max()
    lat_min = df['latitude'].min()

    long_max = df['longitude'].max()
    long_min = df['longitude'].min()
    l_m = long_min

    dif_lat = lat_max - lat_min
    dif_long = long_max - long_min

    d_lat = dif_lat/8
    d_long = dif_long/8
    # print("Minimun longitude ",long_min,"Maximum longitude ",long_max, "Difference", dif_long, "Part ", d_long) 
    # print("Minimun latitude ",lat_min,"Maximum latitude ",lat_max, "Difference", dif_lat, "Part ", d_lat)
    df['locations'] = 0
    place = 1
    while(lat_min<lat_max):
    #     print("Latitude value ",lat_min)
        long_min = l_m
        while(long_min<long_max):
                df.loc[(df['latitude']>lat_min)&(df['latitude']<(lat_min+d_lat))
                      & (df['longitude']>long_min)&(df['longitude']<(long_min + d_long)),"locations"] = place
                place = place + 1
    #             print("Longitude value ",long_min)
                long_min = long_min + d_long

        lat_min = lat_min + d_lat       
    # print('Total Boxes ', place) 
    
    
    cof = []
    location_id =[]


    for i in range(1,df['locations'].max()+1):
        cof.append(df[df["locations"]==i].shape[0])

    for i in range(1,len(cof)+1):
        location_id.append(i)


    # print(len(location_id))
    # print(len(cof))

    # print(len(location_id))
    hm_df = pd.DataFrame()
    hm_df['location_id'] = location_id
    hm_df['cof'] = cof
#     hm_df
    
    
    max_lat_coords = []
    min_lat_coords = []
    max_long_coords = []
    min_long_coords = []
    avg_lat_coords = []
    avg_long_coords = []

    for index,rows in hm_df.iterrows():

            locat = rows['location_id']
            max_lat_coords.append(df.loc[df['locations']==locat]['latitude'].max())
            min_lat_coords.append(df.loc[df['locations']==locat]['latitude'].min())
            avg_lat = (df.loc[df['locations']==locat]['latitude'].max() +df.loc[df['locations']==locat]['latitude'].min())/2
            avg_lat_coords.append(avg_lat)

            max_long_coords.append(df.loc[df['locations']==locat]['longitude'].max())
            min_long_coords.append(df.loc[df['locations']==locat]['longitude'].min())
            avg_long = (df.loc[df['locations']==locat]['longitude'].max()+df.loc[df['locations']==locat]['longitude'].min() )/2
            avg_long_coords.append(avg_long)


    # print(len(max_lat_coords))
    # print(len(min_lat_coords))

    # print(len(max_long_coords))
    # print(len(min_long_coords))
    
    hm_df['max_lat'] = max_lat_coords 
    hm_df['min_lat'] = min_lat_coords
    hm_df['max_long'] =max_long_coords
    hm_df['min_long'] =min_long_coords
    hm_df['avg_lat']= avg_lat_coords
    hm_df['avg_long']=avg_long_coords
    
    
    
    # print(hm_df.shape)
    hm_df.dropna(inplace=True)
    # print(hm_df.shape)
    
    
    
    avgcof = hm_df['cof'].mean()
    hm_df = hm_df.loc[hm_df['cof']>(1.25 * avgcof)]
    # print(hm_df.shape)
    
    latss = hm_df['avg_lat'].tolist()
    longss = hm_df['avg_long'].tolist()
    
    coords = {
    "latss" : latss,
    "longss" : longss
    }
    
    return coords