from django.shortcuts import render
from pickle import load
import pandas 
import numpy as np

def welcome(request):
    # Load the DataFrame from the pickle file
    with open('./savedmodels/popular.pkl', 'rb') as f:
        popular_df = load(f)

    # Extract the columns from the DataFrame
    book_names = list(popular_df['Book-Title'].values)
    authors = list(popular_df['Book-Author'].values)
    images = list(popular_df['Image-URL-M'].values)
    votes = list(popular_df['num_ratings'].values)
    ratings = list(popular_df['avg_ratings'].values)

    # Zip the lists
    books_data = zip(book_names, authors, images, votes, ratings)

    # Pass the zipped list as context to the template
    context = {
        'books_data': books_data,
    }

    # Render the template with the context
    return render(request, 'index.html', context)

def recommend_ui(request):
    with open('./savedmodels/pt.pkl', 'rb') as g:
        pt = load(g)
    with open('./savedmodels/books.pkl', 'rb') as h:
        books = load(h)
    with open('./savedmodels/similarity_scores.pkl', 'rb') as k:
        similarity_scores = load(k)

    if request.method == "POST":
        user_input = request.POST.get('user_input')
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]
        data = []

        for i in similar_items:
            item = {}
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item['title'] = temp_df.drop_duplicates('Book-Title')['Book-Title'].values[0]
            item['author'] = temp_df.drop_duplicates('Book-Title')['Book-Author'].values[0]
            item['image_url'] = temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values[0]

            data.append(item)

        return render(request, "recommend.html", {'data': data, 'user_input': user_input})

    return render(request, "recommend.html")

def recommend_books(request):
    # This view will handle the form submission for /recommend_books/
    with open('./savedmodels/pt.pkl', 'rb') as g:
        pt = load(g)
    with open('./savedmodels/books.pkl', 'rb') as h:
        books = load(h)
    with open('./savedmodels/similarity_scores.pkl', 'rb') as k:
        similarity_scores = load(k)
    if request.method == "POST":
        user_input = request.POST.get('user_input')
        # ... (your existing logic to get recommendations)
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]
        data = []

        for i in similar_items:
            item = {}
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item['title'] = temp_df.drop_duplicates('Book-Title')['Book-Title'].values[0]
            item['author'] = temp_df.drop_duplicates('Book-Title')['Book-Author'].values[0]
            item['image_url'] = temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values[0]

            data.append(item)
        return render(request, "recommend.html", {'data': data, 'user_input': user_input})
    else:
        return render(request, "recommend.html")