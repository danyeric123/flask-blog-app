from werkzeug.utils import redirect
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default="N/A")
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


@app.route("/")
# def index():
#   return render_template('index.html')


@app.route("/posts", methods=["POST", "GET"])
def posts():
    if request.method == "POST":
        post_title, post_content, post_author = (
            request.form["title"],
            request.form["content"],
            request.form["author"],
        )
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect("/posts")
    return render_template(
        "posts.html", posts=BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
    )


@app.route("/posts/<int:id>/delete")
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/posts")


@app.route("/posts/<int:id>/edit", methods=["GET", "POST"])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == "POST":
        post.title, post.content, post.author = (
            request.form["title"],
            request.form["content"],
            request.form["author"],
        )
        db.session.commit()
        return redirect("/posts")
    else:
        return render_template("edit.html", post=post)


@app.route("/posts/<string:author>")
def author_posts(author):
    author_posts = (
        BlogPost.query.filter_by(author=author)
        .order_by(BlogPost.date_posted.desc())
        .all()
    )
    return render_template("posts.html", posts=author_posts)


if __name__ == "__main__":
    app.run(debug=True)
