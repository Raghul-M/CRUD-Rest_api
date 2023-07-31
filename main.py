from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

# Use Postman for Api working with your local host http://127.0.0.1:5000/user
"""
@app.route('/',methods=['GET'])
def home():
    return jsonify(
        {
            'name':'Raghul',
            'msg': 'Welcome to the Arena'

        })

"""
basedir=os.path.abspath(os.path.dirname(__file__)) #to find the project path
print(basedir)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'db.sqllite') #to create db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


db = SQLAlchemy(app) #object for sqlite
app.app_context().push() # To solve the runtime error
mar = Marshmallow(app)  #object for marshmallow , using it for data-serialization schema

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    contact=db.Column(db.String(100),unique=True)

    def __init__(self,name,contact):
        self.name=name
        self.contact=contact

class UserSchema(mar.Schema):
    class Meta: #overwritting the inbuit meta class to view the details outside
        fields = ('id','name','contact')
user_schema = UserSchema() #object for userschema for single operation
users_schema=UserSchema(many=True) #object for userschema for multiple operation

#Add New User
@app.route('/user',methods=['POST']) #http://127.0.0.1:5000/user
def add_user():
    name=request.json['name']
    contact = request.json['contact']
    new_user=User(name, contact)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)

#Show All User
@app.route('/users',methods=['GET']) #http://127.0.0.1:5000/users
def getAllUser():
    all_users=User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

#Show User By ID
@app.route('/user/<id>',methods=['GET']) #http://127.0.0.1:5000/users/2
def getUserByid(id):
    user=User.query.get(id)
    return user_schema.jsonify(user)

#Update User By Id
@app.route('/user/<id>',methods=['PUT']) #http://127.0.0.1:5000/users/2
def UpdateUser(id):
    user=User.query.get(id)
    name = request.json['name']
    contact = request.json['contact']
    user.name=name
    user.contact=contact
    db.session.commit()
    return user_schema.jsonify(user)

#Delete UserBy ID #http://127.0.0.1:5000/users/2
@app.route('/user/<id>',methods=['DELETE'])
def DeleteUserByID(id):
    user=User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)

if __name__=='__main__':
    app.run(debug=True,port=5000)