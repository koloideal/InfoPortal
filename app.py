from flask import Flask, render_template, request, flash, g
import configparser
import os
from database_scripts.ConnectDatabase import ConnectDatabase
from database_scripts.get_posts import get_posts
from database_scripts.get_post import get_post
from database_scripts.create_table import create_table
from database_scripts.new_post import new_post
from datetime import datetime

os.makedirs('databases', exist_ok=True)

config = configparser.ConfigParser()

config.read('secret_data/config.ini')

app = Flask(__name__)

app.config["SECRET_KEY"] = config['Flask']['SECRET_KEY']
app.config['MySQL']['user'] = config['MySQL']['user']
app.config['MySQL']['password'] = config['MySQL']['password']
app.config['MySQL']['host'] = config['MySQL']['host']
app.config['MySQL']['port'] = config['MySQL']['port']
app.config['MySQL']['database'] = config['MySQL']['database']
app.config['DEBUG'] = config['Flask']['DEBUG']

CONNECT = ConnectDatabase(app.config['MySQL']['user'],
                          app.config['MySQL']['password'],
                          app.config['MySQL']['database'])


@app.route('/', methods=['GET', 'POST'])
def main():
    with CONNECT as cursor:
        data = cursor.execute(get_posts())

    return render_template('base.html', posts=data)


@app.route('/posts/<int:id_post>')
def show_posts(id_post):

    with CONNECT as cursor:

        data = cursor.execute(get_post(),(id_post,))

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

                with CONNECT as cursor:

                    result = cursor.execute(new_post(), (title, content, datetime.now()))

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
    with CONNECT as cursor:
        cursor.execute(create_table())


if __name__ == '__main__':
    app.run(debug=bool(int(app.config['Flask']['DEBUG'])))
