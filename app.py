from flask import *
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://neil1:neil1234@ds113853.mlab.com:13853/neilantony2710login?retryWrites=false"
app.config['SECRET_KEY'] = 'secret'
Bootstrap(app)
mongo = PyMongo(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    if 'login' in session:
        if request.method == 'GET':
            recipies = list(mongo.db.rbRecipies.find())
            for recipie in recipies:
                if recipie['hardness'] == 'Difficult':
                    recipie['color'] = 'bg-danger'
                elif recipie['hardness'] == 'Medium':
                    recipie['color'] = 'bg-warning'
                else:
                    recipie['color'] = 'bg-success'
            return render_template('index.html', r=recipies, ab='1')
        elif request.method == 'POST':
            inputRecipe = {}
            inputRecipe['title'] = request.form['title']
            inputRecipe['cookTime'] = request.form['cookTime']
            inputRecipe['hardness'] = request.form['hardness']
            inputRecipe['instructions'] = request.form['instructions']
            inputRecipe['user'] = session['login']
            print(inputRecipe)
            mongo.db.rbRecipies.insert_one(inputRecipe)
            return redirect('/')
    else:
        return redirect('/login')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        y = {}
        y['fname'] = request.form['firstname'].title()
        y['lname'] = request.form['lastname'].title()
        y['email'] = request.form['email']
        y['password'] = request.form['password']
        y['following'] = []
        y['followers'] = []
        y['schedule'] = {}
        print(y)
        x = mongo.db.rbUser.find_one({'email': y['email']})
        if x is not None:
            flash('Account with E-Mail already created.')
            return redirect('/login')
        mongo.db.rbUser.insert_one(y)
        flash('Account created, Now login')
        return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            flash('You are already logged in.')
            return redirect('/')
        else:
            return render_template('login.html')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        y = mongo.db.rbUser.find_one({'email': email, 'password': password})
        if y is None:

            flash('incorrect information')
            return redirect('/login')
        else:

            session['login'] = email


            flash('Success!')
        return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run()

# deploy using heroku, look at student portal, send link to Rohit after.

