from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)
app.config.from_pyfile("config.py")

@app.route('/')
def main():
    return render_template("hello.html")

@app.route('/homepage')
def home():
    """View for the Home page of your website."""
    agent = request.user_agent
    return render_template("home.html", agent=agent)

@app.route('/hi/<string:name>') #/hi/stas?age=30
def greetings(name):
    name = name.upper()
    age = request.args.get("age", 0, type=int)

    return f"Welcome (name=) (age=)", 200

@app.route('/admin')
def admin():
    to_url = url_for("greetings", name="administrator", _external=True)  #http://localhost:8080/hi/administrator"
    print(to_url)
    return redirect(to_url)

@app.route('/resume')
def resume():
    page_title = "Резюме"
    return render_template('resume.html', title=page_title)

if __name__ == '__main__':
    app.run(debug=True)
