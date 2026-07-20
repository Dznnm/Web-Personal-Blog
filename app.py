from flask import Flask, render_template, request, url_for, redirect
import json
from datetime import datetime

app = Flask(__name__)

#date and time
now = datetime.now()
timestamp = now.strftime("%Y-%m-%d")

#helper functions
def load_articles():
    try:
        with open("articles.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def save_articles(articles):
    with open("articles.json", "w") as file:
        json.dump(articles, file, indent=4)

#Routes
@app.route('/', methods=['GET', 'POST'])
def home():
    articles = load_articles()
    return render_template('home.html', articles=articles)

@app.route('/article/<int:article_id>')
def article(article_id):

    articles = load_articles()
    article = None
    for a in articles:
        if a['id'] == article_id:
            article = a
            break
    for a in articles:
        if a['id'] == article_id:
            article = a
            break

    return render_template('article.html', article=article)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    articles = load_articles()
    return render_template('dashboard.html', articles=articles)

@app.route('/add_article', methods=['GET', 'POST'])
def add_article():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        articles = load_articles()
        highest_id = max(article["id"] for article in articles) if articles else 0
        new_article = {
            "id": highest_id + 1,
            "date": timestamp,
            "title": title,
            "content": content
        }
        articles.append(new_article)
        save_articles(articles)

        return redirect(url_for('home'))

    return render_template('add_article.html')

@app.route('/edit_article/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    articles = load_articles()
    article = None
    for a in articles:
        if a["id"] == article_id:
            article = a
            break

    if not article:
        return "Article not found", 404

    if request.method == 'POST':
        if request.form['edit_article'] == 'Update Article':
            title = request.form['title']
            content = request.form['content']

            article['title'] = title
            article['content'] = content
            save_articles(articles)
        
        if request.form['delete_article'] == 'Delete Article':
            articles.remove(article)
            save_articles(articles)

        return redirect(url_for('dashboard'))

    return render_template('edit_article.html', article=article, success=False)