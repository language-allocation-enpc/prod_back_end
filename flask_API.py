from flask import Flask
from flask import jsonify
from flask import request, session, url_for, redirect, make_response
from flask_pymongo import PyMongo
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from bson.objectid import ObjectId
import bson.json_util
import json
import pymongo
import random
import datetime
import string
from ast import literal_eval
from flask_cors import CORS, cross_origin
import data_structs
from solver import *
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from flask_mail import Mail, Message
site_url = 'http://localhost:3000/'


app = Flask(__name__)
cors = CORS(app, resources={r"/*":{"origins": site_url}})


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.testing=False
app.config['MONGO_DBNAME'] = 'language_allocation_database'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/language_allocation_database'
app.config['SECRET_KEY'] = '6Cb4CTv46t39GYncwkmTEbcjs9415fskfnR'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JWT_SECRET_KEY'] = 'WkDHlzbF3d6kWOGQcZvKudFjsJNeSOFY'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = '3071go.nathan@gmail.com'
app.config['MAIL_PASSWORD'] = 'youhou95'
mongo = PyMongo(app)
blacklist = set()
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
mail = Mail(app)

def generate_token():
    return ''.join(random.choices(string.ascii_uppercase +string.ascii_lowercase+ string.digits, k=35))

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


@app.route('/admin/login', methods=['POST'])
@cross_origin(origin=site_url, headers=['Content-Type','Authorization'], supports_credentials=True)
def login():
    users = mongo.db.users
    email = request.get_json(force=True)['email']
    password = request.get_json(force=True)['password']
    result = ""

    response = users.find_one({'type': 'admin', 'email' : email})

    if response:
        if bcrypt.check_password_hash(response['password'], password):
            access_token = create_access_token(identity = {
			    'name': response['first_name'],
				'email': response['email']}
				)

            result = jsonify({"token":access_token})
        else:
            result = jsonify({"error":"Invalid username and password"})
    else:
        result = jsonify({"error":"No results found"})
    return result

@app.route('/admin/logout', methods=["DELETE"])
@cross_origin(origin=site_url,headers=['Content-Type','Authorization'], supports_credentials=True)
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200


@app.route('/admin/check-auth', methods=['GET'])
@cross_origin(origin=site_url,headers=['Content-Type','Authorization'], supports_credentials=True)
@jwt_required
def check_auth():
    return jsonify({"state":"true"})

@app.route('/admin/register', methods=['POST'])
@cross_origin(origin=site_url, headers=['Content-Type','Authorization'], supports_credentials=True)
def register():
    users = mongo.db.users
    first_name = request.get_json(force=True)['first_name']
    last_name = request.get_json(force=True)['last_name']
    email = request.get_json(force=True)['email']
    password = bcrypt.generate_password_hash(request.get_json(force=True)['password']).decode('utf-8')

    user_id = users.insert({
	'first_name' : first_name,
	'last_name' : last_name,
	'email' : email,
	'password' : password,
    'type' : "admin"
	})
    new_user = users.find_one({'_id' : user_id})

    result = {'email' : new_user['email'] + ' registered'}

    return jsonify({'result' : result})



@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


def get_max_collection_id(collection):
    max_column = collection.find_one(sort=[("id", -1)])
    if max_column==None:
        return 0
    return int(max_column["id"])



@app.route('/courses/', methods=['GET'])
@cross_origin(origin=site_url,headers=['Content-Type','Authorization'], supports_credentials=True)
def get_all_courses():
    courses = mongo.db.courses
    all_courses = courses.find()
    if all_courses:
        Output = []
        for course in all_courses:
            output={}
            output["id"] = course["id"]
            output["name"] = course["name"]
            output["language"] = course["language"]
            output["creneaux"] = course["creneaux"]
            output["min_students"] = course["min_students"]
            output["max_students"] = course["max_students"]
            Output.append(output)
        html_code = 200
    else:
        output = "No courses"
        html_code = 400
    return jsonify({'result': Output}), html_code



