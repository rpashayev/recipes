from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash
import re


class Comment:
    DB = 'receipe_schema'
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.recipe_id = data['recipe_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def give_like(cls, data):
        query = '''
            INSERT 
            INTO likes(user_id,recipe__id)
            VALUES (%(user_id)s, %(recipe__id)s);
        '''
        
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_likes(cls, data):
        all_comments = []
        query = '''
            SELECT *
            FROM comments
            JOIN posts ON posts.id = comments.post_id
            JOIN users ON users.id = comments.user_id
            WHERE posts.id = %(id)s
            ORDER BY comments.created_at; 
        '''
        
        results = connectToMySQL(cls.DB).query_db(query, data)
        
        for row in results:
            one_comment = cls(row)
            creator_info = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at'],
            }
            one_comment.creator = user.User(creator_info)
            all_comments.append(one_comment)
        
        return all_comments
