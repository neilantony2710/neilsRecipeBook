from flask import *
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///neilsrb.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secret"
Bootstrap(app)
db = SQLAlchemy(app)


# User Information Schema
class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, fname, lname, email, password):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = password

# Recipe Schema
class recipies(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    cookTime = db.Column(db.Integer)
    hardness = db.Column(db.String(100))
    instructions = db.Column(db.String(5000))
    user = db.Column(db.String(100))

    def __init__(self, title, cookTime, hardness, instructions, user):
        self.title = title
        self.cookTime = cookTime
        self.hardness = hardness
        self.instructions = instructions
        self.user = user
with app.app_context():
    db.create_all()
@app.route("/", methods=["GET", "POST"])
def home():
    if "login" in session:
        if request.method == "GET":
            Xrecipies = list(recipies.query.all())
            print(len(Xrecipies))
            for recipie in Xrecipies:
                if recipie.hardness == "Difficult":
                    recipie.color = "bg-danger"
                elif recipie.hardness == "Medium":
                    recipie.color = "bg-warning"
                else:
                    recipie.color = "bg-success"
            return render_template("index.html", r=Xrecipies, ab="1")
        elif request.method == "POST":
            Xtitle = request.form["title"]
            XcookTime = request.form["cookTime"]
            Xhardness = request.form["hardness"]
            Xinstructions = request.form["instructions"]
            Xuser = session["login"]
            rcp = recipies(Xtitle,XcookTime,Xhardness,Xinstructions,Xuser)
            db.session.add(rcp)
            db.session.commit()
            return redirect("/")
    else:
        return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        y = {}
        y["fname"] = request.form["firstname"].title()
        y["lname"] = request.form["lastname"].title()
        y["email"] = request.form["email"]
        y["password"] = request.form["password"]

        x = users.query.filter_by(email=y["email"]).first()
        print(x)
        # Checks if user is already registered based on email val
        if x is not None:
            flash("Account with E-Mail already created.")
            return redirect("/login")

        usr = users(y["fname"],y["lname"],y["email"],y["password"])
        print(usr.email)
        db.session.add(usr)
        db.session.commit()
        flash("Account created, Now login")
        return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if "login" in session:
            flash("You are already logged in.")
            return redirect("/")
        else:
            return render_template("login.html")
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        print(email)
        y = users.query.filter_by(email=email).first()
        print(y)
        if y is None:
            flash("incorrect email try again")
            return redirect("/login")
        elif y.password != password:
            flash("incorrect password try again")
            return redirect("/login")
        else:
            session["login"] = email
            flash("Success!")
        return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run()
    

