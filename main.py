import numpy as np
import pandas as pd


# 用于将从data.csv文件读取的数据框df转换成用户-电影评分数组um并返回
def dftoarray(df):
    data = pd.pivot_table(df, index='userId', columns='movieId', values='rating')
    data = data.values
    dataum = np.nan_to_num(data)
    return dataum


# sim()方法用于计算两个用户的相似度值,用于simarray()函数调用
def sim(id1, id2, data):
    dot_product = np.dot(data[id1], data[id2])
    norm1 = np.linalg.norm(data[id1])
    norm2 = np.linalg.norm(data[id2])
    similarity = dot_product / (norm1 * norm2)
    return similarity


# simarray()函数通过循环调用sim()方法计算并返回每一个用户与其他用户的相似度数组simu
def simarray(um):
    simarray = np.zeros((len(um), len(um)))
    for i in range(len(um)):
        for j in range(len(um)):
            if i != j:
                simarray[i][j] = sim(i, j, um)
    return simarray


# pUlikem函数用于计算并返回每个用户对每个电影的感兴趣概率（程度）数组
def pUlikem(um, simusort, simusortindex, k):
    pulikem1 = np.zeros((len(um), len(um[0])))
    for u in range(len(um)):
        for m in range(len(um[0])):
            if um[u][m] == 0:
                for siu in range(k):
                    if m != siu:
                        pulikem1[u][m] += simusort[u][siu] * um[simusortindex[u][siu]][m]
    return pulikem1


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

# 从data.csv文件读取数据df,通过dftoarray()函数获得用户-电影评分数组um并保存到um.scv文件中
def getum(file):
    df = pd.read_csv(file)
    um = dftoarray(df)
    np.savetxt('um.csv', um, delimiter=',', fmt='%.1f')
    um1=np.loadtxt('um.csv',delimiter=',')
    return um1

# 通过simarray()函数从um数组获得用户相似度数组simu并保存到simu.csv文件中
def getsimu(um):
    simu = simarray(um)
    np.savetxt('simu.csv', simu, delimiter=',', fmt='%.4f')
    simu1=np.loadtxt('simu.csv',delimiter=',')
    return simu1

# 通过调用np.sort()从simu数组获得每一行降序排列后的数组simusort并保存到simusort.csv文件中
def getsimusort(simu):
    simusort = -np.sort(-simu)
    np.savetxt('simusort.csv', simusort, delimiter=',', fmt='%.4f')
    return simusort

# 通过调用np.argsort()获得simu数组的每一行降序排列时的索引值数组simusortindex并保存到simusortindex.csv文件中
def getsimusortindex(simu):
    simusortindex = np.argsort(-simu)
    np.savetxt('simusortindex.csv', simusortindex, delimiter=',', fmt='%d')
    return simusortindex

# 通过p_ulikem()函数从um数组、simusort数组和simusortindex数组获得用户对每个未评分电影的感兴趣程度值pulikem数组并保存到pulikem.csv文件中，其中10代表取相似度最高的前10个用户的数据
def getpulikem(um,simusort,simusortindex,k):
    pulikem = pUlikem(um, simusort, simusortindex,k)
    np.savetxt('pulikem.csv', pulikem, delimiter=',', fmt='%.4f')
    pulikem1=np.loadtxt('pulikem.csv',delimiter=',')
    return pulikem1

# 通过调用np.argsort()获得pulikm数组的每一行降序排列时的索引值数组pulikemsortindex并保存到pulikemsortindex.csv文件中
def getpulikemsortindex(pulikem):
    pulikemsortindex = np.argsort(-pulikem, axis=1)
    np.savetxt('pulikemsortindex.csv', pulikemsortindex, delimiter=',', fmt='%d')
    return pulikemsortindex

# 将movies.csv中未被评分过的电影删除并保存到movies1.csv文件中
def updatemovies(file1,file2):
    movies = pd.read_csv(file2, index_col='movieId')
    df=pd.read_csv(file1)
    movieid = list(set(list(df['movieId'])))
    movieid.sort()
    movies1 = []
    for mid, title in movies.iterrows():
        if mid in movieid:
            movies1.append(list(title))
    movies2 = pd.DataFrame(movies1, index=movieid, columns=['title', 'genres'])
    movies2.index.name = 'movieId'
    movies2.to_csv('movies1.csv', index=True)
    movies3=pd.read_csv('movies1.csv')
    return movies3

# 将links.csv中未被评分过的电影删除并保存到links1.csv文件中
def updatelinks(file1,file2):
    links=pd.read_csv(file2,index_col='movieId',dtype=str)
    df = pd.read_csv(file1)
    movieid = list(set(list(df['movieId'])))
    movieid.sort()
    links1=[]
    for mid,dbid in links.iterrows():
        if mid in movieid:
            links1.append((list(dbid)))
    links2=pd.DataFrame(links1,index=movieid,columns=['imdbId','tmdbId'])
    links2.index.name='moviId'
    links2.to_csv('link1.csv',index=True)
    links3=pd.read_csv('link1.csv',dtype=str)
    return links3





movies=updatemovies('data.csv','movies.csv')
um=getum('data.csv')
simu=getsimu(um)
simusort=getsimusort(simu)
simusortindex=getsimusortindex(simu)
k=10
pulikem=getpulikem(um,simusort,simusortindex,k)
pulikemsortindex=getpulikemsortindex(pulikem)
links=updatelinks('data.csv','links.csv')

#用result保存获得的给每个用户推荐10个电影的结果
result = []
for i in range(len(pulikemsortindex)):
    result.append(ulikemtopN(i, k, movies, pulikemsortindex, links))
    print(result[i])
result=pd.DataFrame(result)
result.index.name='UserId'
result.to_csv('result.csv')