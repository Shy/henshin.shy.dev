from flask import Flask, render_template
from flaskext.markdown import Markdown
import contentful

client = contentful.Client(
    'mt0pmhki5db7',
    '8c7dbd270cb98e83f9d8d57fb8a2ab7bac9d7501905fb013c69995ebf1b2a719')

app = Flask(__name__)
Markdown(app)
app.debug = True


def format_datetime(value):
    """Format date time object using jinja filters"""
    return (value.strftime('%B %-d, %Y'))


app.jinja_env.filters['datetime'] = format_datetime


@app.route('/')
@app.route('/home')
def index():
    """index route. Gathers information from contentful and renders page"""
    shows = client.entries(
        {'content_type': 'show',
         'order': 'fields.first_episode_date'})

    entry_id = '7AmisHpntSSYOkuOcueecw'
    intro_string = client.entry(entry_id).intro_string

    return render_template('index.html',
                           shows=shows,
                           intro_string=intro_string,
                           title="Henshin!")


@app.route('/show/<string:entry_id>')
def show(entry_id):
    """Take a Slug and return a Show."""
    show = client.entries(
        {'content_type': 'show',
         'fields.slug': entry_id})
    show = show[0]

    return render_template('show.html',
                           show=show,
                           title="- " + show.title)


@app.route('/kamenrider')
def kamenrider():
    """Same as basic index, but only returns Kamen Rider"""
    shows = client.entries(
        {'content_type': 'show',
         'order': 'fields.first_episode_date',
         'fields.type': 'Kamen Rider'})

    entry_id = '5eyqYKNFYcokiMYCqeYEWM'
    intro_string = client.entry(entry_id).intro_string

    return render_template('index.html',
                           shows=shows,
                           intro_string=intro_string,
                           title="Kamen Rider")


@app.route('/supersentai')
def supersentai():
    """Same as basic index, but only returns Super Sentai"""
    shows = client.entries(
        {'content_type': 'show',
         'order': 'fields.first_episode_date',
         'fields.type': 'Super Sentai'})

    entry_id = 'WlrfS7yUw0GioqMK2geqO'
    intro_string = client.entry(entry_id).intro_string

    return render_template('index.html',
                           shows=shows,
                           intro_string=intro_string,
                           title="Super Sentai")


# We only need this for local development.
if __name__ == '__main__':
    app.run()
