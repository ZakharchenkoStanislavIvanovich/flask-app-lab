from . import bp
from flask import render_template, redirect, request, url_for, session, flash, make_response
from datetime import timedelta

# Статично задані облікові дані
VALID_USERNAME = "admin"
VALID_PASSWORD = "12345"

@bp.route("/profile", methods=["GET", "POST"])
def get_profile():
    if "username" not in session:
        flash("Invalid session. Please log in.", "danger")
        return redirect(url_for("user_name.login"))

    username_value = session["username"]
    cookies = request.cookies

    # Отримання вибраної кольорової схеми
    color_scheme = cookies.get("color_scheme", "light")

    if request.method == "POST":
        action = request.form.get("action")
        key = request.form.get("key")
        value = request.form.get("value")
        max_age = request.form.get("max_age", type=int)

        if action == "add" and key and value:
            response = make_response(render_template("profile.html", username=username_value, cookies=cookies, color_scheme=color_scheme))
            response.set_cookie(key, value, max_age=max_age)
            flash(f"Кукі '{key}' успішно додано.", "success")
            return response

        if action == "delete" and key:
            response = make_response(render_template("profile.html", username=username_value, cookies=cookies, color_scheme=color_scheme))
            response.set_cookie(key, '', expires=0)
            flash(f"Кукі '{key}' успішно видалено.", "success")
            return response

        if action == "delete_all":
            response = make_response(render_template("profile.html", username=username_value, cookies=cookies, color_scheme=color_scheme))
            for cookie_key in request.cookies.keys():
                response.set_cookie(cookie_key, '', expires=0)
            flash("Усі кукі успішно видалено.", "success")
            return response

    return render_template("profile.html", username=username_value, cookies=cookies, color_scheme=color_scheme)

@bp.route("/set_color_scheme/<string:color>")
def set_color_scheme(color):
    if color not in ["light", "dark"]:
        flash("Недійсна кольорова схема.", "danger")
        return redirect(url_for("user_name.get_profile"))

    response = make_response(redirect(url_for("user_name.get_profile")))
    response.set_cookie("color_scheme", color, max_age=timedelta(days=30))
    flash(f"Кольорова схема змінена на '{color}'.", "success")
    return response

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Перевірка введених облікових даних
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session["username"] = username
            flash("Вхід успішний!", "success")
            return redirect(url_for("user_name.get_profile"))
        else:
            flash("Невірне ім'я користувача або пароль.", "danger")
    
    return render_template("login.html")

@bp.route('/logout')
def logout():
    # Видалення користувача із сесії
    session.pop('username', None)
    flash("Ви вийшли з системи.", "info")
    return redirect(url_for("user_name.login"))

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

@bp.route('/set_cookie')
def set_cookie():
    response = make_response('Кукі встановлений')
    response.set_cookie('username', 'student', max_age=timedelta(seconds=60))
    response.set_cookie('color', 'blue', max_age=timedelta(seconds=60))
    return response

@bp.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username')
    return f'Користувач: {username}'

@bp.route('/delete_cookie')
def delete_cookie():
    response = make_response ('Кукі видалений')
    response.set_cookie('username', '', expires=0) #response.set_cookie('username', '', max_age=0)
    return response
