from flask import Flask, render_template, jsonify, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/")
def index():
    stories = Story.query.all()
    return render_template("index.html", stories=stories)


@app.route("/use", methods=["POST"])
def use():
    """use the story"""
    try:
        story_id = int(request.form.get("story_id"))
    except ValueError:
        return render_template("error.html", message="Invalid story number.")

    story = Story.query.get(story_id)
    if not story:
        return render_template("error.html", message="No such story with that id.")

    name = request.form.get("name")
    story.add_publisher(name)
    return render_template("success.html")


@app.route("/stories")
def stories():
    """List all stories."""
    stories = Story.query.all()
    return render_template("stories.html", stories=stories)


@app.route("/stories/<int:story_id>")
def story(story_id):
    """List details about a single story."""

    story = Story.query.get(story_id)
    if not story:
        return render_template("error.html", message="No such story with that id.")

    # Get all publishers.
    publishers = story.publishers
    return render_template("story.html", story=story, publishers=publishers)



@app.route("/api/stories", methods=["GET"])
def get_all_stories():
    stories = Story.query.all()
    story_ls = []
    for story in stories:
        story_ls.append({
            "id": story.sid,
            "title": story.title,
            "link": story.link
        })

    return jsonify(story_ls)


@app.route("/api/publishers", methods=["GET"])
def get_all_publishers():
    publishers = Publisher.query.all()
    publisher_ls = []
    for publisher in publishers:
        publisher_ls.append({
            "id": publisher.pid,
            "name": publisher.name,
            "storyid": publisher.story_id
        })

    return jsonify(publisher_ls)


@app.route('/api/publishers', methods=['POST'])
def create_story():
    if not request.json or not 'name' in request.json:
        return render_template("error.html", message="check title")


    data = request.json
    name = data['name'].encode('ascii','ignore')
    storyid = data['story_id']

    print(type(name), type(storyid), name)

    new_publisherid = Publisher(name= name, story_id = storyid)

    db.session.add(new_publisherid)
    db.session.commit()

    return jsonify({
            "id": new_publisherid.pid,
            "name": new_publisherid.name,
            "storyid": new_publisherid.story_id
        })

@app.route("/api/stories/<int:story_id>", methods=["GET"])
def get_story(story_id):
    """Return details about a single story."""

    # Make sure story exists.
    story = Story.query.get(story_id)
    if story is None:
        return jsonify({"error": "Invalid story_id"}), 422

    # Get all publishers.
    publishers = story.publishers
    names = []
    for publisher in publishers:
        names.append(publisher.name)
    return jsonify({
        "id": story.sid,
        "title": story.title,
        "link": story.link,
        "publishers": names
    })

@app.route("/api/publishers/<string:publisher_name>", methods=["GET"])
def get_publisher(publisher_name):
    """Return details about a single Publisher."""

    publishers = Publisher.query.filter_by(name=publisher_name).all()
    if publishers is None:
        return jsonify({"error": "Invalid publisher_name - it should be all small letters"}), 422

    story_info = []
    for publisher in publishers:
        story = Story.query.get(publisher.story_id)
        story_info.append({
            "title": story.title,
            "link": story.link
        })
    return jsonify({
        "id": publisher.pid,
        "publisher": publisher_name,
        "story": story_info
    })
