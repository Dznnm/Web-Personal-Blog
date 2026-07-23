from flask import Flask, render_template, request, url_for, redirect, session
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'skey'
 
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
#GUEST ROUTES
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

    return render_template('article_guest.html', article=article)

#ADMIN ROUTES
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'valedian' and password == 'password':
            session['user'] = request.form['username']
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials", 401

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return 'You have been logged out. <a href="/">Go to Home</a>'

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    articles = load_articles()
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        if request.form['action'] == 'Delete Article':
            articles.remove(article)
            save_articles(articles)
        return redirect(url_for('dashboard'))
    return render_template('dashboard.html', user = session['user'], articles=articles)

@app.route('/articled/<int:article_id>')
def articled(article_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    articles = load_articles()
    article = None
    for a in articles:
        if a['id'] == article_id:
            article = a
            break
    if request.method == 'POST':
        if request.form['action'] == 'Delete Article':
            articles.remove(article)
            save_articles(articles)

        return redirect(url_for('dashboard'))
    return render_template('article.html', article=article)

@app.route('/add_article', methods=['GET', 'POST'])
def add_article():
    if 'user' not in session:
        return redirect(url_for('login'))
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
    if 'user' not in session:
        return redirect(url_for('login'))

    articles = load_articles()
    article = None
    for a in articles:
        if a["id"] == article_id:
            article = a
            break

    if not article:
        return "Article not found", 404

    if request.method == 'POST':
        if request.form['action'] == 'Update Article':
            title = request.form['title']
            content = request.form['content']

            article['title'] = title
            article['content'] = content
            save_articles(articles)
        
        if request.form['action'] == 'Delete Article':
            articles.remove(article)
            save_articles(articles)

        return redirect(url_for('dashboard'))

    return render_template('edit_article.html', article=article, success=False)