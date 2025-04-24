from flask import Flask, render_template, request
import pickle
import numpy as np

import pandas as pd

import os
import gdown
BOOKS_URL = "https://drive.google.com/file/d/1PpSR4PbEtQnCD5f-fLLkQORkrgKZ_OAl/view?usp=sharing"
BOOKS_FILE = "books.pkl"

if not os.path.exists(BOOKS_FILE):
    print("Downloading books.pkl from Google Drive...")
    gdown.download(BOOKS_URL, BOOKS_FILE, quiet=False)


# Open the pickle file
with open('popular.pkl', 'rb') as f:
    try:
        popular_df = pd.read_pickle(f)
    except Exception as e:
        print("Error loading pickle file:", e)

with open('pt.pkl', 'rb') as g:
    try:
        pt = pd.read_pickle(g)
    except Exception as e:
        print("Error loading pickle file:", e)

with open('books.pkl', 'rb') as h:
    try:
        books = pd.read_pickle(h)
    except Exception as e:
        print("Error loading pickle file:", e)

with open('similarity_scores.pkl', 'rb') as i:
    try:
        similarity_scores = pd.read_pickle(i)
    except Exception as e:
        print("Error loading pickle file:", e)


app = Flask(__name__)

@app.route('/')

def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author = list(popular_df['Book-Author'].values),
                           image = list(popular_df['Image-URL-M'].values),
                           votes = list(popular_df['num_ratings'].values),
                           ratings = list(popular_df['avg_ratings'].values)
                           )

@app.route('/recommend')

def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['post'])
def recommend_book():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html', data=data)

if __name__ == '__main__':
    app.run(debug = True)
