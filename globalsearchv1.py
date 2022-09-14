from googleapiclient.discovery import build
import pandas as pd
import kys

key = kys.yt
youtube=build('youtube','v3',developerKey=key)

api_service_name = "youtube"
api_version = "v3"

# Get credentials and create an API client
youtube = build(api_service_name, api_version, developerKey=key)

def get_video_details_uni(youtube, v_id):

    request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=v_id
        )
    response = request.execute()
    data = {
        'Thumbnail':response['items'][0]['snippet']['thumbnails']['high']['url'],
        # 'videoId': response['items'][0]['id'],
        'Owner':response['items'][0]['snippet']['channelTitle'],
        'Title':response['items'][0]['snippet']['title'],
        'View Count':response['items'][0]['statistics']['viewCount'],
        'Like Count':response['items'][0]['statistics']['likeCount'],
       'Comment Count':response['items'][0]['statistics']['commentCount']

       }

    return(pd.DataFrame([data]))


def get_uni_video_comments(youtube, video_ids):
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
            'publishedAt': item['snippet']['topLevelComment']['snippet']['publishedAt']}

        comment_data.append(data)

    return(pd.DataFrame(comment_data))
