from functools import wraps
import mysql.connector
import json
from flask import jsonify
from flask import make_response,request
from configs.config import dbconfig
from datetime import datetime
from datetime import timedelta
import re
import jwt

class auth_model():
    def __init__(self):
        try:
            self.con = mysql.connector.connect(host=dbconfig['host'],user=dbconfig['username'],password=dbconfig['password'],database=dbconfig['database'])
            self.con.autocommit=True
            self.cur = self.con.cursor(dictionary=True)
            print("Connection Successfull")
        except:
            print("Error while connecting to database")


    def token_auth(self, endpoint):
        def inner1(func):
            @wraps(func)
            def inner2(*args):
                auth = request.headers.get("authorization")
                if re.match("^Bearer *([^ ]+)*$",auth,flags=0):
                    token = auth.split(" ")[1]
                    try:

                        jwtdecoded = (jwt.decode(token, "krishan", algorithms="HS256"))
                    except jwt.ExpiredSignatureError:
                        return make_response({"Error" : "Token Expire"})
                    # print(jwtdecoded)
                    # return(jwtdecoded)
                    role_id = jwtdecoded['data']['role_id']
                    self.cur.execute(f"SELECT roles from accessibility_view WHERE endpoint = '{endpoint}'")
                    result =self.cur.fetchall()
                    if len(result)>0:
                        allowed_roles = (json.loads(result[0]['roles']))
                        if role_id in allowed_roles:
                            return func(*args)
                        else:
                            return make_response({"Error": "Invalid Roles"})
                    
                    else:
                        return make_response({"Error": "Unknown End point"})
                    

                else:
                    return make_response({"Error" :"Invalid Token"}, 401)
                #return func()
            return inner2
        return inner1
