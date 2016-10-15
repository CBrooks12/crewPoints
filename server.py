import flask
from flask import request
from flask import url_for
from flask import jsonify # For AJAX transactions

import json
import logging

import random
import math
# Mongo database
#import pymongo
#from pymongo import MongoClient
#from bson.objectid import ObjectId

# Date handling
import arrow # Replacement for datetime, based on moment.js
#import datetime # But we still need time
#from dateutil import tz  # For interpreting local times

###
# Globals
###
app = flask.Flask(__name__)
import CONFIG
INITIAL_POINTS = 20

import uuid
app.secret_key = str(uuid.uuid4())
app.debug = CONFIG.DEBUG
app.logger.setLevel(logging.DEBUG)


#try:
#    dbclient = MongoClient(CONFIG.MONGO_URL)
#    db = dbclient.service
#    collectionAccounts = db.studentAccounts  #for the student accounts
#except:
#    print("Failure opening database.  Is Mongo running? Correct password?")
    #sys.exit(1)

#############
####Pages####
#############


### Home Page ###

@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('index.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('page_not_found.html'), 404


###for login page###
@app.route("/_submitLoginRequest")
def loginGate():
    duckId = request.args.get('duckId',0,type=str)
    pwd = request.args.get('pwd',0,type=str)
#    account = collectionAccounts.find_one({'duckId':duckId,'password':pwd})
    #app.logger.debug(account)
#    if account != None:
#        flask.session['login'] = str(account.get('_id'))
#        flask.session['name'] = account.get('duckId')
    d = {'result':'success'}
#    else:
#        d = {'result':'failed'}
    d = json.dumps(d)
    return jsonify(result = d)


### user Page ###

@app.route("/user")
def user():
    app.logger.debug("user page entry")
#    app.logger.debug(flask.session.get('login'))
#    if flask.session.get('login') == None:
#        return flask.render_template('login.html') 
#Possibly use this, but lets try to avoid the state if possible?
#    crewPoints = collectionAccounts.find_one({"_id":ObjectId(flask.session.get('login'))}).get("crewPoints")
#    flask.session['CrewPoints'] = crewPoints
    
    return flask.render_template('user.html')


##additional pages###
@app.route("/userCreate")
def userCreate():
#    app.logger.debug("user create page entry")
    return flask.render_template('userCreate.html')

@app.route("/medals")
def medalsPage():
    app.logger.debug("user create page entry")
    return flask.render_template('medals.html')

@app.route("/rewards")
def rewardsPage():
    return flask.render_template('rewards.html')
    
@app.route("/the_crew")
def crewPage():
    return flask.render_template('the_crew.html')

@app.route('/login')
def login():
#    if flask.session.get('login') != None:
        return flask.redirect(url_for('user'))
#    else:
#        return flask.render_template('login.html')

@app.route('/createUser')
def createUser():
        return flask.render_template('createUser.html')




##remove the current state###
#def removeState():
#    flask.session['name'] = None
#    flask.session['login'] = None
#    flask.session['CrewPoints'] = None





################
###functions###
################

@app.route("/_portal")
def portalSelector():
    objId = request.args.get('portal', 0, type=str)
    app.logger.debug(objId)
    if objId == "user":
        return flask.redirect(url_for('user'))
        
@app.route("/_userSettings")
def userSettings():
    setting = request.args.get('setting',0,type=str)
    duckId = request.args.get('duckId',0,type=str)
    pwd = request.args.get('pwd',0,type=str)
    if setting  == "addUser":
#        if collectionAccounts.find_one({'duckId':duckId}) == None:
#            crewPoints = INITIAL_POINTS
#            record = {"duckId":duckId, "password":pwd, "date":arrow.utcnow().naive, "crewPoints": crewPoints}
#            collectionAccounts.insert(record)
            d = "added"
#            print d
#        else:
#            d = "account exists"
    elif setting == "removeUser":
#        collectionAccounts.remove({'_id':ObjectId(flask.session.get('login'))})
#        removeState()
        return flask.redirect(url_for('login'))
    elif setting == "logout":
#        removeState()
        return flask.redirect(url_for('login'))
    else:
        d = "wat"
#    print d
    return jsonify(result = d)        
 
        
        ##test##
@app.route("/_getWord")
def preData():
    aReturn = request.args.get('aThing',0,type=str)
    aVal = json.loads(aReturn)
    hashtag = aVal.get("aWord")
    print(hashtag)
    d = {"result":"true", "val":hashtag}
    return jsonify(d)

if __name__ == "__main__":
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug = CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=CONFIG.PORT,threaded=True)
