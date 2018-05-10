"""
Spyder Editor

This is a temporary script file.
"""



import requests
import pandas as pd
import csv
import time
import json
import sys
import imp
import sys
import os

print('start..')
print (requests)
print(dir(requests))

# Create some GLOBAL varaiables so that you don't have to change these in each function.
# Note that in general, global variables are not a great software engineering practice but
# for "quick and dirty" code like this it can make your life simpler.
access_token = ('Bearer BQDxBlVWFc_OLS4AkxmcOEYo3oLicMR_OXMVHJwtYtzMDEACCCjpA9jZ6NIHd9tIwqdRccPvvGgrqJw_Qts')
#sleep_time = 0.3
sleep_time = 0.05

def main():
    os.chdir("/Users/sarahcouzens/Documents/project capstone")
    
#    queries = ['1995','1996','1997','1998','1999','2000','2001',
#              '2002','2003','2004','2005','2006','2007','2008',
#              '2009','2010','2011','2012','2013','2014','2015','2016','2017']
    queries = ['1994','1995']
    
    num_tracks = 10

    for query in queries:
            
            ltrack = []
            song_ids = []
            artist_ids = []
            album_ids = []
            
            audioF = []
            artist_data = []
            album_data = []
    
            
            col1 = [   'popularity',
                       'song_id',     'artist_id',     'album_id', 
                       'song_name',   'artist_name',   'album_name', 
                       'explicit',    'disc_number',   'track_number']
            
            
            col2 =  [  'song_id', 'uri',
                       'tempo', 'type',
                       'key', 'loudness',
                       'mode', 'speechiness',
                       'liveness', 'valence',
                       'danceability', 'energy',
                       'track_href', 'analysis_url',
                       'duration_ms', 'time_signature',
                       'acousticness', 'instrumentalness' ]
            
            col3 =  [  'artist_id',  'artist_genres',  'artist_popularity']
            
            col4 =  [  'album_id',  'album_genres',   'album_popularity',  'album_release_date']
            
            n = 0 
            idx = 0
            
            while idx < num_tracks:  
                
                API_search_request(query, 'track', 10, idx, ltrack, song_ids, artist_ids, album_ids)   
                
                n +=1
                
                print(('\n>> this is No '+ str(n) + ' search End '))
                idx += 10
                
# idx += 50 

                
                # Limit API requests to at most 3ish calls / second
                
                # YR - use global variable for sleep_time
                #time.sleep(0.05)   
                time.sleep(sleep_time)   
                
                print(len(song_ids))
                
                ## spotify API "search" option vs here track/audiofeature query
                
                for idx in range(0, len(song_ids), 1):
                    API_get_audio_feature(song_ids[idx: idx+1], audioF)
                    # YR - use global variable for sleep_time
                    #time.sleep(0.3)
                    time.sleep(sleep_time)
                
                for idx in range(0, len(artist_ids), 1):
                    API_get_artists(artist_ids[idx: idx+1], artist_data)
                    # YR - use global variable for sleep_time
                    #time.sleep(0.3)
                    time.sleep(sleep_time)
                
                for idx in range(0, len(album_ids), 1):
                    API_get_albums(album_ids[idx: idx+1], album_data)
                    # YR - use global variable for sleep_time
                    #time.sleep(0.3)
                    time.sleep(sleep_time)
                
                
                df1 = pd.DataFrame(ltrack, columns=col1)
                
                df2 = pd.DataFrame(audioF, columns=col2) 
                
                
                df3 = pd.DataFrame(artist_data, columns=col3)
                
                df4 = pd.DataFrame(album_data, columns=col4)
                
                df = df1.merge(df2, on='song_id', how='outer').merge(df3, on='artist_id', how='outer').merge(
                     df4, on='album_id', how='outer')

                # YR
                #
                # Break up the merges done on the previous line into separate
                # merges. We can then create a separate file with the 
                # results of each step of the merge to analyze what 
                # is happening.
                dfMerge1 = df1.merge(df2, on='song_id', how='outer')
                dfMerge2 = dfMerge1.merge(df3, on='artist_id', how='outer')
                dfMerge3 = dfMerge2.merge(df4, on='album_id', how='outer')
                
                filename = "_" + query + '.csv'                      
                
                # YR 
                #
                # You can change \t (i.e. tab) to "," to get csv - HOWEVER this 
                # is NOT a good idea since title names may have commas in them.
                # Therefore using a tab to separate the data is a much better
                # idea. You need to read this into R by using read.table
                # instead of read.csv. Read the R documentation for read.table
                # You set the separator to '\t' when calling read.table..
                df.to_csv(filename + '_all', sep='\t')

                #YR
                #
                # Let's create separate files to see all the parts of the data
                # that we generated above. This will allow us to understand
                # waht is going on. It turns out after looking at this data
                # that the ARTISTS and ALBUMS have no data (just headers)
                # This could be because the API didn't work correctly
                # or because there is no data on those albums and artists
                # in Spotify's database (probably not - probably something
                # wrong with the code)
                df1.to_csv('tracks' + filename, sep='\t')
                df2.to_csv('audio' + filename, sep='\t')
                df3.to_csv('artists' + filename, sep='\t')
                df4.to_csv('albums' + filename, sep='\t')
                dfMerge1.to_csv('merge1' + filename, sep='\t')
                dfMerge2.to_csv('merge2' + filename, sep='\t')
                dfMerge3.to_csv('merge3' + filename, sep='\t')
                
                print ('finish')
                
                print (query)
                
