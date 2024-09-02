from flask import Flask, render_template, request, flash
import configparser
import os
import sqlite3
from sql_scripts import *
import time
import math

os.makedirs('databases', exist_ok=True)

config = configparser.ConfigParser()

config.read('config.ini')

app = Flask(__name__)

app.config["SECRET_KEY"] = config['Flask']['SECRET_KEY']
app.config['DATABASE'] = config['Flask']['DATABASE']
app.config['DEBUG'] = config['Flask']['DEBUG']

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'databases/database.db')))


def create_table_in_db():

    connection = sqlite3.connect(app.config['DATABASE'])
    cursor = connection.cursor()

    cursor.execute(sql_create_database())

    connection.commit()

    cursor.close()
    connection.close()


def get_post(id):

    connection = sqlite3.connect(app.config['DATABASE'])
    cursor = connection.cursor()

    cursor.execute(sql_get_post_database(), (id,))

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result


def get_posts():

    connection = sqlite3.connect(app.config['DATABASE'])
    cursor = connection.cursor()

    cursor.execute(sql_get_posts_database())

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


def new_post(title, content):

    try:

        date = math.floor(time.time())

        connection = sqlite3.connect(app.config['DATABASE'])
        cursor = connection.cursor()

        cursor.execute(sql_new_post_database(), (title, content, date))

        connection.commit()

        cursor.close()
        connection.close()

    except Exception as e:

        return False, e

    else:

        return True, None


@app.route('/', methods=['GET', 'POST'])
def main():

    data = get_posts()

    return render_template('base.html', posts=data)


@app.route('/posts/<int:id_post>')
def show_posts(id_post):

    data = get_post(id_post)

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

                result = new_post(title, content)

                if result[0]:

                    flash('Post added successfully', category='success')

                else:

                    flash(str(result[1]), category='bad')

                return render_template('add_post.html')

        except ValueError:

            flash('Post can\'t be empty', category='bad')

            return render_template('add_post.html')

    else:

        return render_template('add_post.html')


@app.before_request
def before_request():
    create_table_in_db()


if __name__ == '__main__':
    app.run(debug=True)
