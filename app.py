import streamlit as st
import numpy as np
import pandas as pd

movies_df = pd.read_csv('working/movie_filterd_country.csv')
sig_kernel = np.load('working/sig_kernel.npy')
indices = pd.read_csv('working/movie_indices.csv')
country_code = pd.read_csv('working/country_codes.csv')

def recommend(title, sig_kernel=sig_kernel):

    idx = indices[indices['original_title'] == title].index[0]
    sig_scores = list(enumerate(sig_kernel[idx]))
    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)
    sig_scores = sig_scores[1:11]

    # Movie indices
    movie_indices = [i[0] for i in sig_scores]
    return movies_df[['original_title', 'popularity']].iloc[movie_indices].reset_index(drop=True)


st.title('Movie Recommender')

ctr = st.selectbox('Select Location', country_code['Country'])
cc = country_code[country_code['Country'] == ctr]['Code'].values[0]


if ctr:
    try:
        st.header(f'Recommended movies for {ctr} Users')
        st.dataframe(movies_df[movies_df[cc] == True][['original_title', 'vote_count', 'vote_average', 'score']].head(10))
    except ValueError:
        st.error('Invalid input. Please enter numbers separated by commas.')

selected_option = st.selectbox('Select a Movie:', indices)


if selected_option:
    try:
        st.header(f'Recommended movies for {selected_option}')
        df = recommend(selected_option)
        st.dataframe(df.style.hide(axis="index"))

    except ValueError:
        st.error('Invalid input. Please enter numbers separated by commas.')
