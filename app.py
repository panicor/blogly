"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'hey'
app.debug = True

toolbar = DebugToolbarExtension(app)

connect_db(app)
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    posts = Post.query.order_by(Post.created_at.desc()).limit(10).all()
    return render_template("posts/home.html", posts = posts)

@app.errorhandler(404)
def error(e):
    return render_template('404.html'), 404

@app.route('/users')
def users_list():
    users = User.query.order_by(User.l_name, User.f_name).all()
    return render_template('users/index.html', users=users)

@app.route('/users/new', methods=["GET"])
def users_new_form():
    return render_template('users/new.html')

@app.route('/users/new', methods=["POST"])
def users_new():
    new_user = User(
        f_name = request.form['f_name'],
        l_name = request.form['l_name'],
        image_url = request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def users_display(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/display.html', user=user)

@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def users_update(user_id):
    user = User.query.get_or_404(user_id)
    user.f_name = request.form['f_name']
    user.l_name = request.form['l_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def users_delete(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

@app.route("/users/<int:user_id>/posts/new", methods=['GET'])
def posts_new_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("posts/new.html", user=user)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def posts_new(user_id):
    user = User.query.get_or_404(user_id)
    new_post = Post(
                title = request.form['title'], 
                content =request.form['content'],
                user=user)

    db.session.add(new_post)
    db.session.commit()

    flash(f'Post with title "{new_post.title}" was added.')

    return redirect(f"/users/{user_id}")

@app.route("/posts/<int:post_id>")
def posts_display(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("posts/display.html", post=post)

@app.route("/posts/<int:post_id>/edit")
def posts_edit(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("posts/edit.html", post=post)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def posts_update(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    flash(f'Post with title "{post.title}" was edited.')

    return redirect(f"/users/{post.user_id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def posts_delete(post_id):
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    flash(f'Post with title "{post.title}" was deleted.')

    return redirect(f"/users/{post.user_id}")