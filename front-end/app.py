from flask import Flask, render_template, url_for, request, session, redirect, flash
from flask_pymongo import PyMongo

import bcrypt


#intitalize flask app
app = Flask(__name__, static_url_path='/static')



app.config['MONGO_DBNAME'] = 'Users'
app.config['MONGO_URI'] = 'mongodb+srv://admin:admin@cluster0.1f9yj.mongodb.net/Users?retryWrites=true&w=majority'
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]

mongo = PyMongo(app)

    
logged_in = False

@app.route('/')
def index():
    if logged_in:
        return redirect( url_for('product'))
    return render_template('index.html')
"""    if session['logged_in']:
        return redirect( url_for('product'))"""
    

@app.route('/about')
def aboutUs():
    return render_template('about.html')

@app.route('/prod', methods=["GET", "POST"])
def product():
    if request.method == 'POST':
        if request.files:
            person = request.files['img_person']
            article = request.files['img_article']
            return redirect(url_for('solution'))
    
    return render_template('product.html')


@app.route('/soln')
def solution():
    return render_template('solution.html')

@app.route('/signin', methods = ['POST'])
def signIn():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'email': request.form['email']})

        if login_user:
            if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
                session['username'] = login_user['username']
                logged_in = True
                return redirect(url_for('product'))
        else:
            
            flash('Invalid username/password')
            return render_template('index.html')
     
    return render_template('index.html')  



    


@app.route('/signup', methods = ['POST', 'GET'])
def signUp():
    if logged_in:
        return redirect( url_for('product'))
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'username': request.form['username']})
        
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name': request.form['name'], 'username': request.form['username'], 'email': request.form['email'], 'password': hashpass })
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            
            flash("That username is already taken, please choose another")
            return render_template('signup.html')
    
    return render_template('signup.html')    

if __name__ == "__main__":
    app.secret_key = 'secret'
    app.run(debug=True)
