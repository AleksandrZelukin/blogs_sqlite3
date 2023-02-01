
from flask import Flask, render_template, url_for, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

db = sqlite3.connect('blog.db')

cur=db.cursor()



# cur.execute("DROP TABLE IF EXISTS articles")
cur.execute("""CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    intro TEXT NOT NULL,
    text TEXT NOT NULL,
    date DATETIME DEFAULT utcnow
)""")


# Добавление данных
cur.execute("INSERT INTO articles VALUES ('Amazon is cool!', 'Amazon is really cool','Modest')")

# Удаление данных
cur.execute("DELETE FROM articles WHERE title = 'Admin'")

# Изменение данных
cur.execute("UPDATE articles SET title = 'Admin', views = 1 WHERE title = 'Amazon is cool!'")

# Выборка данных
cur.execute("SELECT rowid, * FROM articles WHERE rowid < 5 ORDER BY views")
items = cur.fetchall()
print(items)
print(cur.fetchmany(1))
# print(c.fetchone()[1])

for el in items:
    print(el[1] + "\n" + el[4])

db.commit()

db.close()

result = cur.fetchall()
print(result)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/posts', methods=['POST', 'GET'])
def posts():
    
    return render_template("posts.html")

@app.route('/posts/<int:id>', methods=['POST', 'GET'])
def post_detail(id):
    return render_template("post_detail.html")


@app.route('/posts/<int:id>/del')
def post_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "Kluda!"

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']


        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')

        except:
            return "Rakstu pievienošanai procesa rodas Kluda!"
    else:
        return render_template("create-article.html")


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')

        except:
            return "Rakstu rediģesanas procesa rodas Kluda!"
    else:
        
        return render_template("post_update.html", article=article)



if __name__ == "__main__":
    app.run(debug=True)

# app.run(host='0.0.0.0', port=80)

