from . import bp
from flask import render_template, redirect, request, url_for

@bp.route('/hi/<string:name>') #/hi/stas?age=30
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, type=int)

    return render_template("hi.html",
                           name=name, age=age)

@bp.route('/admin')
def admin():
    to_url = url_for("user_name.greetings", name="administrator", age=45, _external=True) #http://localhost:8080/hi/administrator"
    print(to_url)
    return redirect(to_url)