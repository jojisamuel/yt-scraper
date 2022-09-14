import streamlit as st
import pandas as pd
import kys

st.set_page_config(page_title='Youtube challenge', page_icon='ytub.png')
from sqlalchemy import create_engine
my_conn = kys.my_conn

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


title1=st.text_input('Enter the Youtube Video URL (iNeuron)')


if st.button('SEARCH'):
    # query = f"select authorProfileImageUrl,authorDisplayName, textDisplay from video_comments where videoId='{title}'"
    title = title1.split('=')[1]
    query2 = f"select * from video_details where video_id='{title}'"
    df_video = pd.read_sql(query2, con=my_conn)
    df_video1 = df_video[['channelTitle', 'title', 'viewCount', 'likeCount']]
    st.dataframe(df_video1, width=None, height=None)

    df_video_comments = pd.DataFrame(list(mycol.find()))
    df_comments = df_video_comments[df_video_comments['videoId'] == title]

    df2=df_comments.rename(columns = {'authorProfileImageUrl': 'Thumbnail','authorDisplayName': 'Name','textDisplay': 'Comments'}).reset_index()

    df2=df2[['Thumbnail','Name','Comments']]
    html = convert_df(df2)

    # CSS to inject contained in a string
    hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """


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