@app.route('/courses/<course_id>', methods=['GET'])
@cross_origin(origin=site_url,headers=['Content-Type','Authorization'], supports_credentials=True)
def get_course_by_id(course_id):
    courses = mongo.db.courses
    course = courses.find_one({"id": int(course_id)})
    if course:
        output={}
        output["id"] = course["id"]
        output["name"] = course["name"]
        output["language"] = course["language"]
        output["creneaux"] = course["creneaux"]
        output["min_students"] = course["min_students"]
        output["max_students"] = course["max_students"]
        html_code = 200
    else:
        output = "No matching course for id " + str(course_id)
        html_code = 400
    return jsonify({'result': output}), html_code


@app.route('/courses/by-language/<language>', methods=['GET'])
@cross_origin(origin=site_url,headers=['Content-Type','Authorization'])
def get_course_by_language(language):
    courses = mongo.db.courses
    courses_of_language = courses.find({"language": language})
    if courses_of_language:
        Output = []
        for course in courses_of_language:
            output={}
            output["id"] = course["id"]
            output["name"] = course["name"]
            output["language"] = course["language"]
            output["creneaux"] = course["creneaux"]
            output["min_students"] = course["min_students"]
            output["max_students"] = course["max_students"]
            Output.append(output)
        html_code = 200
    else:
        Output = "No matching course for language " + str(language)
        html_code = 400
    return jsonify({'result': Output}), html_code

@app.route('/courses/not-english/', methods=['GET'])
@cross_origin(origin=site_url,headers=['Content-Type','Authorization'], supports_credentials=True)
def get_course_not_english():
    courses = mongo.db.courses
    Output = []
    for course in courses_of_language:
        if course["language"] != "Anglais":
            output={}
            output["id"] = course["id"]
            output["name"] = course["name"]
            output["language"] = course["language"]
            output["creneaux"] = course["creneaux"]
            output["min_students"] = course["min_students"]
            output["max_students"] = course["max_students"]
            Output.append(output)
        html_code = 200
    return jsonify({'result': Output}), html_code


@app.route('/courses/<course_id>', methods=['POST'])
@cross_origin(origin=site_url,headers=['Content-Type','Authorization'], supports_credentials=True)
def update_course(course_id):
    courses = mongo.db.courses
    new_name = request.get_json(force=True)['name']
    new_language = request.get_json(force=True)['language']
    new_creneaux = request.get_json(force=True)['creneaux']
    new_min_students = request.get_json(force=True)['min_students']
    new_max_students = request.get_json(force=True)['max_students']
    course_update = courses.update({"id":int(course_id)}, {"id":int(course_id),
                                                           "name":new_name,
                                                           "language":new_language,
                                                           "creneaux":new_creneaux,
                                                           "min_students":new_min_students,
                                                           "max_students":new_max_students})
    if course_update:
        output = "Course with id "+course_id+" updated successfully"
        html_code = 200
    else:
        output = "No matching course for id " + str(course_id)
        html_code = 400
    return jsonify({'result': output}), html_code


@app.route('/courses/', methods=['PUT'])
@cross_origin(origin=site_url,headers=['Content-Type','Authorization'], supports_credentials=True)
def add_course():
    courses = mongo.db.courses
    id = get_max_collection_id(courses)+1
    new_name = request.get_json(force=True)['name']
    new_language = request.get_json(force=True)['language']
    new_creneaux = request.get_json(force=True)['creneaux']
    new_min_students = request.get_json(force=True)['min_students']
    new_max_students = request.get_json(force=True)['max_students']
    course_inserted = courses.insert({"id":int(id),
                                                           "name":new_name,
                                                           "language":new_language,
                                                           "creneaux":new_creneaux,
                                                           "min_students":new_min_students,
                                                           "max_students":new_max_students})
    if course_inserted:
        output = {"id":id}
        html_code = 200
    else:
        output = "Could not add course"
        html_code = 400
    return jsonify({'result': output}), html_code


@app.route('/courses/<course_id>', methods=['DELETE'])
@cross_origin(origin=site_url,headers=['Content-Type','Authorization'], supports_credentials=True)
def remove_course(course_id):
    courses = mongo.db.courses
    course_removed = courses.remove({"id":int(course_id)})
    if course_removed:
        output = "Course successfully removed"
        html_code = 200
    else:
        output = "Could not remove course"
        html_code = 400
    return jsonify({'result': output}), html_code



