from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import like, user
from flask import flash
import re, datetime

RECIPE_REGEX = re.compile(r'^\s*$')

class Recipe:
    DB = 'receipe_schema'
    
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_cooked = data['date_cooked']
        self.long_cooking = data['long_cooking']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        self.creator = None
        self.users_liked = []
    
    @classmethod
    def get_all_recipes(cls):
        all_recipes = []
        query = '''
            SELECT *
            FROM recipes
            LEFT JOIN users ON users.id = recipes.user_id
            LEFT JOIN likes ON likes.recipe_id = recipes.id
            LEFT JOIN users AS liker ON liker.id = likes.user_id
            ORDER BY recipes.created_at DESC;
        '''
        results = connectToMySQL(cls.DB).query_db(query)

        for row in results:
            if not all_recipes or row['id'] != one_recipe.id:
                one_recipe = cls(row)
                creator_info = {
                    'id': row['users.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': row['password'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
                }
                one_recipe.creator = user.User(creator_info)
                all_recipes.append(one_recipe)
            
            if row['likes.id']:
                liker_info = {
                    'id': row['liker.id'],
                    'first_name': row['liker.first_name'],
                    'last_name': row['liker.last_name'],
                    'email': row['liker.email'],
                    'password': row['liker.password'],
                    'created_at': row['liker.created_at'],
                    'updated_at': row['liker.updated_at']
                }
                one_recipe.users_liked.append(user.User(liker_info))
        return all_recipes
    
    # @classmethod
    # def get_one_recipe(cls, data):
    #     query = '''
    #         SELECT *
    #         FROM recipes
    #         JOIN users ON users.id = recipes.user_id
    #         WHERE recipes.id = %(id)s;
    #     '''
    #     results = connectToMySQL(cls.DB).query_db(query, data)
        
    #     one_recipe = cls(results[0])
    #     for row in results:
    #         creator_info = {
    #             'id': row['users.id'],
    #             'first_name': row['first_name'],
    #             'last_name': row['last_name'],
    #             'email': row['email'],
    #             'password': row['password'],
    #             'created_at': row['users.created_at'],
    #             'updated_at': row['users.updated_at'],
    #         }
        
    #         one_recipe.creator = user.User(creator_info)
            
    #     return one_recipe
    
    @classmethod
    def get_one_recipe(cls, data):
        query = '''
            SELECT *
            FROM recipes
            LEFT JOIN users ON users.id = recipes.user_id
            LEFT JOIN likes ON likes.recipe_id = recipes.id
            LEFT JOIN users AS liker ON liker.id = likes.user_id
            WHERE recipes.id = %(id)s;
        '''
        results = connectToMySQL(cls.DB).query_db(query, data)

        one_recipe = cls(results[0])
        creator_info = {
            'id': results[0]['users.id'],
            'first_name': results[0]['first_name'],
            'last_name': results[0]['last_name'],
            'email': results[0]['email'],
            'password': results[0]['password'],
            'created_at': results[0]['users.created_at'],
            'updated_at': results[0]['users.updated_at'],
        }
        one_recipe.creator = user.User(creator_info)
        for row in results:
            if row['likes.id']:
                liker_info = {
                    'id': row['liker.id'],
                    'first_name': row['liker.first_name'],
                    'last_name': row['liker.last_name'],
                    'email': row['liker.email'],
                    'password': row['liker.password'],
                    'created_at': row['liker.created_at'],
                    'updated_at': row['liker.updated_at']
                }
                one_recipe.users_liked.append(user.User(liker_info))
        return one_recipe
    
    @classmethod
    def save_recipe(cls, data):
        query = '''
            INSERT 
            INTO recipes(name, description, instructions, date_cooked, long_cooking, user_id)
            VALUES ( %(name)s, %(description)s, %(instructions)s, %(date_cooked)s, %(long_cooking)s, %(user_id)s );
        '''
        
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def delete_recipe(cls, data):
        query = '''
            DELETE
            FROM recipes(recipes(name, description, instructions, date_cooked, long_cooking, user_id))
            WHERE id = %(id)s;
        '''
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def edit_recipe(cls, data):
        query = '''
            UPDATE recipes
            SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date_cooked=%(date_cooked)s, long_cooking=%(long_cooking)s
            WHERE id = %(id)s;
        '''
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['description']) == 0 or RECIPE_REGEX.match(recipe['description']):
            flash('Description cannot be empty!', 'recipe_error')
            is_valid = False
        if len(recipe['name']) == 0 or RECIPE_REGEX.match(recipe['name']):
            flash('Name cannot be empty!', 'recipe_error')
            is_valid = False
        if len(recipe['instructions']) == 0 or RECIPE_REGEX.match(recipe['instructions']):
            flash('Instruction cannot be empty!', 'recipe_error')
            is_valid = False
        if not recipe['date_cooked']:
            flash('Invalid date!', 'recipe_error')
            is_valid = False
        elif datetime.datetime.strptime(recipe['date_cooked'],'%Y-%m-%d') > datetime.datetime.now():
            flash('Cannot be future date', 'recipe_error')
            is_valid = False
        if 'long_cooking' not in recipe:
            flash('Please select cooking time!', 'recipe_error')
            is_valid = False
            
        return is_valid
