#!/usr/bin/python

from psycopg2 import connect, OperationalError, errors
from random import shuffle

USER = 'kokot300'
PASSWORD = ''
HOST = 'localhost'
DATABASE = 'quiz_db'


class Question:
    @classmethod
    def creator(cls, question, aaa, bbb, ccc, ddd, correct, category_id):
        if not isinstance(question, str):
            return 'classmethod says: question must be a string'
        if not isinstance(aaa, str) or len(aaa) > 60:
            return 'classmethod says: aaa must be a string of 60 chars max'
        if not isinstance(bbb, str) or len(bbb) > 60:
            return 'classmethod says: bbb must be a string of 60 chars max'
        if not isinstance(ccc, str) or len(ccc) > 60:
            return 'classmethod says: aaa must be a string of 60 chars max'
        if not isinstance(ddd, str) or len(ddd) > 60:
            return 'classmethod says: ddd must be a string of 60 chars max'
        if not isinstance(correct, str) or len(correct) > 60:
            return 'classmethod says: correct must be a string of 1 char max'
        if category_id:
            pass
        return cls(question, aaa, bbb, ccc, ddd, correct, category_id)

    def __init__(self, question, aaa, bbb, ccc, ddd, correct, category_id, idd=-1):
        self.question = question
        self.aaa = aaa
        self.bbb = bbb
        self.ccc = ccc
        self.ddd = ddd
        self.correct = correct
        self.category_id = category_id  # provisory
        self.id = idd

    def add_to_db(self):
        command = f'''INSERT INTO questions(question, aaa, bbb, ccc, ddd, correct, category_id) VALUES (%s, %s, %s, %s, %s, %s, %s);'''
        tlp = (self.question, self.aaa, self.bbb, self.ccc, self.ddd, self.correct, self.category_id)
        cursor = Question.connect_me()
        try:
            cursor.execute(command, tlp)
        except OperationalError as e:
            print(e)
            return f'{e}'
        except errors.UniqueViolation as e:
            return f'{e}'
        else:
            cursor.close()
            return 'added'

    @staticmethod
    def get_from_class_id(question_id):
        command = '''SELECT question, aaa, bbb, ccc, ddd, correct, category_id, id FROM questions WHERE id = %s;'''
        tlp = (question_id,)
        cursor = Question.connect_me()
        try:
            cursor.execute(command, tlp)
            data = cursor.fetchone()  # tuple
        except OperationalError as e:
            print(e)
            return f'{e}'
        else:
            cursor.close()
            if data is not None:
                new_question = Question(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])
                return new_question

    @staticmethod
    def connect_me():
        try:
            cnx = connect(
                user=USER,
                password=PASSWORD,
                host=HOST,
                database=DATABASE
            )
            cnx.autocommit = True
            cursor = cnx.cursor()
            return cursor
        except OperationalError as e:
            print(e)
            return f'{e}'

    def __str__(self):
        return f'{self.id}/{self.question}/{self.aaa}/{self.bbb}/{self.ccc}/{self.ddd}/{self.correct}/{self.category_id}'

    @staticmethod
    def get_5_random(category=None):
        cursor = Question.connect_me()
        if category is None:
            command = '''SELECT id FROM questions;'''
            try:
                cursor.execute(command)
                data = cursor.fetchall()  # list of tuples
            except OperationalError as e:
                print(e)
                return f'{e}'

        else:
            command = '''SELECT id FROM questions WHERE category_id = %s;'''
            tlp = (category,)

            try:
                cursor.execute(command, tlp)
                data = cursor.fetchall()  # tuple
            except OperationalError as e:
                print(e)
                return f'{e}'
        cursor.close()
        shuffle(data)
        print('data in models', data)
        return data[0:5]


class Category:
    @classmethod
    def creator(cls, name):
        if len(name) <= 60:
            return cls(name)

    def __init__(self, name):
        self.name = name
        self.id = -1

    @staticmethod
    def connect_me():
        try:
            cnx = connect(
                user=USER,
                password=PASSWORD,
                host=HOST,
                database=DATABASE
            )
            cnx.autocommit = True
            cursor = cnx.cursor()
            return cursor
        except OperationalError as e:
            print(e)
            return f'{e}'

    def add_to_db(self):
        command = f'''INSERT INTO categories(name) VALUES (%s);'''
        tlp = (self.name,)
        cursor = Question.connect_me()
        try:
            cursor.execute(command, tlp)
        except OperationalError as e:
            print(e)
            return f'{e}'
        except errors.UniqueViolation as e:
            return f'{e}'
        else:
            cursor.close()
            return 'added'

    @staticmethod
    def validate_category(name):
        command = f"""SELECT * FROM categories WHERE name = %s;"""
        tlp = (name,)
        cursor = Question.connect_me()
        try:
            cursor.execute(command, tlp)
        except OperationalError as e:
            print(e)
            return f'{e}'
        else:
            data = cursor.fetchone()
            cursor.close()
            print(data)
            if data is None:
                return False
            return True

    @staticmethod
    def get_cat_by_name(name):
        command = f"""SELECT id FROM categories WHERE name = %s;"""
        tlp = (name,)
        cursor = Question.connect_me()
        try:
            cursor.execute(command, tlp)
        except OperationalError as e:
            print(e)
            return f'{e}'
        else:
            data = cursor.fetchone()
            cursor.close()
            print(data)
            return data

    @staticmethod
    def get_all_cat():
        command = f"""SELECT name FROM categories;"""
        cursor = Question.connect_me()
        try:
            cursor.execute(command)
        except OperationalError as e:
            print(e)
            return f'{e}'
        else:
            data = cursor.fetchall()
            cursor.close()
            return data

    def __str__(self):
        return f'{self.id}, {self.name}'


if __name__ == '__main__':
    pass
    # q = Question('kto jest najpiękniejszy na świecie?', 'ja', 'ty', 'on', 'ona', 'a', 1)
    # q.add_to_db()
    # q = Question.get_from_class_id(2)
    # print(q)
    # q = Question.creator('kto jest najsilniejszy na świecie?', 'ja', 'ty', 'on', 'ona', 'd', 1)
    # print(q)
    # q.add_to_db()
    # q = Question.get_5_random()
    # print(q[0][0])
    # Category.validate_category('głupie')