@app.route('/creneaux/', methods=['GET'])
@cross_origin(origin=site_url,headers=['Content-Type','Authorization'])
def get_all_creneaux():
    creneaux = mongo.db.creneaux
    all_creneaux = creneaux.find()
    Output = []
    for creneau in all_creneaux:
        output={}
        output["id"] = creneau["id"]
        output["day"] = creneau["day"]
        output["begin"] = creneau["begin"]
        output["end"] = creneau["end"]
        output["type"] = creneau["type"]
        Output.append(output)
        html_code = 200
    return jsonify({'result': Output}), html_code


@app.route('/creneaux/<creneaux_id>', methods=['GET'])
@cross_origin(origin=site_url,headers=['Content-Type','Authorization'])
def get_creneau_by_id(creneau_id):
    creneaux = mongo.db.creneaux
    creneau = creneaux.find_one({"id": int(creneau_id)})
    if creneau:
        output={}
        output["id"] = creneau["id"]
        output["day"] = creneau["day"]
        output["begin"] = creneau["begin"]
        output["end"] = creneau["end"]
        output["type"] = creneau["type"]
        html_code = 200
    else:
        output = "No matching creneau for id " + str(course_id)
        html_code = 400
    return jsonify({'result': output}), html_code

@app.route('/creneaux/by-promotion/<promo>', methods=['GET'])
@cross_origin(origin=site_url,headers=['Content-Type','Authorization'])
def get_creneau_by_promo(promo):
    creneaux = mongo.db.creneaux.find({"type" : {'$regex': promo}})
    Output = []
    for creneau in creneaux:
        if promo in creneau["type"]:
            output={}
            output["id"] = creneau["id"]
            output["day"] = creneau["day"]
            output["begin"] = creneau["begin"]
            output["end"] = creneau["end"]
            output["type"] = creneau["type"]
            Output.append(output)
        html_code = 200
    return jsonify({'result': Output}), html_code


@app.route('/creneaux/<creneau_id>', methods=['POST'])
@cross_origin(origin=site_url,headers=['Content-Type','Authorization'])
def update_creneau(creneau_id):
    creneaux = mongo.db.creneaux
    new_day = request.get_json(force=True)['day']
    new_begin = request.get_json(force=True)['begin']
    new_end = request.get_json(force=True)['end']
    new_type = request.get_json(force=True)['type']
    creneau_updated = courses.update({"id":int(creneau_id)}, {"id":int(creneau_id),
                                                           "day":new_day,
                                                           "begin":new_begin,
                                                           "end":new_end,
                                                           "type":new_type})
    if creneau_updated:
        output = "Creneau with id "+creneau_id+" updated successfully"
        html_code = 200
    else:
        output = "No matching creneau for id " + str(creneau_id)
        html_code = 400
    return jsonify({'result': output}), html_code


@app.route('/creneaux/', methods=['PUT'])
@cross_origin(origin=site_url,headers=['Content-Type','Authorization'])
def add_creneau():
    creneaux = mongo.db.creneaux
    id = get_max_course_id()+1
    new_day = request.get_json(force=True)['day']
    new_begin = request.get_json(force=True)['begin']
    new_end = request.get_json(force=True)['end']
    new_type = request.get_json(force=True)['type']
    creneau_inserted = courses.insert({"id":int(creneau_id),
                                                           "day":new_day,
                                                           "begin":new_begin,
                                                           "end":new_end,
                                                           "type":new_type})
    if course_inserted:
        output = {"id":id}
        html_code = 200
    else:
        output = "Could not add course"
        html_code = 400
    return jsonify({'result': output}), html_code


@app.route('/creneaux/<creneau_id>', methods=['DELETE'])
@cross_origin(origin=site_url,headers=['Content-Type','Authorization'])
def remove_creneau(creneau_id):
    creneaux = mongo.db.creneaux
    creneau_removed = creneaux.remove({"id":int(creneau_id)})
    if creneau_removed:
        output = "Creneau successfully removed"
        html_code = 200
    else:
        output = "Could not remove creneau"
        html_code = 400
    return jsonify({'result': output}), html_code

@app.route('/users/students/<student_id>', methods=['GET'])
@cross_origin(origin=site_url,headers=['Content-Type','Authorization'])
def get_student_by_id(student_id):
    users = mongo.db.users
    student = users.find_one({"type": "student", "id": int(student_id)})
    if student:
        output={}
        output["id"] = student["id"]
        output["name"] = student["name"]
        output["email"] = student["email"]
        output["vows"] = student["vows"]
        html_code = 200
    else:
        output = "No matching student for id " + str(student_id)
        html_code = 400
    return jsonify({'result': output}), html_code

