from flask import Flask, render_template, request, redirect, session

from flask_app import app

from flask_app.models.recipe import Recipe
from flask_app.models.user import User

@app.route('/recipes')
def recipesIndex():
    return render_template('new.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template('dashboard.html',user = User.get_by_id(data), recipes = Recipe.get_all())

@app.post('/new')
def add():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes')
    data = {
        'user_id' : session['user_id'],
        ** request.form
    }
    print(data)
    Recipe.save(data)
    return redirect('/dashboard')

@app.post('/update/<int:id>')
def update(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/edit/{id}')
    data = {
        'id':id,
        **request.form
    }
    Recipe.update(data)
    return redirect('/dashboard')

@app.route('/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id':id
    }
    return render_template('edit.html',recipe = Recipe.get_one(data))

@app.route('/instructions/<int:id>')
def instructions(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id':id
    }
    return render_template('instructions.html',user = User.get_by_id(data),recipe = Recipe.get_one(data))

@app.route('/delete/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id':id
    }
    Recipe.delete(data)
    return redirect('/dashboard')