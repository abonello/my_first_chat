import os
from datetime import datetime
from flask import Flask, redirect, render_template, request

app = Flask(__name__)
messages = []

def add_messages(username, message):
    '''Add messages to the `messages` list.'''
    now = datetime.now().strftime("%H:%M:%S")
    message_dict = {"timestamp": now, "from": username, "message": message}
    # messages.append("({}) {}: {}".format(now, username, message))
    messages.append(message_dict)

def get_all_messages():
    '''Get all of the messages and separate them by a `br`.'''
    # return "<br>".join(messages)
    return messages

@app.route('/', methods=['GET', 'POST'])
def index():
    """Main Page with instructions."""
    if request.method == "POST":
        # print(request.form)
        with open("data/users.txt", "a") as user_list:
            user_list.write(request.form["username"])
        return redirect(request.form["username"])
    # return "<h1>Hello World</h1>"
    # return "To send a message use /USERNAME/MESSAGE"
    return render_template("index.html")

# Like a personalised home page for each user. Each user will have their URL.   
@app.route('/<username>')
def user(username):
    '''Display chat messages.'''
    # return "Welcome, {0}. <br>{1}".format(username, messages)
    return "<h1>Welcome, {0}</h1>{1}".format(username, get_all_messages())
    
@app.route('/<username>/<message>')
def send_message(username, message):
    '''Create a new message and redirect back to the caht page.'''
    add_messages(username, message)
    # return "{0} says: {1}".format(username, message)
    return redirect(username)
    
app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)