@app.route('/users/students/', methods=['GET'])
@cross_origin(origin=site_url,headers=['Content-Type','Authorization'], supports_credentials=True)
@jwt_required
def get_all_students():
    users = mongo.db.users
    students = users.find({"type": "student"})
    if students:
        Output = []
        for student in students:
            if student['email']!='':
                output={}
                output["id"] = student["id"]
                output["first_name"] = student["name"].split(' ')[0]
                output["last_name"] = student["name"].split(' ')[1]
                output["email"] = student["email"]
                output["token"] = student["token"]
                Output.append(output)
        html_code = 200
    else:
        Output = "No student found"
        html_code = 400
    return jsonify({'result': Output}), html_code

@app.route('/users/students/get-courses', methods=['GET'])
@cross_origin(origin=site_url,headers=['Content-Type','Authorization'], supports_credentials=True)
@jwt_required
def get_courses_allocation():
    users = mongo.db.users
    students = users.find({"type": "student"})
    if students:
        Output = []
        for student in students:
            if student['email']!='':
                output={}
                output["name"]=student["name"]
                output["email"]=student["email"]
                output["courses"]=student["courses"]
                Output.append(output)
        html_code = 200
    else:
        Output = "No student found"
        html_code = 400
    return jsonify({'result': Output}), html_code

@app.route('/users/students/', methods=['POST'])
@cross_origin(origin=site_url,headers=['Content-Type','Authorization'], supports_credentials=True)
def send_all_students():
    users = mongo.db.users
    students = users.find({"type": "student"})
    if students:
        Output = []
        for student in students:
            if student['email']!='':
                msg = Message("Veuillez remplir le questionnaire langues au lien suivant",
                          sender="no-reply@questionnaire-DLC.com",
                          recipients=[student['email']])
                msg.body = "Voici votre lien personnalisé :  \n" + site_url+ "login?token="+student['token']
                mail.send(msg)
        html_code = 200
    else:
        Output = "No student found"
        html_code = 400
    return jsonify({'result': Output}), html_code

@app.route('/users/students/send-affect', methods=['POST'])
@cross_origin(origin=site_url,headers=['Content-Type','Authorization'], supports_credentials=True)
def send_affectations():
    users = mongo.db.users
    students = users.find({"type": "student"})
    courses = mongo.db.courses
    if students:
        Output = []
        for student in students:
            if student['email']!='':
                msg = Message("Résultats de l'affectation des cours de langues",
                          sender="no-reply@questionnaire-DLC.com",
                          recipients=[student['email']])
                msg.body = "Vous êtes inscrits aux cours suivants : \n"
                for course_id in student.courses:
                    current = courses.find({'id': course_id})
                    msg.body+=current.name+"\n"
                mail.send(msg)
        html_code = 200
    else:
        Output = "No student found"
        html_code = 400
    return jsonify({'result': Output}), html_code

@app.route('/admin/students/', methods=['PUT'])
@cross_origin(origin=site_url,headers=['Content-Type','Authorization'], supports_credentials=True)
@jwt_required
def update_all_students():
    users = mongo.db.users
    students = users.find({"type": "student"})
    data = request.get_json(force=True)
    print(data)
    for new_student in data:

        if 'token' not in new_student or new_student['token']=='':
            new_student['token'] = generate_token()
        empty=False
        for v in new_student.values():
            if v=='':
                print(new_student)
                empty=True
        if empty:
            continue

        student_updated = users.update_one({"email":new_student["email"]}, {"$set" : {
        "id":get_max_collection_id(users)+1,
                                                               "name":new_student['first_name']+" "+new_student['last_name'],
                                                               "email":new_student['email'],
                                                               "type":"student",
                                                               "vows":[],
                                                               "courses":[],
                                                               "token":new_student['token']}}, upsert=True)
        print(student_updated)

        if not student_updated:
            users.insert({"id":get_max_collection_id(users)+1,
                                                                   "name":new_student['first_name']+" "+new_student['last_name'],
                                                                   "email":new_student['email'],
                                                                   "type":"student",
                                                                   "vows":[],
                                                                   "courses":[],
                                                               "token":new_student['token']})
    for student in students:
        still_belongs = False
        for new_student in data:
            if student["email"] == new_student["email"]:
                still_belongs = True
        if not still_belongs:
            users.delete_one({"email":student["email"]})




    return jsonify({'result': "done"}), 200

