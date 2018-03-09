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