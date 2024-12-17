from . import post_bp
from flask import render_template, abort, flash, redirect, url_for, session, request
from .forms import PostForm
from .utils import load_posts, save_posts
import datetime
import json

@post_bp.route('/resume')
def resume():
    page_title = "Резюме"
    return render_template('resume.html', title=page_title)

def load_posts():
    try:
        with open('posts.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def save_posts(posts):
    with open('posts.json', 'w') as file:
        json.dump(posts, file, indent=4)

@post_bp.route('/')
def get_posts():
    posts = load_posts()
    
    for post in posts:
        try:
            post["publish_date"] = datetime.datetime.strptime(
                post["publish_date"], '%Y-%m-%d'
            ).strftime('%B %d, %Y')
        except (ValueError, KeyError):
            post["publish_date"] = "Unknown date"
    
    return render_template('posts.html', posts=posts)

@post_bp.route('/<int:id>')
def detail_post(id):
    posts = load_posts()
    post = next((post for post in posts if post["id"] == id), None)
    if post is None:
        abort(404)
    return render_template("detail_post.html", post=post)

@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        is_active = form.is_active.data
        publish_date = form.publish_date.data.strftime('%Y-%m-%d')
        category = form.category.data

        posts = load_posts()
        new_id = len(posts) + 1
        new_post = {
            "id": new_id,
            "title": title,
            "content": content,
            "author": "Admin",
            "is_active": is_active,
            "publish_date": publish_date,
            "category": category
        }
        
        posts.append(new_post)
        save_posts(posts)
        flash(f'Post "{title}" added successfully!', 'success')
        return redirect(url_for('posts.get_posts'))
    return render_template('add_post.html', form=form)

@post_bp.route('/delete_post/<int:id>', methods=['POST'])
def delete_post(id):
    posts = load_posts()
    post_to_delete = next((post for post in posts if post["id"] == id), None)
    if post_to_delete:
        posts.remove(post_to_delete)
        save_posts(posts)
        flash(f'Post "{post_to_delete["title"]}" has been deleted successfully!', 'success')
    return redirect(url_for('posts.get_posts'))

@post_bp.route('/toggle_active/<int:id>', methods=['POST'])
def toggle_active(id):
    posts = load_posts()
    post = next((post for post in posts if post["id"] == id), None)
    if post:
        post["is_active"] = not post["is_active"]
        save_posts(posts)
        flash(f'Post "{post["title"]}" is now {"active" if post["is_active"] else "inactive"}!', 'success')
    return redirect(url_for('posts.get_posts'))
