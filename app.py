import streamlit as st
import preprocessor, helper

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    st.write("File successfully uploaded.")

    df = preprocessor.preprocess(data)
    st.dataframe(df)

    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show Analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_message, num_image_message, num_video_message, num_non_media_messages,num_links = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

            st.header("Messages (No Media)")
            st.title(num_non_media_messages)

        with col3:
            st.header("Total Media Shared")
            st.title(num_media_message)

            st.header("Videos Shared")
            st.title(num_video_message)

            st.header("Images Shared")
            st.title(num_image_message)

        with col4:
            st.header("Link Shared")
            st.title(num_links)