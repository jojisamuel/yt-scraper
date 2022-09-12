import streamlit as st
import pandas as pd
import kys


my_conn = kys.my_conn


st.set_page_config(page_title='Youtube challenge', page_icon='ytub.png')

st.title('iNeuron YOUTUBE VIDEOS SEARCH ')
st.sidebar.success("select a page ")

# Converting links to html tags
def path_to_image_html(path):
        return '<img src="' + path + '" width="60" >'

@st.cache
def convert_df(input_df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return input_df.to_html(escape=False, formatters=dict(Thumbnail=path_to_image_html))

query = "select v_d.channelId,v_id.videoId, v_id.videoOwnerChannelTitle,concat('https://www.youtube.com/watch?v=',v_id.videoId) 'Video Link', concat('https://drive.google.com/file/d/',v_gd.id,'/view?usp=sharing') 'Download Link' , v_d.likeCount 'Likes', v_d.commentCount 'No Of Comments',v_d.title 'Title Of the Video', v_id.thumbnails 'Thumbnail' from `yt-proj`.video_details v_d inner join `yt-proj`.video_ids v_id on  v_d.video_id=v_id.videoId inner join `yt-proj`.video_gdrive v_gd on v_d.video_id=v_gd.name"
df_search = pd.read_sql(query,con=my_conn)

username=['Hitesh Choudhary','Krish Naik','MySirG.com','Telusko']
channel_id=['UCXgGY0wkgOzynnHvSEVmE3A','UCNU_lfiiWBdtULKOw6X0Dig','UCkGS_3D0HEzfflFnG0bD24A','UC59K-uG2A5ogwIrHw4bmlEg']
CHOICES= dict(zip(channel_id, username))
# CHOICES = {1: "dataset a", 2: "dataset b", 3: "dataset c"}
option = st.selectbox('Select option', CHOICES.keys(), format_func=lambda x:CHOICES[ x ])


if st.button('SEARCH'):
    df_result_search = df_search[df_search['channelId'] == option]
    df_result_search.rename(columns={'videoOwnerChannelTitle':'Name Of Youtuber'},inplace=True)
    style = df_result_search.reset_index()
    style = style[['Thumbnail','Title Of the Video','Name Of Youtuber','Video Link','Download Link','Likes','No Of Comments']]

    html = convert_df(style)
    st.markdown(
        html,
        unsafe_allow_html=True
    )

    st.download_button(
         label="Download data as HTML",
        data=style,
        file_name='output.html',
        mime='text/html',
        )