from flask import Flask, render_template, request, flash
import configparser
import os
from database_scripts.get_posts import get_posts
from database_scripts.get_post import get_post
from database_scripts.create_table import create_table
from database_scripts.new_post import new_post
from database_scripts.get_max_id import get_max_id
import time
import math
from flask_mysqldb import MySQL

os.makedirs('databases', exist_ok=True)

config = configparser.ConfigParser()

config.read('secret_data/config.ini')

app = Flask(__name__)

app.config["SECRET_KEY"] = config['Flask']['SECRET_KEY']
app.config['DEBUG'] = config['Flask']['DEBUG']
app.config['MYSQL_USER'] = config['MySQL']['user']
app.config['MYSQL_PASSWORD'] = config['MySQL']['password']
app.config['MYSQL_DB'] = config['MySQL']['database']

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def main():
    cursor = mysql.connection.cursor()
    cursor.execute(get_posts())
    data = cursor.fetchall()

    return render_template('base.html', posts=data)


@app.route('/posts/<int:id_post>')
def show_posts(id_post):
    cursor = mysql.connection.cursor()
    cursor.execute(get_post(), (id_post,))
    data = cursor.fetchone()

    title = data[1]
    content = data[2]

    return render_template('show_posts_page.html', title=title, content=content)


@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':

        try:

            title = request.form['title']
            content = request.form['content']

            if not all([title, content]):

                raise ValueError

            else:

                cursor = mysql.connection.cursor()

                cursor.execute(get_max_id())

                max_id = cursor.fetchone()

                max_id = max_id[0] if max_id[0] else 0

                cursor.execute(new_post(),
                               (int(max_id) + 1,
                                title,
                                content,
                                math.floor(time.time()),))

                mysql.connection.autocommit(on=True)

                flash('Post added successfully', category='success')

                return render_template('add_post.html')

        except ValueError:

            flash('Post can\'t be empty', category='bad')

            return render_template('add_post.html')

    else:

        return render_template('add_post.html')


@app.before_request
def before_request():
    cursor = mysql.connect.cursor()
    cursor.execute(create_table())


if __name__ == '__main__':
    app.run(debug=bool(int(app.config['Flask']['DEBUG'])))
