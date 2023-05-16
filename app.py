import streamlit as st
import numpy as np
import pandas as pd
import pickle
similarity = pickle.load(open('artifacts/similarity.pkl','rb'))
final_ratings = pd.read_csv('artifacts/final_ratings.csv')
popular_books = pd.read_csv('artifacts/popular_books.csv')
book_pivot = pd.read_csv('artifacts/book_pivot.csv').set_index('title')

final_ratings = final_ratings[['title', 'author', 'year', 'Image-URL-M']]
popular_books = popular_books[['title', 'author', 'year', 'Image-URL-M','num_ratings','avg_rating']]


def recommend(book_name):
    """
    Recommends top related books based on a given book.

    Args:
        book_name (str): The name of the book.

    Returns:
        list: A list of recommended books, each represented as a list containing the title, author, year, and image URL.

    """
    index = np.where(book_pivot.index == book_name)[0][0]
    top_related_books = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[:6]
    recommended_books_index = [i[0] for i in top_related_books]
    recommended_books = [book_pivot.index[id] for id in recommended_books_index]
    
    books = []
    for book in recommended_books:
        idx = np.where(final_ratings.title == book)[0][0]
        books.append(final_ratings.iloc[idx].tolist())
   
    return books


def load_recommendation():

    book_list = book_pivot.index.tolist()
    selected_book = st.selectbox('Select any Book',book_list)
    btn = st.button('Find the Recommended Books')
    if btn:
        recommended_books = recommend(selected_book)

        cols = st.columns(6)

        for i in range(6):
            cols[i].image(recommended_books[i][3])
            #cols[i].write(f"<b>Title:</b> {recommended_books[i][0]}", unsafe_allow_html=True)
            cols[i].write(f"**{recommended_books[i][0]}**")  #title
            cols[i].write(f"({recommended_books[i][2]})") #year

            cols[i].write(f" by<br> **{recommended_books[i][1]}**", unsafe_allow_html=True)



def load_popular_books():
    popular_books_list = [popular_books.iloc[i].tolist() for i in popular_books.index]

    n = st.selectbox('Select the number of top books',[i for i in range(4,550,4)])
    
    if n > len(popular_books_list):
        st.write(f"**There are {len(popular_books_list)} top books shortlisted**")

    num_columns = 4
    num_rows = n // 4

    for row_index in range(num_rows):
        cols = st.columns(num_columns)

        for col_index, col in enumerate(cols):
            book_index = row_index * num_columns + col_index

            if book_index < len(popular_books_list):
                with col:
                    col.image(popular_books_list[book_index][3])
                    col.markdown(f"**{popular_books_list[book_index][0]}**")  # title
                    col.write(f"(Publication Year: {popular_books_list[book_index][2]})")  # year
                    col.markdown(f"Total Ratings: {popular_books_list[book_index][4]}")
                    col.write(f" by<br> **{popular_books_list[book_index][1]}**", unsafe_allow_html=True)
            else:
                break



st.title('Book Recommender System')
select_ops = st.selectbox('Select what you want',['Popular Books','Get Recommendation of books'])


if select_ops == 'Popular Books':
    st.header('Popular Books')
    load_popular_books()

else:
    st.header('Get Book Recommendation')
    load_recommendation()


