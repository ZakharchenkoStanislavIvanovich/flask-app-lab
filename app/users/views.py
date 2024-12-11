from . import bp
from flask import render_template, redirect, request, url_for, session, flash

# Статично задані облікові дані
VALID_USERNAME = "admin"
VALID_PASSWORD = "12345"

@bp.route("/profile")
def get_profile():
    if "username" in session:
        username_value = session["username"]
        return render_template("profile.html", username=username_value)
    flash("Invalid session. Please log in.", "danger")
    return redirect(url_for("user_name.login"))

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
    #response.set_cookie('username', 'student', expires=datetime.now()+timedelta(seconds=10))
    response.set_cookie('username', 'student', max_age=timedelta(seconds=60))
    response.set_cookie('color', max_age=timedelta(seconds=60))
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