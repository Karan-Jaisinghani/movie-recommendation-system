import streamlit as st
import pickle
import requests

def fetch(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=9aba8637298cf2db574d96a33c81ebbf'.format(movie_id))
    data = response.json()
    print(data)
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

sim = pickle.load(open("sim.pkl", "rb"))
movies = pickle.load(open("movies.pkl", "rb"))
def recommend(movie):
    index=movies[movies['title']==movie].index[0]
    sim1= sim[index]
    list1 = sorted(list(enumerate(sim1)),reverse=True,key=lambda x:x[1])[1:11]
    recommended_movies=[]
    recom_movie_poster = []
    id1 = []
    for i in list1:
        recommended_movies.append(movies.iloc[i[0]].title)
        recom_movie_poster.append(fetch(movies.iloc[i[0]].movie_id))
        id1.append(movies.iloc[i[0]].movie_id)
    return recommended_movies,recom_movie_poster,id1


movies_list1 = movies['title'].values
st.title("Movie Recommender System")
option = st.selectbox(
    "Select the movie you want your recommendations based on: ",movies_list1,)

st.write("You selected:", option)

if st.button("Recommend"):
    names, posters, ids = recommend(option)
    row1 = st.columns(5)
    row2 = st.columns(5)
    c = 0
    for col in row1 + row2:
        if c==11:
            break
        tile = col.container(height='content',width='stretch',border=True,horizontal=True,vertical_alignment='distribute')
        tile.text(names[c])
        tile.image(posters[c])
        c += 1
