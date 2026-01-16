from flask import Flask, render_template, g, request, redirect,url_for
import sqlite3

app = Flask(__name__)


def get_db():
    conn = sqlite3.connect("SQLite (2).db")
    conn.row_factory = sqlite3.Row
    return conn

@app.teardown_appcontext
def close_connection(exception):
    connection = getattr(g, 'db', None)
    if connection is not None:
        connection.close()


@app.route("/")
def index():
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('SELECT * from post')
    result = cursor.fetchall()

    posts = []
    for post in result:
        posts.append({
            'id': post[0],
            'title': post[1],
            'content': post[2]
        })

    context = {'posts': posts}
    return render_template("blog.html", **context)

@app.route('/add/',methods=['GET','POST'])
def add_post():
    connection = get_db()
    cursor = connection.cursor()
    if request.method == 'POST':
        title = request.form['title']
        context = request.form['context']
        cursor.execute(
            'INSERT INTO post (title,context) VALUES (?,?)',
            (title,context)
        )
        connection.commit()
        return redirect(url_for('index'))
    return render_template('add_post.html')

@app.route('/post/<post_id>')
def post(post_id):
    connection = get_db()
    cursor = connection.cursor()
    result = cursor.execute(
        'SELECT * FROM post WHERE id = ?',(post_id,)
    ).fetchone()
    post_dikt = {'id': result[0], 'title': result[1], 'content': result[2]}
    return render_template('post.html', post= post_dikt)

if __name__ == "__main__":
    app.run()