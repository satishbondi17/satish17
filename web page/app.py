from flask import Flask, render_template, request, session
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

app.secret_key = "satish"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Satish@17"
app.config["MYSQL_DB"] = "satish"

mysql = MySQL(app)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    message = ""
    if (request.method == "POST" and
            "uid" in request.form and
            "pass" in request.form and
            "name" in request.form and
            "email" in request.form and
            "phno" in request.form and
            "gn" in request.form):

        UserId = request.form["uid"]
        Password = request.form["pass"]
        Fullname = request.form["name"]
        Email = request.form["email"]
        PhoneNo = request.form["phno"]
        Gender = request.form["gn"]

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("INSERT INTO student VALUES(%s,%s,%s,%s,%s,%s)",
                    (UserId, Password, Fullname, Email, PhoneNo, Gender))
        mysql.connection.commit()

        message = "Successfully Created Account"
        return render_template("home.html", msg=message)
    else:
        message = "Please Enter the Form"

    return render_template("register.html", msg=message)


@app.route("/login", methods=["POST", "GET"])
def login():
    message = ""
    if (request.method == "POST" and
            "uid" in request.form and
            "pass" in request.form):
        UserId = request.form["uid"]
        Password = request.form["pass"]

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM student WHERE userid=%s and password=%s", (UserId, Password))
        user = cur.fetchone()

        if user:
            session["LoggedIn"] = True
            session["userId"] = user["userId"]
            session["password"] = user["password"]
            session["fullname"] = user["fullname"]
            session["Email"] = user["Email"]
            session["phoneNo"] = user["phoneNo"]
            session["Gender"] = user["Gender"]

            message = "Successfully Logged In"
            return render_template("dashboard.html")
        else:
            message = "Please enter valid userid/password"
            return render_template("Login.html", msg=message)

    return render_template("Login.html", msg=message)


@app.route('/logout')
def logout():
    session.pop('userId', None)
    message = "Successful logout!!"
    return render_template("home.html", msg=message)
@app.route("/delete", methods=["POST", "GET"])
def delete():
    message = ""
    if (request.method == "POST" and
            "uid" in request.form and
            "pass" in request.form):
        UserId = request.form["uid"]
        Password = request.form["pass"]

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("DELETE TABLE student WHERE userid=%s and password=%s", (UserId, Password))
        user = cur.fetchone()

        if user:
            session["LoggedIn"] = True
            session["userId"] = user["userId"]
            session["password"] = user["password"]
            session["fullname"] = user["fullname"]
            session["Email"] = user["Email"]
            session["phoneNo"] = user["phoneNo"]
            session["Gender"] = user["Gender"]

            message = "deleted suceessfully!!"
            return render_template("home.html",msg=message)
        else:
            message = "Please enter valid userid/password"
            return render_template("Login.html", msg=message)

    return render_template("Login.html", msg=message)

@app.route("/update", methods=["POST", "GET"])

def update():
    message = ""
    if (request.method == "POST" and
            "uid" in request.form and
            "pass" in request.form):
        UserId = request.form["uid"]
        Password = request.form["pass"]

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("UPDATE TABLE student WHERE userid=%s and password=%s", (UserId, Password))
        user = cur.fetchone()

        if user:
            session["LoggedIn"] = True
            session["userId"] = user["userId"]
            session["password"] = user["password"]
            session["fullname"] = user["fullname"]
            session["Email"] = user["Email"]
            session["phoneNo"] = user["phoneNo"]
            session["Gender"] = user["Gender"]

            return render_template("register.html",msg=message)
            return "updated suceessfully!!"
        else:
            message = "Please enter valid userid/password"
            return render_template("Login.html", msg=message)

    return render_template("register.html", msg=message)





@app.route("/dash")
def dash():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)