def API_search_request(keywords, search_type, results_limit, results_offset, ltrack, song_ids, artist_ids, album_ids):

    off = str(results_offset)
    lim = str(results_limit)

    url = 'https://api.spotify.com/v1/search?q=year:'+ keywords +'&type=' + search_type +'&offset='+ off +'&limit=' + lim
    
    # YR - use the global token found at the top of this file - that way you only have to change it in ONE place.
    #access_token = ('Bearer BQDxBlVWFc_OLS4AkxmcOEYo3oLicMR_OXMVHJwtYtzMDEACCCjpA9jZ6NIHd9tIwqdRccPvvGgrqJw_Qts')


    r = requests.get(url, headers={"Accept": "application/json" , "Authorization": access_token})

    if r: 
        j = r.json()
        print(j)
    else:
        return r


    litem = j['tracks']['items']
    #print(len(ll))
    try:
        for l in litem:
        
            if l['id'] not in song_ids:
                song_ids.append( l['id'] )

            if l['artists'][0]['id'] not in artist_ids:
                artist_ids.append( l['artists'][0]['id'] )

            if l['album']['id'] not in album_ids:
                album_ids.append(  l['album']['id'] )
        
        
            k =   [  l['popularity'],
        
                     l['id'], 
                     l['artists'][0]['id'],
                     l['album']['id'],

                     l['name'],
                     l['artists'][0]['name'],
                     l['album']['name'],

                     l['explicit'], 
                     l['disc_number'],
                     l['track_number']]
        
            ltrack.append(k)
    except:
        ValueError
      
   # f.close()
    #return j


def API_get_audio_feature(songids, audioF):
    
    #print(songids)
    #print '>> call art several'
    track_ids = ','.join(songids)

    url = 'https://api.spotify.com/v1/audio-features?ids=' + track_ids  
    ## access_token will expire soon
    # YR - use the global token found at the top of this file - that way you only have to change it in ONE place.
    #access_token = ('Bearer BQDxBlVWFc_OLS4AkxmcOEYo3oLicMR_OXMVHJwtYtzMDEACCCjpA9jZ6NIHd9tIwqdRccPvvGgrqJw_Qts')
    
    r = requests.get(url, headers={"Accept": "application/json" , "Authorization": access_token})
    
    if r:
        j = r.json()
    else:
        return r
    
    # print(j)
    ll = j['audio_features']

    try:

        for l in ll:
            k =  [  l['id'],l['uri'],
                    l['tempo'],l['type'],
                    l['key'],l['loudness'],
                    l['mode'],l['speechiness'],
                    l['liveness'],l['valence'],
                    l['danceability'],l['energy'],
                    l['track_href'],l['analysis_url'],
                    l['duration_ms'],l['time_signature'],
                    l['acousticness'],l['instrumentalness'] ]

            audioF.append(k)
        
    except:
        ValueError
    
        

    #return j

def API_get_artists(artist_ids, artist_data):

    art_ids = ','.join(artist_ids)

    url = 'https://api.spotify.com/v1/artists?ids=' + art_ids

    # YR 
    #
    # Your artists and albums data were blank since you didn't specify the authorization information
    # before trying to connect. I replaced the following line with the one below it. 
    #r = requests.get(url)

    # YR - add the authentication info to the request!!!
    r = requests.get(url, headers={"Accept": "application/json" , "Authorization": access_token})
    
    if r:
        j = r.json()
    else:
       #print 'for this specific art_ids, response reaches maximum, return'
        return r

    
    ll = j['artists']

    try:
        for l in ll:
        
            k = [  l['id'], 
                   l['genres'],
                   l['popularity'] ]

            artist_data.append(k)
    
    except:
        ValueError
    


def API_get_albums(album_ids, album_data):
   

    alb_ids = ','.join(album_ids)

    url = 'https://api.spotify.com/v1/albums?ids=' + alb_ids

    # YR 
    #
    # Your artists and albums data were blank since you didn't specify the authorization information
    # before trying to connect. I replaced the following line with the one below it. 
    #r = requests.get(url)

    # YR - add the authentication info to the request!!!
    r = requests.get(url, headers={"Accept": "application/json" , "Authorization": access_token})

    if r:
        j = r.json()
    else:
        return r


    ll = j['albums']
    
    try:
        for l in ll:
            k = [  l['id'], 
                   l['genres'],
                   l['popularity'],
                   l['release_date'] ]

            album_data.append(k)
    
    except:
        ValueError


if __name__ == '__main__':
    main()