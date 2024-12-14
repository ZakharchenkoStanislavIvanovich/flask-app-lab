from . import post_bp
from flask import render_template, abort, flash, redirect, url_for, session, request
from .forms import PostForm
from .utils import load_posts, save_posts
import datetime
import json

# posts
posts = [
    {"id": 1, 'title': 'My First Post', 'content': 'This is the content of my first post.', 'author': 'John Doe', 'is_active': True, 'publish_date': '2024-12-01', 'category': 'tech'},
    {"id": 2, 'title': 'Another Day', 'content': 'Today I learned about Flask macros.', 'author': 'Jane Smith', 'is_active': True, 'publish_date': '2024-12-02', 'category': 'science'},
    {"id": 3, 'title': 'Flask and Jinja2', 'content': 'Jinja2 is powerful for templating.', 'author': 'Mike Lee', 'is_active': False, 'publish_date': '2024-12-03', 'category': 'lifestyle'}
]

def load_posts():
    try:
        with open('posts.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

@post_bp.route('/')
def get_posts():
    posts = load_posts()
    
    # Форматування дати, якщо потрібно
    for post in posts:
        try:
            post["publication_date"] = datetime.datetime.strptime(
                post["publication_date"], '%Y-%m-%d'
            ).strftime('%B %d, %Y')  # Наприклад: December 14, 2024
        except (ValueError, KeyError):
            post["publication_date"] = "Unknown date"
    
    return render_template('posts/posts.html', posts=posts)


@post_bp.route('/<int:id>')
def detail_post(id):
    if id > len(posts) or id < 1:
        abort(404)
    post = posts[id - 1]
    return render_template("posts/detail_post.html", post=post)

@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        is_active = form.is_active.data
        publish_date = form.publish_date.data.strftime('%Y-%m-%d')
        category = form.category.data

        new_id = len(posts) + 1
        posts.append({
            "id": new_id,
            "title": title,
            "content": content,
            "author": "Admin",
            "is_active": is_active,
            "publish_date": publish_date,
            "category": category
        })
        flash(f'Post "{title}" added successfully!', 'success')
        return redirect(url_for('posts.get_posts'))
    return render_template('posts/add_post.html', form=form)


@post_bp.route('/delete_post/<int:id>', methods=['POST'])
def delete_post(id):
    if id > len(posts) or id < 1:
        abort(404)
    post_to_delete = next((post for post in posts if post["id"] == id), None)
    if post_to_delete:
        posts.remove(post_to_delete)
        flash(f'Post "{post_to_delete["title"]}" has been deleted successfully!', 'success')
    return redirect(url_for('posts.get_posts'))

@post_bp.route('/toggle_active/<int:id>', methods=['POST'])
def toggle_active(id):
    if id > len(posts) or id < 1:
        abort(404)
    post = next((post for post in posts if post["id"] == id), None)
    if post:
        post["is_active"] = not post["is_active"]
        save_posts(posts)
        flash(f'Post "{post["title"]}" is now {"active" if post["is_active"] else "inactive"}!', 'success')
    return redirect(url_for('posts.get_posts'))