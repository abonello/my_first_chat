# Flask Chat App

This project is currently hosted [here](https://my-first-chatroom.herokuapp.com/).

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

* * *
## Adding Time Stamp
In order to be able to use dates, times and using timestamps we need to import
datetime

~~~~python
from datetime import datetime
~~~~

The timestamp will be included in the list in the add_messages function. A new 
variable called **now** will hold the current time which will then be appended
to the messages list with the rest of the information:
~~~~python
def add_messages(username, message):
    '''Add messages to the `messages` list.'''
    now = datetime.now().strftime("%H:%M:%S")
    messages.append("({}) {}: {}".format(now, username, message))
~~~~

* * *
## Upgrading storage to a List of Dictionaries
~~~~python
def add_messages(username, message):
    '''Add messages to the `messages` list.'''
    now = datetime.now().strftime("%H:%M:%S")
    message_dict = {"timestamp": now, "from": username, "message": message}
    messages.append(message_dict)
~~~~

For now we need to modify the output of **get_all_messages** function:
~~~~python
def get_all_messages():
    '''Get all of the messages and separate them by a `br`.'''
    return messages
~~~~

## Start using Templates

We need to import render_template
~~~~python
from flask import Flask, redirect, render_template
~~~~

Create templates folder and index.html inside it.  
The return of the index routing function is changed to point to this new html 
template.

~~~~python
@app.route('/')
def index():
    """Main Page with instructions."""
    return render_template("index.html")
~~~~

index.html is a simple html file. The body will contain the following paragraph
for now:

~~~~html
<p>To send a message use /USERNAME/MESSAGE</p>
~~~~

## Storing Users in a text file

We need to request a form in the index.html if the POST method is used.

The first thing we need is to import request.

~~~~python
from flask import Flask, redirect, render_template, request
~~~~

Then in the index function of the root route we need to check if the POST method
was used. For now we will print the result in the CLI.
~~~~python
@app.route('/', methods=['GET', 'POST'])
def index():
    """Main Page with instructions."""
    if request.method == "POST":
        print(request.form)
    return render_template("index.html")
~~~~

For now, the form in the index.html looks like the following:
~~~~html
<form method="POST">
    <label for="username">Username:</label>
    <input type="text" id="username" name="username"/>
    <button>Go to chat!</button>
</form>
~~~~

We need to store the user in a text file.  
Create a **users.txt** file in a folder called **data**. The reason we need this
file is that the web is stateless -- ie. it does not persist any data itself. We
need to store it if we want the data to persist. Later on, using frameworks like
Django, it will handle all users stuff for us which is a benefit of using a kind
of batteries included framework.

**BUG:** At the moment, all users are stored attached to each other with no 
spaces or other separation. The next step is to store each user on a separate 
line. This is corrected by adding a new line at the end of the appended string.
~~~~python
@app.route('/', methods=['GET', 'POST'])
def index():
    """Main Page with instructions."""
    if request.method == "POST":
        with open("data/users.txt", "a") as user_list:
            user_list.write(request.form["username"] + "\n")
        return redirect(request.form["username"])
    return render_template("index.html")
~~~~

I do not understand why the tutor is using writelines instead of write. I do not 
see the advantage of former or the disadvantage of the latter.

* * *
## Refactoring To Use chat.html Instead Of A Single String

We will create a new html file to display our chat messages. This will work by 
passing it the necessary chat messages.

At the moment if we have more than one user using the app and one of them writes
a message, that user sees the message but the other user will not see it unless
his page is refreshed.

One of the ways of getting around this is by doing something called **long 
polling** in JavaScript.

For now we have prepared the chat.html

~~~~html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Home Page</title>
</head>
<body>
    <h1>Welcome, {{ username }}</h1>
    {{ chat_messages }}
</body>
</html>
~~~~

And adjusted the user function of the username route
~~~~python
@app.route('/<username>')
def user(username):
    '''Display chat messages.'''
    messages = get_all_messages()
    return render_template("chat.html", 
                            username = username, chat_messages = messages)
~~~~


##Simple Long Polling With JavaScript

Long polling refreshes the page after a specified period of time. It is achieved 
by using JavaScript's setTimeout function.  
Code in chat.html
~~~~javascript
<!-- long polling -->
<script>
    // Reload the page every 5 seconds
    setTimeout(function() {
        location.reload();
    }, 5000);
</script>
~~~~
This will auto refresh teh page every 5 seconds.

Next we need to reformat the display of the messages so that it displays each 
message on a fresh line.
~~~~html
{% for message in chat_messages%}
<span>({{ message["timestamp"] }}) {{ message["from"].title() }} - {{message["message"]}}</span><br>
{% endfor %}
~~~~

## Save Chats To A .txt File

Next step is to save our chat messages in a .txt file. This will make the chat 
persistant by writing the chat messages to an external file.

Modified  add messages function
~~~~python
def add_messages(username, message):
    '''Add messages to the `messages` text file (previously it was a list).'''
    now = datetime.now().strftime("%H:%M:%S")
    message_dict = {"timestamp": now, "from": username, "message": message}
    with open("data/messages.txt", 'a') as chat_list:
        chat_list.writelines("({0}) {1} - {2}\n".format(
            message_dict['timestamp'], 
            message_dict['from'].title(), 
            message_dict['message']))
~~~~

And modified get_all_messages function
~~~~python
def get_all_messages():
    '''Get all of the messages and separate them by a `br`.'''
    messages = []
    with open("data/messages.txt", "r") as chat_messages:
        messages = chat_messages.readlines()
    return messages
~~~~

I also had to modify the chat.html file
~~~~html
    <h1>Welcome, {{ username }}</h1>
    {% for message in chat_messages%}
    <span>{{ message }}</span><br>
    {% endfor %}
~~~~

Now we have a user list stored in users.txt and the messages (together) with
the username and timestamp stored in messages.txt

## Refactor code to simplify it

1. We are now using a txt file to store messages not a list:
    ~~~~python
    '''Add messages to the `messages` text file (previously it was a list).'''
    ~~~~
2. We can actually remove the dependency on storing this information in the 
    dictionary now because we can just insert the values directly into the 
    string in the add_messages function:
    ~~~~python
    def add_messages(username, message):
        '''Add messages to the `messages` text file (previously it was a list).'''
        # Write the chat message to the messages.txt file
        with open("data/messages.txt", 'a') as chat_list:
            chat_list.writelines("({0}) {1} - {2}\n".format(
                datetime.now().strftime("%H:%M:%S"), 
                username.title(), 
                message))
    ~~~~

3. Currently we are writing to a file in two separate places. We need to 
    centralize this in order to minimize the room for exceptions. Create a 
    function called **write_to_file**. This takes two parameters; a filename 
    and the data that we want to write to that file.
    ~~~~python
    def write_to_file(filename, data):
    '''Handle the process of writing data to a file.'''
    with open(filename, 'a') as file:
        file.writelines(data)
    ~~~~
    The add_messages function has now been refactored as it writes to a file:
    ~~~~python
    def add_messages(username, message):
        '''Add messages to the `messages` text file (previously it was a list).'''
        # Write the chat message to the messages.txt file
        write_to_file("data/messages.txt", "({0}) {1} - {2}\n".format(
                datetime.now().strftime("%H:%M:%S"), 
                username.title(), 
                message))
    ~~~~
    The index function is also writing to a file. We can simplify this:
    ~~~~python
    @app.route('/', methods=['GET', 'POST'])
    def index():
        """Main Page with instructions."""
        # Handle POST request
        if request.method == "POST":
            write_to_file("data/users.txt", request.form["username"] + "\n")
            return redirect(request.form["username"])
        return render_template("index.html")
    ~~~~
 
 
* * *
## Deploy on Heroku

login to heroku
~~~~
heroku login
~~~~
Enter email and password.  
Then create a new app. I am calling it my-first-chatroom.
~~~~
heroku apps:create my-first-chatroom
~~~~
Heroku adds a git remote to our local git. To view this use:
~~~~
git remote -v
~~~~
Create a Procfile
~~~~
echo web: python run.py > Procfile
~~~~
Now push to Heroku
~~~~
git push -u heroku master
~~~~

We need to set scales. This sets one dynamo worker running.
~~~~
heroku ps:scale web=1
~~~~

At this point there is a Heroku error. Logging in to the dashboard
I can see what the error is. The process can also be done in command line but 
it is easier in the dashboard.
We need to create some config VARS.
In heroku, once you get into your app, go to Settings. Then select 
**Reveal Config Vars**. Here input key, value pairs for host IP and PORT:
|IP| 0.0.0.0|
|:-:|-|
|**PORT**|**5000** |
Follow this by **More > Restart all dynos**
Open the App once more.

Notice that the old messages are still available.