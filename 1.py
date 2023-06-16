import numpy as np
import pandas as pd

# 给用户u推荐n个电影
def ulikemtopN(u,n,movies,pulikemsortindex,links):
    title=[]
    genres=[]
    imdbid=[]
    tmdbid=[]
    movie=[]
    for i in range(n):
        title.append(movies.loc[pulikemsortindex[u][i],'title'])
        genres.append(movies.loc[pulikemsortindex[u][i], 'genres'])
        imdbid.append(links.loc[pulikemsortindex[u][i],'imdbId'])
        tmdbid.append(links.loc[pulikemsortindex[u][i],'tmdbId'])
        movie.append(title[i]+' '+genres[i]+' imdb:https://www.imdb.com/title/tt'+imdbid[i]+' tmdb:https://www.themoviedb.org/movie/'+tmdbid[i])
    return movie

movies=pd.read_csv('movies1.csv')
links=pd.read_csv('link1.csv',dtype=str)
pulikemsortindex=np.loadtxt('pulikemsortindex.csv',delimiter=',')
k=10
result = []
for i in range(len(pulikemsortindex)):
    result.append(ulikemtopN(i, k, movies, pulikemsortindex, links))
    print(result[i])
