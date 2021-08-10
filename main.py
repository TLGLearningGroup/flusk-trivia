#!/usr/bin/python3
# An object of Flask class is our WSGI application
from flask import Flask
from flask import redirect
from flask import url_for
from flask import request
from flask import render_template
import requests

# Flask constructor takes the name of current
# module (__name__) as argument
app = Flask(__name__)

# route() function of the Flask class is a
# decorator, tells the application which URL
# should call the associated function
@app.route("/")
def home():
   return render_template("home.html")

@app.route("/getquestion", methods = ["POST"])
def get_question():
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

    # print(requests_config)

    url = "https://opentdb.com/api.php?"

    res = requests.get(url, params=requests_config)

    res_dict = res.json()
    # return redirect(url_for("render_question"))

    # print(res_dict["results"])
    # print("#@#########",res_dict["results"][0]["qeustion"])
    return render_template("question.html", results = res_dict["results"])

@app.route("/question")
def render_question():
    return render_template("question.html")





@app.route("/login", methods = ["POST", "GET"])
def login():
    # POST would likely come from a user interacting with postmaker.html
    if request.method == "POST":
        if request.form.get("nm"): # if nm was assigned via the POST
            user = request.form.get("nm") # grab the value of nm from the POST
        else: # if a user sent a post without nm then assign value defaultuser
            user = "defaultuser"
    # GET would likely come from a user interacting with a browser
    elif request.method == "GET":
        if request.args.get("nm"): # if nm was assigned as a parameter=value
            user = request.args.get("nm") # pull nm from localhost:5060/login?nm=larry
        else: # if nm was not passed...
            user = "defaultuser" # ...then user is just defaultuser
    return redirect(url_for("success", name = user)) # pass back to /success with val for name





if __name__ == "__main__":
   app.run(host="0.0.0.0", port=2224) # runs the application
   # app.run(host="0.0.0.0", port=2224, debug=True) # DEBUG MODE

