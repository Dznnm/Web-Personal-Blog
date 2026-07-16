from flask import Flask, render_template, request

app = Flask(__name__)

#Routes
@app.route('/', methods=['GET', 'POST'])
def home():
    articles = [
        {"id": 1,
         "date": "2024-06-01",
         "title": "My First Blog Post",
         "content": "This is the content of my first blog post."
        },
        {"id": 2,
            "date": "2024-06-02",
         "title": "My Second Blog Post",
         "content": "This is the content of my second blog post."
        }
    ]

    return render_template('home.html', articles=articles)

@app.route('/article/<int:article_id>')
def article(article_id):
    articles = [
        {"id": 1,
         "date": "2024-06-01",
         "title": "My First Blog Post",
         "content": "This is the content of my first blog post."
        },
        {"id": 2,
            "date": "2024-06-02",
         "title": "My Second Blog Post",
         "content": "This is the content of my second blog post."
        }
    ]

    article = next((a for a in articles if a["id"] == article_id), None)
    if article is None:
        return render_template('404.html'), 404

    return render_template('article.html', article=article)