import streamlit as st
import pandas as pd
import kys
from googleapiclient.discovery import build
import globalsearchv1

st.set_page_config(page_title='Youtube challenge', page_icon='ytub.png')
from sqlalchemy import create_engine
my_conn = kys.my_conn
key = kys.yt
youtube=build('youtube','v3',developerKey=key)
client = kys.client
mydb = client['ineuron']
mycol = mydb['ytscrapev1']

st.title('Video comments')

# Converting links to html tags
def path_to_image_html(path):
        return '<img src="' + path + '" width="60" >'

@st.cache
def convert_df(input_df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return input_df.to_html(escape=False, formatters=dict(Thumbnail=path_to_image_html))


title1=st.text_input('Enter the Youtube Video URL ')


if st.button('SEARCH'):
    # query = f"select authorProfileImageUrl,authorDisplayName, textDisplay from video_comments where videoId='{title}'"
    title = title1.split('=')[1]

    df_uni_video_details = globalsearchv1.get_video_details_uni(youtube, title)
    # df2 = df2[['Thumbnail', 'Name', 'Comments']]
    html = convert_df(df_uni_video_details)

    st.markdown(
        html,
        unsafe_allow_html=True
        )
    st.markdown ("COMMENTS")

    df_uni_video_comments=globalsearchv1.get_uni_video_comments(youtube, title)

    df_uni_video_comments=df_uni_video_comments.rename(columns = {'authorProfileImageUrl': 'Thumbnail','authorDisplayName': 'Name','textDisplay': 'Comments'}).reset_index()

    df_uni_video_comments=df_uni_video_comments[['Thumbnail','Name','Comments']]
    html = convert_df(df_uni_video_comments)

    st.markdown(
        html,
        unsafe_allow_html=True
        )

# Saving the dataframe as a webpage

    st.download_button(
         label="Download data as HTML",
        data=html,
        file_name='output.html',
        mime='text/html',
        )
