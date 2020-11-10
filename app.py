from flask import Flask, render_template, url_for, abort, request, redirect
from flaskext.markdown import Markdown
import contentful
from trycourier import Courier
from dotenv import load_dotenv
import os
import uuid

load_dotenv()
SPACE_ID = os.environ.get("SPACE_ID")
DELIVERY_API_KEY = os.environ.get("DELIVERY_API_KEY")
API_URL = os.environ.get("API_URL")
ENV = os.environ.get("ENV")
COURIER_AUTH_TOKEN = os.environ.get("COURIER_AUTH_TOKEN")
FLASK_DEBUG = os.environ.get("FLASK_DEBUG")

client = contentful.Client(SPACE_ID, DELIVERY_API_KEY, API_URL, environment=ENV)
courier_client = Courier()

app = Flask(__name__)
Markdown(app)


def format_datetime(value):
    """Format date time object using jinja filters"""
    return value.strftime("%B %-d, %Y")


app.jinja_env.filters["datetime"] = format_datetime


@app.route("/")
@app.route("/home")
def index():
    """index route. Gathers information from contentful and renders page"""
    shows = client.entries(
        {"content_type": "show", "order": "fields.first_episode_date"}
    )

    entry_id = "7AmisHpntSSYOkuOcueecw"
    intro_string = client.entry(entry_id)

    return render_template(
        "index.html",
        shows=shows,
        intro_string=intro_string.intro_string,
        title=intro_string.title,
    )


@app.route("/show/<string:entry_id>")
def show(entry_id):
    """Take a Slug and return a Show."""
    show = client.entries({"content_type": "show", "fields.slug": entry_id})
    show = show[0]

    return render_template("show.html", show=show, title="- " + show.title)


@app.route("/<string:filter_string>")
def filter(filter_string):
    """Filters by show type"""
    intro_string = client.entries(
        {"content_type": "intro_string", "fields.type": filter_string}
    )

    if not intro_string:
        abort(404)

    intro_string = intro_string[0]

    shows = client.entries(
        {
            "content_type": "show",
            "order": "fields.first_episode_date",
            "fields.type": filter_string,
        }
    )

    return render_template(
        "index.html",
        shows=shows,
        intro_string=intro_string.intro_string,
        title=intro_string.title,
    )


@app.route("/email_submit", methods=["POST"])
def email_submit():
    email = request.form["email"]
    sub_type = request.form["type"]
    recipent_id = uuid.uuid4()
    courier_client.replace_profile(recipent_id, {"email": email})
    if sub_type == "everyone":
        list_id = "henshin.blog"
    else:
        list_id = f"henshin.blog.{sub_type}"
    courier_client.lists.subscribe(list_id, recipent_id)
    success_image = client.asset("6WgPhLpPAKnzeArKWdWfzM")
    return render_template(
        "email_submitted.html",
        email=email,
        type=sub_type,
        success_image=success_image,
        summary_message=f"{email} has been subscribed to our {sub_type} email list!",
    )


@app.route("/user/<string:recipent_id>", methods=["POST", "GET"])
def user_profile(recipent_id):
    if request.method == "GET":
        success_image = client.asset("2EvzLa2QCuv5Jr5NEsgf2A")
        profile = courier_client.get_profile(recipent_id)
        lists = courier_client.lists.find_by_recipient_id(recipent_id)
        return render_template(
            "user.html",
            profile=profile,
            lists=lists,
            success_image=success_image,
            recipent_id=recipent_id,
        )
    elif request.method == "POST":
        recipent_id = request.form["recipent_id"]
        email = request.form["email"]
        sub_type = request.form["type"]
        success_image_dict = {
            "unsubscribe": "3QcVid0F6RQv8IQkWSOpQX",
            "supersentai": "FqWHTUkgWYoQYHa6LjxM5",
            "kamenrider": "2NUqyQPzpl55OaYu3AN739",
            "everyone": "6KCYnLQynyf6IRCsx87ffP",
        }
        success_image = client.asset(success_image_dict[sub_type])
        result = courier_client.lists.find_by_recipient_id(recipent_id)
        courier_client.merge_profile(recipent_id, {"email": email})
        for item in result["results"]:
            courier_client.lists.unsubscribe(item["id"], recipent_id)
        if sub_type == "everyone":
            list_id = "henshin.blog"
        elif sub_type == "unsubscribe":
            return render_template(
                "email_submitted.html",
                email=email,
                type=sub_type,
                success_image=success_image,
                summary_message=f"{email} has been unsubscribed from all email lists.",
            )
        else:
            list_id = f"henshin.blog.{sub_type}"
        courier_client.lists.subscribe(list_id, recipent_id)
        return render_template(
            "email_submitted.html",
            email=email,
            type=sub_type,
            summary_message=f"{email} has been subscribed to our {sub_type} email list!",
            success_image=success_image,
        )


# We only need this for local development.
if __name__ == "__main__":
    app.run(debug=FLASK_DEBUG)