@app.route('/users/students/', methods=['PUT'])
@cross_origin(origin=site_url,headers=['Content-Type','Authorization'], supports_credentials=True)
def add_student():
    users = mongo.db.users
    id = get_max_collection_id(users)+1
    new_name = request.get_json(force=True)['name']
    new_email = request.get_json(force=True)['email']
    new_token = ''.join(random.choices(string.ascii_uppercase +string.ascii_lowercase+ string.digits, k=35))
    student_inserted = users.insert({"id":int(id),
                                                           "name":new_name,
                                                           "email":new_email,
                                                           "token":new_token,
                                                           "vows":[],
                                                           "courses":[],
                                                           "type":"student"})
    if student_inserted:
        output = {"id":id}
        html_code = 200
    else:
        output = "Could not add student"
        html_code = 400
    return jsonify({'result': output}), html_code

@app.route('/users/students/<student_id>', methods=['POST'])
@cross_origin(origin=site_url,headers=['Content-Type','Authorization'])
def update_student(student_id):
    users = mongo.db.users
    new_name = request.get_json(force=True)['name']
    new_email = request.get_json(force=True)['email']
    new_vows = request.get_json(force=True)['vows']
    student_updated = users.update_one({"id":int(student_id)}, {"$set" : {"id":int(student_id),
                                                           "name":new_name,
                                                           "email":new_email,
                                                           "vows":new_vows}})
    if student_updated:
        output = {}
        output["id"] = student_id
        html_code = 200
    else:
        output = "Could not add student"
        html_code = 400
    return jsonify({'result': output}), html_code


@app.route('/users/students/vows/<student_token>', methods=['POST'])
@cross_origin(origin=site_url,headers=['Content-Type','Authorization'], supports_credentials=True)
def update_student_vows(student_token):
    users = mongo.db.users
    new_vows = request.get_json(force=True)['vows']
    student = users.find_one({"token":student_token})
    student_updated = users.update_one({"token":student_token}, {"$set" : {"vows":new_vows}})
    if student_updated:
        output = {}
        output["token"] = student_token
        html_code = 200
        msg = Message("Voeux enregistrés",
                  sender="no-reply@questionnaire-DLC.com",
                  recipients=[student['email']])
        mail.send(msg)
    else:
        output = "Could not add student's vows"
        html_code = 400
    return jsonify({'result': output}), html_code


@app.route('/login/<token>')
@cross_origin(origin=site_url,headers=['Content-Type','Authorization'])
def login_service(token):
    users = mongo.db.users
    student = users.find_one({"token" : token})
    if student:
        output = student["id"]
        html_code = 200
        return get_student_by_id(output)
    else:
        output = "No matching student for this token"
        html_code = 400
        return jsonify({"result":output}),html_code






@app.route('/admin/solve-courses/', methods=['POST'])
@cross_origin(origin=site_url,headers=['Content-Type','Authorization'], supports_credentials=True)
def solve_courses():
    students_from_db = mongo.db.users.find({"type" : "student"})
    students = []
    for student_from_db in students_from_db:
        current_student = data_structs.student(id = student_from_db["id"])
        current_vows = []
        for vow_from_db in student_from_db["vows"]:
            current_vow = data_structs.vow()
            print(vow_from_db)
            current_vow.from_dict(vow_from_db)
            current_student.vows.append(current_vow)

        current_student.name = student_from_db["name"]
        current_student.id = student_from_db["id"]
        students.append(current_student)
    courses_from_db = mongo.db.courses.find()
    courses = []
    for course_from_db in courses_from_db:
        course = data_structs.course(course_from_db["id"],
                        course_from_db["name"],
                        course_from_db["language"],
                        course_from_db["creneaux"],
                        course_from_db["min_students"],
                        course_from_db["max_students"])
        courses.append(course)
    solve(courses, students)
    for student in students:
        mongo.db.users.update_one({"id" : student.id}, {"$set":{"courses" : [c.to_dict() for c in student.courses]}})
    return jsonify(students), 200






if __name__ == '__main__':
    app.run(debug=True)
