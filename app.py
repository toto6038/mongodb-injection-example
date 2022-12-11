from flask import Flask, render_template, redirect, url_for, request
import pymongo
app = Flask(__name__)
conn_str = "mongodb://root:example@localhost:27017/?authMechanism=DEFAULT"
try:
    client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
    client.server_info()
except Exception:
    print("Unable to connect mongodb.")
    exit(1)

isLoggedIn: bool = False
db = client['mydb']
accounts = db.accounts


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.get("/login")
def login():
    return render_template("login.html")


@app.post("/login")
def do_login():
    data = request.form
    username = data.get('username')
    password = data.get('password')
    query = {
        "$where": "function (){ return this.username==" + f"'{username}'" + "&& this.password==" + f"'{password}'" + "}"
    }
    print(accounts.find_one(query))
    result = accounts.find_one(query)
    if result:
        global isLoggedIn
        isLoggedIn = True

        return redirect(url_for("user", username=result['username']))
    return redirect(url_for("login"))


@app.route("/user/<username>")
def user(username):
    global isLoggedIn
    if not isLoggedIn:
        return render_template("error.html")
    else:
        isLoggedIn = False
        return render_template("user.html", username=username)


if __name__ == "__main__":
    app.run(debug=True)
