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