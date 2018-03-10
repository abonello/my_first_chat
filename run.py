import os
from datetime import datetime
from flask import Flask, redirect, render_template, request

app = Flask(__name__)
# messages = []

def write_to_file(filename, data):
    '''Handle the process of writing data to a file.'''
    with open(filename, 'a') as file:
        file.writelines(data)

def add_messages(username, message):
    '''Add messages to the `messages` text file (previously it was a list).'''
    # now = datetime.now().strftime("%H:%M:%S")
    # message_dict = {"timestamp": now, "from": username, "message": message}
    # messages.append("({}) {}: {}".format(now, username, message))
    # messages.append(message_dict)
    # Write the chat message to the messages.txt file
    # with open("data/messages.txt", 'a') as chat_list:
    #     chat_list.writelines("({0}) {1} - {2}\n".format(
    #         message_dict['timestamp'], 
    #         message_dict['from'].title(), 
    #         message_dict['message']))
    # with open("data/messages.txt", 'a') as chat_list:
    #     chat_list.writelines("({0}) {1} - {2}\n".format(
    #         datetime.now().strftime("%H:%M:%S"), 
    #         username.title(), 
    #         message))
    write_to_file("data/messages.txt", "({0}) {1} - {2}\n".format(
            datetime.now().strftime("%H:%M:%S"), 
            username.title(), 
            message))

def get_all_messages():
    '''Get all of the messages and separate them by a `br`.'''
    messages = []
    with open("data/messages.txt", "r") as chat_messages:
        messages = chat_messages.readlines()
    # return "<br>".join(messages)
    return messages

@app.route('/', methods=['GET', 'POST'])
def index():
    """Main Page with instructions."""
    # Handle POST request
    if request.method == "POST":
        # print(request.form)
        # with open("data/users.txt", "a") as user_list:
        #     user_list.write(request.form["username"] + "\n")
        write_to_file("data/users.txt", request.form["username"] + "\n")
        return redirect(request.form["username"])
    # return "<h1>Hello World</h1>"
    # return "To send a message use /USERNAME/MESSAGE"
    return render_template("index.html")

# Like a personalised home page for each user. Each user will have their URL.   
@app.route('/<username>')
def user(username):
    '''Display chat messages.'''
    messages = get_all_messages()
    # return "Welcome, {0}. <br>{1}".format(username, messages)
    # return "<h1>Welcome, {0}</h1>{1}".format(username, get_all_messages())
    return render_template("chat.html", 
                            username = username, chat_messages = messages)
    
@app.route('/<username>/<message>')
def send_message(username, message):
    '''Create a new message and redirect back to the caht page.'''
    add_messages(username, message)
    # return "{0} says: {1}".format(username, message)
    return redirect(username)
    
app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)