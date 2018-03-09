import os
from flask import Flask

app = Flask(__name__)
messages = []

def add_messages(username, message):
    messages.append("{}: {}".format(username, message))

@app.route('/')
def index():
    """Main Page with instructions."""
    # return "<h1>Hello World</h1>"
    return "To send a message use /USERNAME/MESSAGE"

# Like a personalised home page for each user. Each user will have their URL.   
@app.route('/<username>')
def user(username):
    '''Display chat messages.'''
    return "Welcome, {0}. <br>{1}".format(username, messages)
    
@app.route('/<username>/<message>')
def send_message(username, message):
    '''Create a new message and redirect back to the caht page.'''
    # add_messages(username, message)
    return "{0} says: {1}".format(username, message)
    
app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)