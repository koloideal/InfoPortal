from quart import Quart, render_template, request, flash, get_flashed_messages
from message_to_user import main
from telethon.errors.rpcerrorlist import PeerIdInvalidError
import configparser

config = configparser.ConfigParser()

config.read('config.ini')


app = Quart(__name__)
app.config["SECRET_KEY"] = config['Quart']['SECRET_KEY']


@app.route('/', methods=['GET', 'POST'])
async def contact():

    if request.method == 'POST':

        try:

            data = await request.form

            text = data['text']

            username = data['username'] if data['username'][0] != '@' else data['username'][1:]

            await main(text, username)

        except PeerIdInvalidError:

            await flash('Invalid')

        else:

            await flash('Successfully sent')

    return await render_template('base.html')


if __name__ == '__main__':

    app.run(debug=True)
