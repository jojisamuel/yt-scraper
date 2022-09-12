from googleapiclient.discovery import build
import pandas as pd
import requests
import gridfs
import kys


pd.options.display.width= None
pd.options.display.max_columns= None
pd.set_option('display.max_rows', 3000)
pd.set_option('display.max_columns', 3000)

my_conn = kys.my_conn
client = kys.client
mydb = client['ineuron']
mycol = mydb['ytscrapev1']

key = kys.yt
channel_users=['krishnaik06','javaboynavin','saurabhexponent1','HiteshChoudharydotcom']
channel_ids=['UCXgGY0wkgOzynnHvSEVmE3A',  #hitesh
            'UCNU_lfiiWBdtULKOw6X0Dig',  #krish
            'UC59K-uG2A5ogwIrHw4bmlEg', #tolesu
            'UCkGS_3D0HEzfflFnG0bD24A'] #saurab

youtube=build('youtube','v3',developerKey=key)

def get_channel_stats(youtube, channel_ids):

    """ Channel STATISTICS"""

    all_data = []

    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=','.join(channel_ids)
    )
    response = request.execute()

    # loop through items
    for item in response['items']:
        data = {'channelName': item['snippet']['title'],
                'subscribers': item['statistics']['subscriberCount'],
                'views': item['statistics']['viewCount'],
                'totalVideos': item['statistics']['videoCount'],
                'playlistId': item['contentDetails']['relatedPlaylists']['uploads']
                }

        all_data.append(data)

    return (pd.DataFrame(all_data))

def get_video_ids(youtube, playlist_id):

    """Get all the videos"""

    vid_all_data = []
    v2 = []
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=playlist_id,
        maxResults=50)
    response = request.execute()
    fs = gridfs.GridFS(mydb)
    # loop through items
    for item in response['items']:
        data = {'channelId': item['snippet']['channelId'],
                'videoId': item['contentDetails']['videoId'],
                'title': item['snippet']['title'],
                'thumbnails': item['snippet']['thumbnails']['default']['url'],
                'videoOwnerChannelTitle': item['snippet']['videoOwnerChannelTitle'],
                'videoOwnerChannelId': item['snippet']['videoOwnerChannelId'],
                'playlistId': item['snippet']['playlistId']
                }
        name = data['videoId']
        img_url = data['thumbnails']
        image_content = requests.get(img_url).content
        fs.put(image_content, filename=name)

        vid_all_data.append(data)

    return (vid_all_data)


def get_video_details(youtube, video_ids):

    """ Video stats of each videos """

    all_video_info = []

    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=','.join(video_ids[i:i + 50])
        )
        response = request.execute()

        for video in response['items']:
            stats_to_keep = {'snippet': ['channelId', 'channelTitle', 'title', 'publishedAt'],
                             'statistics': ['viewCount', 'likeCount', 'commentCount']
                             }
            video_info = {}
            video_info['video_id'] = video['id']

            for k in stats_to_keep.keys():
                for v in stats_to_keep[k]:
                    try:
                        video_info[v] = video[k][v]
                    except:
                        video_info[v] = None

            all_video_info.append(video_info)

    return pd.DataFrame(all_video_info)

def get_video_comments(youtube, video_ids):

    """ Video Comments"""
    comment_data = []
    request = youtube.commentThreads().list(
        part="snippet,replies",
        videoId=video_ids,maxResults=50

    )
    response = request.execute()

    for item in response['items']:
        data = {'videoId': item['snippet']['videoId'],
            'textDisplay': item['snippet']['topLevelComment']['snippet']['textDisplay'],
            'authorDisplayName': item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
            'authorProfileImageUrl': item['snippet']['topLevelComment']['snippet']['authorProfileImageUrl'],
            'authorProfileId': item['snippet']['topLevelComment']['snippet']['authorChannelId']['value'],
            'publishedAt': item['snippet']['topLevelComment']['snippet']['publishedAt']}

        comment_data.append(data)

    return(pd.DataFrame(comment_data))


#######
df_channel_stats = get_channel_stats(youtube, channel_ids)
df_channel_stats.to_sql(con=my_conn,name='channel_stats',if_exists='append', index=False)
######

vid_all_data=[]
for i in df_channel_stats['playlistId'].tolist():
    video_ids = get_video_ids(youtube, i)
    vid_all_data.append(video_ids)


df_vid_all_data = pd.DataFrame()
for i in vid_all_data:
    temp_df = pd.DataFrame.from_dict(i)
    df_vid_all_data = pd.concat([df_vid_all_data, temp_df])
df_vid_all_data.to_sql(con=my_conn,name='video_ids',if_exists='append', index=False)
###########

video_ids=df_vid_all_data['videoId'].tolist()

df_get_video_details = get_video_details(youtube, video_ids)



df_get_video_details.to_sql(con=my_conn,name='video_details',if_exists='append', index=False)

#######
c_vid_all_data=[]
for i in df_get_video_details['video_id'].tolist():
    v_comments = get_video_comments(youtube, i)
    c_vid_all_data.append(v_comments)


df_c_vid_all_data = pd.DataFrame()
for i in c_vid_all_data:
    temp_df = pd.DataFrame.from_dict(i)
    df_c_vid_all_data = pd.concat([df_c_vid_all_data, temp_df])

# df_c_vid_all_data.to_sql(con=my_conn,name='video_comments',if_exists='append', index=False)
# df_c_vid_all_data.reset_index(inplace=True)
#
comment_data_dict = df_c_vid_all_data.to_dict("records")# Insert collection
mycol.insert_many(comment_data_dict)
