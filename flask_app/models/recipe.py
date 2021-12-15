from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash

class Recipe:
    def __init__ (self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date = data['date']
        self.under30 = data['under30']
        self.user_id = data['user_id']

    @classmethod
    def save(cls,data):
        query = 'INSERT INTO recipes (name,description,instructions,date,under30,user_id) VALUES (%(name)s,%(description)s,%(instructions)s,%(date)s,%(under30)s,%(user_id)s);'
        result = connectToMySQL('recipes').query_db(query,data)
        return result

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM recipes'
        result = connectToMySQL('recipes').query_db(query)
        recipes = []
        for row in result:
            recipes.append( cls(row) )
        return recipes

    @classmethod
    def update(cls,data):
        query = 'UPDATE recipes SET name=%(name)s,description=%(description)s,instructions=%(instructions)s,date=%(date)s,under30=%(under30)s WHERE id = %(id)s;'
        return connectToMySQL('recipes').query_db(query,data)

    @classmethod
    def get_one(cls,data):
        query = 'SELECT * FROM recipes WHERE id = %(id)s;'
        result = connectToMySQL('recipes').query_db(query,data)
        return cls(result[0])

    @classmethod
    def delete(cls,data):
        query = 'DELETE FROM recipes WHERE id = %(id)s;'
        return connectToMySQL('recipes').query_db(query,data)

    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data['name']) < 3:
            flash('Recipe name has to be 3 characters long.','recipe')
            is_valid = False
        if len(data['description']) < 3:
            flash('Recipe description has to be 3 characters long.','recipe')
            is_valid = False
        if len(data['instructions']) < 3:
            flash('Recipe instructions has to be 3 characters long.','recipe')
            is_valid = False
        if data['date'] == '':
            flash('Date input needed','recipe')
            is_valid = False
        return is_valid