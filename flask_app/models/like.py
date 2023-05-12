from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user

class Like:
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
            INTO likes(user_id, recipe_id)
            VALUES ( %(user_id)s, %(recipe_id)s );
        '''
        
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def withdraw_like(cls, data):
        query = '''
            DELETE
            FROM likes
            WHERE user_id = %(user_id)s AND recipe_id = %(recipe_id)s;
        '''
        
        return connectToMySQL(cls.DB).query_db(query, data)
    
