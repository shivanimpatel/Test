from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Float
import os
from flask_marshmallow import Marshmallow

# define the flask app
mfaqapi = Flask(__name__)
# config settings for SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
# telling flask (sqlalchemy) where the database file will be stored/accessible to/from
mfaqapi.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'mfaq.db')

# configure marshmallow
ma = Marshmallow(mfaqapi)


# initialise our database as a python object
db = SQLAlchemy(mfaqapi)
@mfaqapi.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database Successfully Created!')


@mfaqapi.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database Dropped Successfully')


# home page route (endpoint)
@mfaqapi.route('/')
def home():
    return jsonify(data='Hello World #UTFB!')


# users / consumers of my api must provide a key=value pair
# in the format of:
# p=lastname i.e p=Booth
# cohort = enum('DP', 'DE', 'DM')
@mfaqapi.route('/gettechnicalquestion', methods=['POST','GET'])
def getquestion():
    Question = request.args.get('p')
    questiondata = Question.query.filter_by(Question=Question)
    # retrieve records from a database
    result = question_schema.dump(questiondata)
    return jsonify(result)


@mfaqapi.route('/addquestion', methods=['POST','GET'])
def addquestion():
    qn = request.form['Question']
    ar = request.form['Author']
   # insert the data into the sqlite database
    new_question = Question(Question=qn, Author=ar)
    db.session.add(new_question)
    db.session.commit()

    # result = successfailure flag
    # if insert successful then return result
    # else return result

    return jsonify(data='Question {} added to the database'.format(qn)), 201


@mfaqapi.route('/rempeople', methods=['GET', 'POST'])
def rempeople():
    # name = request.args.get('p')
    name = request.form['lastname']
    remperson = Question.query.filter_by(lname=name).first()
    if remperson:
        db.session.delete(remperson)
        db.session.commit()
        return jsonify(data='Person with last name {} removed from the database'.format(name))
    else:
        return jsonify(data='Person with last name {} did not exist in the database'.format(name))


# in SQLAlchemy a Model is a table - we are creating the blueprint for our own table called People
class Question(db.Model):
    __tablename__='question' # make a table called people
    QuestionID = Column(Integer, primary_key=True)
    Question = Column(String)
    Author = Column(String)

class QuestionSchema(ma.Schema):
    class Meta:
        fields=('QuestionID', 'Question', 'Author')


question_schema = QuestionSchema()


if __name__ == '__main__':
    mfaqapi.run(debug=True)