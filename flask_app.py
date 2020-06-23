#!/usr/bin/python

from flask import Flask, render_template, request
from models import Question, Category

app = Flask(__name__)

questions_lst2 = []


@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        return render_template('index.html')


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    global questions_lst2
    categories = Category.get_all_cat()
    if request.method == 'GET':
        return render_template('quiz_select_cat.html', categories=categories)
    else:
        where = request.form.get('where')
        if where == '0':
            questions_lst2 = []
            category = request.form.get('category')
            if category == 'All':
                category = None
            else:
                category = Category.get_cat_by_name(category)
                category = category[0]
                print(category)
            questions_lst = Question.get_5_random(category)
            print(questions_lst)
            for idd in questions_lst:
                ask = Question.get_from_class_id(idd)
                ask = str(ask)
                ask_lst = ask.split('/')
                questions_lst2.append(ask_lst)
            return render_template('quiz_challenge.html', questions_lst2=questions_lst2)
        elif where == '1':
            answer_lst = []
            try:
                for answer in questions_lst2:
                    ans = answer[6]
                    answer_lst.append(ans)
                question_id_lst = []
                for question_id in questions_lst2:
                    ques = question_id[0]
                    question_id_lst.append(ques)

                user_answers = []
                first_question = request.form.get(question_id_lst[0])
                second_question = request.form.get(question_id_lst[1])
                third_question = request.form.get(question_id_lst[2])
                fourth_question = request.form.get(question_id_lst[3])
                fifth_question = request.form.get(question_id_lst[4])
                user_answers.append(first_question)
                user_answers.append(second_question)
                user_answers.append(third_question)
                user_answers.append(fourth_question)
                user_answers.append(fifth_question)
                print(user_answers)

                score = 0
                for i in range(5):
                    if user_answers[i] == answer_lst[i]:
                        score += 1

                return render_template('quiz_results.html', questions_lst2=questions_lst2, user_answers=user_answers,
                                       score=score)
            except IndexError:
                return render_template('quiz_select_cat.html', categories=categories)
        else:
            return render_template('quiz_select_cat.html', categories=categories)


@app.route('/quiz_api', methods=['GET', 'POST'])
def quiz_api():
    if request.method == 'GET':
        return render_template('quiz_api.html')
    else:
        return render_template('quiz_api.html')


@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        categories = Category.get_all_cat()
        return render_template('add_question.html', categories=categories)
    else:
        categories = Category.get_all_cat()
        question = request.form.get('question')
        a = request.form.get('a').lower()
        b = request.form.get('b').lower()
        c = request.form.get('c').lower()
        d = request.form.get('d').lower()
        correct = request.form.get('correct').lower()

        category = request.form.get('category').lower()
        category = Category.get_cat_by_name(category)
        category = category[0]

        print(question, a, b, c, d, correct, category)

        msg = Question.creator(question, a, b, c, d, correct, category)
        print(msg)

        return render_template('add_question.html', categories=categories, msg=msg.add_to_db())


@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if request.method == 'GET':
        return render_template('add_category.html')
    else:
        candidate = request.form.get('category').lower()
        new_cat = Category.creator(candidate)

        return render_template('add_category.html', msg=new_cat.add_to_db())


if __name__ == '__main__':
    app.run(debug=True)
