from flask_app import app
from flask import render_template,flash,redirect,request,session
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.post("/register")
def validate():
    if User.validate_registration(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form["password"])
        data = {
        "first_name":request.form["first_name"],
        "last_name":request.form["last_name"],
        "email":request.form["email"],
        "password":pw_hash,
        }
        id = User.save(data)
        flash("User created!", "register")  
        session["user_id"] = id
        return redirect("/dashboard")
    else:
        return redirect("/")

@app.post('/login')
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email/Password","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Email/Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    flash("logged out!", "login")
    return redirect('/')