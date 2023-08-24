import csv
import pandas as pd
from flask import Flask,jsonify,request
from demographic_filter import output
from content_filter import get_recommendations
movies_data = pd.read_csv("final.csv")
all_movies = movies_data[["original_title","poster_link","release_date","runtime","weighted_rating"]]
liked_movies = []
unliked_movies = []
not_watched_movies = []

def info():
    movie_data = {
        "original_title":all_movies.iloc[0,0],
        "poster_link":all_movies.iloc[0,1],
        "release_date":all_movies.iloc[0,2],
        "duration":all_movies.iloc[0,3],
        "rating":all_movies.iloc[0,4]/2
    }
    return movie_data

app = Flask(__name__)
@app.route("/get-movie")
def get_movie():
    m_data = info()
    return jsonify({
        "data":m_data,
        "status":"success"
    })
@app.route("/like")
def liked_movie():
    global all_movies
    m_data = info()
    liked_movies.append(m_data)
    all_movies.drop([0],inplace=True)
    all_movies = all_movies.reset_index(drop=True)
    return jsonify({
        "status":"success"
    })
@app.route("/dislike")
def disliked_movie():
    global all_movies
    m_data = info()
    unliked_movies.append(m_data)
    all_movies.drop([0],inplace=True)
    all_movies = all_movies.reset_index(drop=True)
    return jsonify({
        "status":"success"
    })
@app.route("/not_watched")
def not_watch_movie():
    global all_movies
    m_data = info()
    not_watched_movies.append(m_data)
    all_movies.drop([0],inplace=True)
    all_movies = all_movies.reset_index(drop=True)
    return jsonify({
        "status":"success"
    })
@app.route("/liked_movies")
def like():
    global liked_movies
    return jsonify({
        "data":liked_movies,
        "status":"success"
    })
@app.route("/popular_movies")
def popular():
    pop_movie_data = []
    for index,row in output.iterrows():
        pm_data = {
            "original_title":row["original_title"],
            "poster_link":row["poster_link"],
            "release_date":row["release_date"],
            "duration":row["runtime"],
            "rating":row["weighted_rating"]/2,

        }
        pop_movie_data.append(pm_data)
    return jsonify({
        "data":pop_movie_data,
        "status":"success"
    })
@app.route("/recommended_movies")
def recon_movies():
    global liked_movies
    column_names = ["original_title","poster_link","release_date","runtime","weighted_rating"]
    all_recommended = pd.DataFrame(columns = column_names)
    for i in liked_movies:
        output = get_recommendations(i["original_title"])
        all_recommended = all_recommended.append(output)
    all_recommended.drop_duplicates(subset=["original_title"],inplace=True)
    recommended_movie_data=[]
    for index,row in all_recommended.iterrows():
        pm_data = {
            "original_title":row["original_title"],
            "poster_link":row["poster_link"],
            "release_date":row["release_date"],
            "duration":row["runtime"],
            "rating":row["weighted_rating"]/2,

        }
        recommended_movie_data.append(pm_data)
    return jsonify({
        "data":recommended_movie_data,
        "status":"success"
    })








if __name__ == "__main__":
    app.run()
