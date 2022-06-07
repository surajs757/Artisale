import requests
import sys
import json
import base64
from flask_cors import CORS
from flask import Flask, render_template, request, redirect, Response, abort, jsonify, make_response, Response
from json import dumps

app = Flask(__name__)
CORS(app)

@app.route('/api/v1/users', methods=['POST'])
def addUser():
    if(request.method != 'POST'):
        return "unsupported media type", 415

    try:
        data = request.get_json(force=True)
        print(data)
        firstName = data["firstName"]
        lastName = data["lastName"]
        email = data["email"]
        username = data["username"]
        password = data["password"]
        uid = data["uid"]
    except:
        return "bad request", 400
    f1 = open("static/users.txt", "r")
    existingUserIds = [x.split("\t")[0] for x in f1.readlines()]
    if(uid in existingUserIds):
        return "user already exists", 400
    f1.close()

    st = str(uid) + "\t" + username + "\t" + firstName + "\t" + lastName + "\t" + email + "\t" + password + "\n"
    f = open("static/users.txt", "a")
    f.write(st)
    f.close()
    return "added user successfully",201


@app.route('/api/v1/users',methods=['GET'])
def list_users():
    if(request.method != "GET"):
        abort(405)    
    f=open("static/users.txt","r")
    creds=f.readlines()
    names=[x.split('\t')[2] for x in creds]
    if (len(names)==0):
        return "No users",204

    return jsonify(names)

@app.route('/api/v1/users/<uid>',methods=['DELETE'])
def rem_user(uid):
    if(request.method != "DELETE"):
        abort(405)    
    f=open("static/users.txt","r")        
    creds=f.readlines()
    #return creds[0]
    ids=[x.split('\t')[0] for x in creds]
    #return str(len(names))
    #return userid
    if uid not in ids:
        abort(400)
    else:
        reqcred=""
        for cred in creds:
            if(uid==cred.split()[0]):
                reqcred=cred
                break
        creds.remove(reqcred)
        st=''.join(creds)
        #return st
        f.close()
        f=open("static/users.txt","w")
        f.write(st)
        
    st="user "+uid+" removed successfullly"
    return str(st),200


@app.route('/api/v1/users/cart', methods=['POST'])
def addcart():
    if(request.method != 'POST'):
        return "unsupported media type", 415

    try:
        data = request.get_json(force=True)
        uid = data["uid"]
        arname = data["arname"]
        arid = data["arid"]
        cost = data["cost"]
    except:
        return "bad request", 400
    f1 = open("static/artifact.txt", "r")
    arIds = [x.split("\t")[0] for x in f1.readlines()]
    if(arid in arIds):
        return "articraft id already exists", 400
    f1.close()

    st = str(arid) + "\t" + uid + "\t" + arname + "\t" + arid + "\t" + cost + "\n"
    f = open("static/artifact.txt", "a")
    f.write(st)
    f.close()
    return "articraft added successfully",201

@app.route('/api/v1/users/<id>/cart', methods=['GET'])
def getCart(id):
    if(request.method != 'GET'):
        return "METHOD NOT ALLOWED", 415
    try:
        userCart = []
        f1 = open("static/artifact.txt")
        for line in f1:
            data = line.split('\t')
            if (id == data[1]):
                lineJson = {}
                lineJson["UserID"] = data[1]
                lineJson["ArtifactName"] = data[2]
                lineJson["ArtifactId"] = data[3]
                lineJson["Cost"] = data[4][:-1] if data[4][-1:] == '\n' else data[4]
                userCart.append(lineJson)
        print(userCart)

    except:
        return "bad request", 400
    f1.close()
    return json.dumps(userCart)


if(__name__ == "__main__"):
    app.debug = True
    app.run(port = 5000)
