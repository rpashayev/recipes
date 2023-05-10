from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import like

@app.route('/posts/comments/create', methods=['POST'])
def create_comment():
    if not like.Comment.validate_comment(request.form):
        return redirect('/wall')
    
    data = {
        'content': request.form['content'],
        'user_id': session['id'],
        'post_id': request.form['post_id']
    }
    like.Comment.save_comment(data)
    
    return redirect('/wall')
