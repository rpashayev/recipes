from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import recipe, user

@app.route('/recipes')
def start_page():
    if 'id' not in session:
        return redirect('/logout')
    id = {
        'id': session['id']
    }
    return render_template('recipes.html', all_recipes = recipe.Recipe.get_all_recipes(), one_user = user.User.get_one_user(id))

@app.route('/recipes/create')
def show_create_page():
    if 'id' not in session:
        return redirect('/logout')
    return render_template('new_recipe.html')

@app.route('/recipes/save', methods=['POST'])
def create_recipe():
    if not recipe.Recipe.validate_recipe(request.form):
        return redirect('/recipes/create')
    
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_cooked': request.form['date_cooked'],
        'long_cooking': request.form['long_cooking'],
        'user_id': session['id']
    }
    
    recipe.Recipe.save_recipe(data)
    
    return redirect('/recipes')

@app.route('/recipes/edit/<int:recipe_id>')
def show_edit_page(recipe_id):
    if 'id' not in session:
        return redirect('/logout')    
    data = {
        'id': recipe_id
    }
    return render_template('edit_recipe.html', recipe=recipe.Recipe.get_one_recipe(data))

@app.route('/recipes/edit', methods=['POST'])
def edit_recipe():
    if not recipe.Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/edit/{request.form["id"]}')
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_cooked': request.form['date_cooked'],
        'long_cooking': request.form['long_cooking'],
        'id': request.form['id'] 
    }
    
    recipe.Recipe.edit_recipe(data)
    
    return redirect('/recipes')

@app.route('/recipes/delete/<int:recipe_id>')
def delete_one_recipe(recipe_id):
    if 'id' not in session:
        return redirect('/logout')    
    data = {
        'id': recipe_id
    }
    
    recipe.Recipe.delete_recipe(data)
    
    return redirect('/recipes')



@app.route('/recipes/view/<int:recipe_id>')
def show_one_recipe(recipe_id):
    if 'id' not in session:
        return redirect('/logout')
    data = {
        'id': recipe_id
    }
    
    user_id = {
        'id': session['id']
    }
    return render_template('view_recipe.html', recipe=recipe.Recipe.get_one_recipe(data), user=user.User.get_one_user(user_id))
