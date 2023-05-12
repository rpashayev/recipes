from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import like

@app.route('/recipes/like/<int:recipe_id>')
def like_recipe(recipe_id):
    if 'id' not in session:
        return redirect('/logout')
    
    data = {
        'user_id': session['id'],
        'recipe_id': recipe_id
    }
    like.Like.give_like(data)
    
    return redirect('/recipes')

@app.route('/recipes/unlike/<int:recipe_id>')
def unlike_recipe(recipe_id):
    if 'id' not in session:
        return redirect('/logout')
    
    data = {
        'user_id': session['id'],
        'recipe_id': recipe_id
    }
    like.Like.withdraw_like(data)
    
    return redirect('/recipes')