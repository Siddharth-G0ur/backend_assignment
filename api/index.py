from flask import Flask,request
import requests
from datetime import datetime


def search_author(data,name):
    return {"comments":[i for i in data["comments"] if i["author"].split()[0]==name]}

def at_from(data,date):
    return {"comments":[i for i in data["comments"] if datetime.strptime(i["at"], "%a, %d %b %Y %H:%M:%S GMT")>=datetime.strptime(date, "%d-%m-%Y")]}

def at_to(data,date):
    return {"comments":[i for i in data["comments"] if datetime.strptime(i["at"], "%a, %d %b %Y %H:%M:%S GMT")<=datetime.strptime(date, "%d-%m-%Y")]}

def like_from(data,likes_lower):
    return {"comments":[i for i in data["comments"] if i["like"]>=int(likes_lower)]}

def like_to(data,likes_upper):
    return {"comments":[i for i in data["comments"] if i["like"]<=int(likes_upper)]}

def reply_from(data,reply_lower):
    return {"comments":[i for i in data["comments"] if i["reply"]>=int(reply_lower)]}

def reply_to(data,reply_upper):
    return {"comments":[i for i in data["comments"] if i["reply"]<=int(reply_upper)]}

def search_text(data,srh_txt):
    return {"comments":[i for i in data["comments"] if srh_txt in i["text"]]}


# create the app
app=Flask(__name__)
app.debug = True


#testing route for server
@app.route("/")
def home():
    return "Home route"
    
# functions mapped
function_map = {
    "search_author": search_author,
    "at_from": at_from,
    "at_to": at_to,
    "like_from": like_from,
    "like_to": like_to,
    "reply_from": reply_from,
    "reply_to": reply_to,
    "search_text": search_text,
    "seach_text":search_text
}
@app.route('/search',methods=['GET'])
def api_fun():
    api=requests.get("https://dev.ylytic.com/ylytic/test")
    api_data=api.json()
    for i in request.args:
        api_data=function_map[i](api_data,request.args[i])
    return api_data


if __name__ == "__main__":
    app.run(port=5000)
