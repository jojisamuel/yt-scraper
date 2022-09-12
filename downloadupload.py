from __future__ import unicode_literals
import yt_dlp
import pandas as pd
import json
import requests
import kys

ydl_opts = {'format': 'best','outtmpl': '%(id)s.%(ext)s'}
headers = kys.headers
my_conn = kys.my_conn
client = kys.client


def downloader(video_id):
    url='https://www.youtube.com/watch?v='
    x=url+video_id
    print(x)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
     ydl.download([x])
     print('DOWNLOAD COMPLETE')

    filename = video_id + '.mp4'
    para = {}
    para['name'] = video_id
    para["parents"] = ["1l_6fwtEAaZbbc8Ci-SmElD3otV7dGgXh"]

    files = {
        'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
        'file': open(filename, "rb")
    }
    r = requests.post(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
        headers=headers,
        files=files
    )
    print('upload complete')
    return(r.json())

# query='SELECT videoId FROM `yt-proj`.video_ids'
# df_up=pd.read_sql(query,con=my_conn)
df_up=pd.read_csv('vid.csv')

for i in df_up['videoId'].tolist():
    print(i)
    df_up = downloader(i)
    df_upgdrive = pd.DataFrame([df_up])
    print(df_upgdrive)
    df_upgdrive.to_sql(con=my_conn, name='video_gdrive', if_exists='append', index=False)
    print('Entry Done')
# df=pd.read_csv('videos_details3.csv')
# video_id=df['video_id'][0]
# print(video_id)
# df_up=downloader(video_id)
# print(df_up)
# type(df_up)
# d11=pd.DataFrame([df_up])
# print(d11)
# d11.to_sql(con=my_conn,name='video_gdrive1',if_exists='append', index=False)
# query = "select * from video_details"
# table_df = pd.read_sql(query,con=my_conn)
# print(table_df.head())