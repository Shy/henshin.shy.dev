from flask import Flask, render_template
from flaskext.markdown import Markdown
import contentful

client = contentful.Client(
    'mt0pmhki5db7',
    '8c7dbd270cb98e83f9d8d57fb8a2ab7bac9d7501905fb013c69995ebf1b2a719')

app = Flask(__name__)


def format_datetime(value):
    """Format date time object from jinja"""
    return (value.strftime('%B %-d, %Y'))

Markdown(app)
app.jinja_env.filters['datetime'] = format_datetime


@app.route('/')
def index():
    """index route. Gathers information from contentful and renders page"""
    shows = client.entries(
        {'content_type': 'show', 'order': 'fields.first_episode_date'})

    entry_id = '7AmisHpntSSYOkuOcueecw'
    intro_string = client.entry(entry_id).intro_string

    for show in shows:
        print(show.henshin[0].url())
    return render_template('index.html',
                           shows=shows,
                           intro_string=intro_string)


# We only need this for local development.
if __name__ == '__main__':
    app.run(debug=True)
