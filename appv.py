import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import webbrowser

# CSS to set a fixed width for buttons
button_style = """
    <style>
    .stButton>button {
        width: 350px;
        white-space: nowrap;
        text-wrap: wrap;
    }
    </style>
"""

def video_app():

    df = pd.read_csv('Sih_utube_video.csv')

    df['combined_text'] = df['Title'] + ' ' + df['Description'] + ' ' + df['Subject'] + ' ' + df['Language'] + df['Uploader'] + ' ' + df['Rating'].astype(str) + ' ' + df['Views'].astype(str) + ' ' + df['Class'].astype(str) + ' ' + df['KeyWords']
    df['combined_text'] = df['combined_text'].str.lower()

    tfidf_vectorizer = TfidfVectorizer(stop_words='english')

    tfidf_matrix = tfidf_vectorizer.fit_transform(df['combined_text'])

    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    def recommend_videos(search_query, cosine_sim=cosine_sim):
        query_vector = tfidf_vectorizer.transform([search_query])

        cosine_scores = linear_kernel(query_vector, tfidf_matrix)

        video_indices = cosine_scores.argsort()[0][::-1]

        recommended_videos = df.iloc[video_indices[:10]][['Title', 'URL']].values.tolist()

        return recommended_videos

    st.markdown("<h3 style='color: orange;'>Which Video's You are Looking for....</h3>", unsafe_allow_html=True)
    st.write("Enter your search query below to find recommended videos.")

    search_query = st.text_input("Enter your search query:")
    
    recommend_button = st.button("Recommend", type="primary")

    if recommend_button:
        if search_query:
            recommended_videos = recommend_videos(search_query)

            if recommended_videos:
                st.subheader("Recommended Videos:")
                st.markdown(button_style, unsafe_allow_html=True)  
                col1, col2 = st.columns(2)

                for i, (title, url) in enumerate(recommended_videos, start=1):
                    if i % 2 == 1:
                        column = col1
                    else:
                        column = col2
                    if column.button(title, key=f"button_{i}", on_click=lambda url=url: webbrowser.open_new_tab(url)):
                        column.write(f"You clicked on '{title}'. Opening the URL in your browser...")
            else:
                st.warning("No videos found matching your query. Please try a different search.")
        else:
            st.warning("Please enter a search query before clicking the 'Recommend' button.")

