#!/usr/bin/python3
import os
from flask import Flask
from flask import redirect
from flask import url_for
from flask import request
from flask import render_template
from modules.handlers import get_question
from modules.handlers import check_answer

app = Flask(__name__)

# route() function of the Flask class is a
@app.route("/")
def home():
   return render_template("home.html")

@app.route("/getquestion", methods = ["POST"])
def getquestion():

    return get_question()

@app.route("/checkanswer", methods = ["POST"])
def checkanswer():
    return check_answer()




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




port = int(os.environ.get('PORT', 2224))


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=port, debug=False) # runs the application
   # app.run(host="0.0.0.0", port=2224, debug=True) # DEBUG MODE

