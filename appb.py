import pickle
import streamlit as st
import numpy as np
import sklearn


def book_app():
    st.markdown("<h3 style='color: pink;'>Which Book's You are Looking for....</h3>", unsafe_allow_html=True)
    st.write("Enter your search query below to find recommended books.")

    model = pickle.load(open('artifacts/model.pkl', 'rb'))
    books_names = pickle.load(open('artifacts/books_names.pkl', 'rb'))
    df = pickle.load(open('artifacts/df.pkl', 'rb'))
    book_pivot = pickle.load(open('artifacts/books_pivot.pkl', 'rb'))

    def fetch_poster(suggestion):
        book_name = []
        ids_index = []
        poster_url = []

        for book_id in suggestion:
            book_name.append(book_pivot.index[book_id])
            
        for i in book_name[0]:
            ids = np.where(df['Title'] == i)[0][0]
            ids_index.append(ids)
            
        for id in ids_index:
            url = df.iloc[id]['URL']
            poster_url.append(url)
            
        return poster_url

    def recommend_books(book_name):
        book_list = []
        book_id = np.where(book_pivot.index == book_name)[0][0]
        distance, suggestion = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1, -1), n_neighbors = 6)

        poster_url = fetch_poster(suggestion)

        for i in range(len(suggestion)):
            books = book_pivot.index[suggestion[i]]
            for j in books:
                book_list.append(j)
                
        return book_list, poster_url



    selected_books = st.selectbox("Type or select a book", books_names)

    if st.button('Recommend', type="primary"):
        recommedation_books, poster_url = recommend_books(selected_books)
        col0, col1, col2, col3, col4, col5 = st.columns(6)

        with col0:
            st.text(recommedation_books[0])
            st.image(poster_url[0])

        with col1:
            st.text(recommedation_books[1])
            st.image(poster_url[1])
            
        with col2:
            st.text(recommedation_books[2])
            st.image(poster_url[2])
            
        with col3:
            st.text(recommedation_books[3])
            st.image(poster_url[3])
            
        with col4:
            st.text(recommedation_books[4])
            st.image(poster_url[4])
            
        with col5:
            st.text(recommedation_books[5])
            st.image(poster_url[5])