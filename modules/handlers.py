from flask import Flask
from flask import redirect
from flask import url_for
from flask import request
from flask import render_template
import requests
import random
import html.parser as htmlparser
parser = htmlparser.HTMLParser()


questions_list = []


def get_question():
    global questions_list
    amount_value = request.form.get("trivia_amount")
    category_value = request.form.get("trivia_category")
    difficulty_value = request.form.get("trivia_difficulty")
    type_value = request.form.get("trivia_type")

    requests_config = {
        "amount" : None if amount_value == "any" else amount_value,
        "category" : None if category_value == "any" else category_value,
        "difficulty" : None if difficulty_value == "any" else difficulty_value,
        "type": None if type_value == "any" else type_value
    }


    url = "https://opentdb.com/api.php?"

    res = requests.get(url, params=requests_config)

    res_dict = res.json()

    print(res_dict["results"][0])
    for result in res_dict["results"]:
        result["answers"] = result["incorrect_answers"]
        result["answers"].append(result["correct_answer"])
        random.shuffle(result["answers"])
        # remove url escape code
        result["answers"] = parser.unescape(result["answers"])
        
        result["question"] = parser.unescape(result["question"])


    questions_list = res_dict["results"].copy()
    
    return render_template("question.html", questions = questions_list)


def check_answer():
    global questions_list

    total_question_count = len(questions_list)
    correct_answer_count = 0
    print(questions_list)
    for key in request.form:
        user_answer = request.form.get(key)
        print(f"{key}  :  {user_answer}")

        if user_answer == questions_list[int(key)]["correct_answer"]:
            correct_answer_count += 1
    
    return render_template("answer.html", total_count=total_question_count, correct_count=correct_answer_count)