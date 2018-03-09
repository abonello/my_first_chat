# Flask Chat App

This is a chat application written using Flask. The purpose of this project is 
to take data from a URL (user names and chat messages) and store it in a Python 
list. Once we get beyond that then we can look at the possibility of storing it 
in a JSON file or some other type of file maybe CSV.  
We will also need to render that information back out to all users
(display on the browser) along with the timestamp. Anybody who has this 
application open can see the messages.

After initialising git
~~~~ 
git init 
~~~~

**Install Flask**.

I create the **run.py** file. This will be my Flask application.

fundamental imports

~~~~python
import os
from flask import Flask
~~~~

create flask application
~~~~python
app = Flask(__name__)
~~~~

create first route for ROOT:
~~~~python
@app.route('/')
def index():
    return "<h1>Hello World</h1>"
~~~~

Prepare the app to run
~~~~python
app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)
~~~~
This is like the OS.get.environment but a bit shorter. It will get the IP 
address and the PORT.

Create requirements.txt file
~~~~
pip3 freeze --local >requirements.txt
~~~~
requirements.txt file will allow anybody else who is cloning our repository to 
install all requirements.  
Note that when we install Flask, it will install its own requirements as well.

## Implementing basic Vies and Routing
~~~~python
@app.route('/')
def index():
    """Main Page with instructions."""
    # return "<h1>Hello World</h1>"
    return "To send a message use /USERNAME/MESSAGE"

# Like a personalised home page for each user. Each user will have their URL.   
@app.route('/<username>')
def user(username):
    return "Hi " + username
    
@app.route('/<username>/<message>')
def send_message(username, message):
    return "{0} says: {1}".format(username, message)
~~~~

* * *
## Next steps

We want to be able to actually take this information (name / message) and store 
it in a list.

We want to be able to store our lists in our chat items in a python list. 
1. Create an empty list called **messages**.
    ~~~~python
    messages = []
    ~~~~
2. Create a new function called **add_messages**. This is going to take in two parameters,
    username and message.  
    Inside this function we will use an append method:
    ~~~~python
    def add_messages(username, message):
        messages.append("{}: {}".format(username, message))
    ~~~~
    that will store the username and message inside of the messages list.

Update the info returned by the user function to show any stored messages.

Now the function send_message will store the message in messages list and then 
redirects to user function. We need to import redirect.
~~~~python
from flask import Flask, redirect
~~~~

~~~~python
@app.route('/<username>/<message>')
def send_message(username, message):
    '''Create a new message and redirect back to the caht page.'''
    add_messages(username, message)
    return redirect(username)
~~~~
The user function will then display the user name and any messages stored.
~~~~python
@app.route('/<username>')
def user(username):
    '''Display chat messages.'''
    return "Welcome, {0}. <br>{1}".format(username, messages)
~~~~

A refinement on this:
Using a get_all_messages function:
~~~~python
def get_all_messages():
    '''Get all of the messages and separate them by a `br`.'''
    return "<br>".join(messages)
~~~~

This function will be called in the return statement of the user function.
~~~~python
@app.route('/<username>')
def user(username):
    '''Display chat messages.'''
    return "Welcome, {0}. <br>{1}".format(username, get_all_messages())
~~~~
This will tidy up the output by displaying each message on a new line.

Reformat output by using a h1 tag:
~~~~python
return "<h1>Welcome, {0}</h1>{1}".format(username, get_all_messages())
~~~~