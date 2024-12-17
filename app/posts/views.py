from . import post_bp
from flask import render_template, abort, flash, redirect, url_for, session, request
from .forms import PostForm
from .utils import load_posts, save_posts
import datetime
import json
from app.posts.models import Post
from app import db

@post_bp.route('/resume')
def resume():
    page_title = "Резюме"
    return render_template('resume.html', title=page_title)

#def load_posts():
#    try:
#        with open('posts.json', 'r') as file:
#            return json.load(file)
#    except FileNotFoundError:
#        return []
#    except json.JSONDecodeError:
#        return []
#
#def save_posts(posts):
#    with open('posts.json', 'w') as file:
#        json.dump(posts, file, indent=4)

@post_bp.route('/')
def get_posts():
    posts = Post.query.order_by(Post.publish_date.desc()).all()
#    posts = load_posts()
#    
#    for post in posts:
#        try:
#            post["publish_date"] = datetime.datetime.strptime(
#                post["publish_date"], '%Y-%m-%d'
#            ).strftime('%B %d, %Y')
#        except (ValueError, KeyError):
#            post["publish_date"] = "Unknown date"
    
    return render_template('posts.html', posts=posts)

@post_bp.route('/<int:id>')
def detail_post(id):
    post = Post.query.get_or_404(id)
    return render_template("detail_post.html", post=post)


@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit(): 
  
        post = Post(
            title=form.title.data,
            content=form.content.data,
            is_active=form.is_active.data,
            publish_date=form.publish_date.data,
            category=form.category.data,
            author="Author Name" 
        )
        
      
        db.session.add(post)
        db.session.commit()  
        
        flash(f'Post "{post.title}" added successfully!', 'success')
        return redirect(url_for('posts.get_posts'))
    return render_template('add_post.html', form=form)

@post_bp.route('/delete_post/<int:id>', methods=['POST'])
def delete_post(id):
    post_to_delete = Post.query.get(id)
    if post_to_delete:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash(f'Post "{post_to_delete.title}" has been deleted successfully!', 'success')
    else:
        flash(f'Post with ID {id} not found.', 'danger')
    return redirect(url_for('posts.get_posts'))


@post_bp.route('/toggle_active/<int:id>', methods=['POST'])
def toggle_active(id):
    post = Post.query.get(id)
    if post:
        post.is_active = not post.is_active
        db.session.commit()
        flash(f'Post "{post.title}" is now {"active" if post.is_active else "inactive"}!', 'success')
    else:
        flash(f'Post with ID {id} not found.', 'danger')
    return redirect(url_for('posts.get_posts'))

@post_bp.route('/edit_post/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Post.query.get_or_404(id) 
    form = PostForm(obj=post)

#    if request.method == 'GET' and post.publish_date:
#        form.publish_date.data = post.publish_date.strftime('%Y-%m-%dT%H:%M')

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.is_active = form.is_active.data
#        post.publish_date = datetime.strptime(form.publish_date.data, '%Y-%m-%dT%H:%M')
        post.category = form.category.data

        db.session.commit()
        flash(f'Post "{post.title}" has been updated successfully!', 'success')
        return redirect(url_for('posts.get_posts'))

    return render_template('edit_post.html', form=form, post=post)