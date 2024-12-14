from flask import (abort, request, redirect, url_for, render_template)
from . import app

@app.route('/')
def main():
    return render_template("base1.html")

@app.route('/homepage')
def home():
    """View for the Home page of your website."""
    agent = request.user_agent
    return render_template("home.html", agent=agent)


@app.route('/resume')
def resume():
    page_title = "Резюме"
    return render_template('resume.html', title=page_title)

@app.errorhandler(404)
def page_not_found(error):
    # Відображаємо шаблон 404.html і повертаємо статусний код 404
    return render_template('404.html'), 404