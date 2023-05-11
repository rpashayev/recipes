from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import like

@app.route('/recipes/like/<int:recipe_id>', methods=['POST'])
def like_recipe(recipe_id):
    if 'id' not in session:
        return redirect('/logout')
    
    data = {
        'user_id': session['id'],
        'recipe_id': recipe_id
    }
    print(data)
    like.Like.give_like(data)
    
    return redirect('/recipes')
