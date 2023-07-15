import mysql.connector
import json
from flask import jsonify
from flask import make_response
from configs.config import dbconfig
from datetime import datetime
from datetime import timedelta
import jwt

class user_model():
    def __init__(self):
        self.con = mysql.connector.connect(host=dbconfig['host'],user=dbconfig['username'],password=dbconfig['password'],database=dbconfig['database'])
        print("Connection Successfull")
        self.con.autocommit=True
        self.cur = self.con.cursor(dictionary=True)
        
    def all_user_model(self):
        self.cur.execute("SELECT * FROM customer")
        result = self.cur.fetchall()
        if len(result)>0:
            #return {"data":result}
            #return make_response({"payload":result},200)
            response = jsonify({"data": result})
            response.headers['Access-Control-Allow-Origin']="*"
            return make_response(response,200)

        else:
            return jsonify({"Message": "No result Found"}), 200
        
    def add_user(self,data):
        query = """
    INSERT INTO customer (cu_first_name, cu_last_name, cu_email, cu_phone, cu_password, cu_category, cu_isemailverified, cu_isphoneverified, cu_registered_date,cu_isdeleted)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
        values = (
            data['First_Name'],
            data['Last_Name'],
            data['Email'],
            data['PhoneNo'],
            data['Password'],
            data['Category'],
            data['EmailVerified'],
            data['PhoneVerified'],
            data['RegisteredDate'],
            data['IsDeleted']
            )
        self.cur.execute(query,values)
        return jsonify({"Message": "User Created Successfully"}), 201
    
    def update_user(self, data):
        query = """
            UPDATE customer
            SET cu_first_name = %s,
                cu_last_name = %s,
                cu_email = %s,
                cu_phone = %s,
                cu_password = %s,
                cu_category = %s,
                cu_isemailverified = %s,
                cu_isphoneverified = %s,
                cu_registered_date = %s,
                cu_isdeleted = %s
            WHERE cu_id = %s;
        """
        values = (
            data['First_Name'],
            data['Last_Name'],
            data['Email'],
            data['PhoneNo'],
            data['Password'],
            data['Category'],
            data['EmailVerified'],
            data['PhoneVerified'],
            data['RegisteredDate'],
            data['IsDeleted'],
            data['CustomerId']
        )

        self.cur.execute(query, values)

        if self.cur.rowcount > 0:
            return jsonify({"Message": "User Updated Successfully"}), 201
        else:
            return jsonify({"Message": "No Update"}), 202
        
    def delete_user(self, Id):
        query = """
            DELETE FROM Customer WHERE cu_id = %s
        """

        cu_id = Id  # Assuming the ID is directly passed as the 'Id' argument

        self.cur.execute(query, (cu_id,))

        if self.cur.rowcount > 0:
            return jsonify({"Message": "User Deleted Successfully"}), 200
        else:
            return jsonify({"Message": "No User Deleted"}), 202



    def patch_user(self, data, Id):
        if not isinstance(data, dict):
            return jsonify({"Message": "Invalid data format"}), 400

        query = "UPDATE customer SET "
        values = []

        for key, value in data.items():
            if isinstance(key, str) and isinstance(value, str):
                query += f"{key} = %s, "
                values.append(value)

        if not values:
            return jsonify({"Message": "No Update"}), 200

        query = query[:-2] + f" WHERE cu_id = %s"
        values.append(Id)

        self.cur.execute(query, values)

        if self.cur.rowcount > 0:
            return jsonify({"Message": "User Updated Successfully"}), 200
        else:
            return jsonify({"Message": "No Update"}), 200
        
    def page_user(self, limit, page):
        limit = int(limit)
        page  = int(page)
        start_page = (page*limit)-limit  
        #Example : 10th page se 5 data chiye to 10*5 = 50 and then sub 5 we get start point as 45 
        query = "SELECT * FROM customer LIMIT %s, %s"
        self.cur.execute(query, (start_page, limit))
        result = self.cur.fetchall()
        if len(result)>0:
            #return {"data":result}
            #return make_response({"payload":result},200)
            response = jsonify({"data": result, "page_no" :page,"page_limit":limit})
            response.headers['Access-Control-Allow-Origin']="*"
            return make_response(response,200)

        else:
            return jsonify({"Message": "No result Found"}), 200

    def avatar_user(self, uid, filepath):
        if not filepath:
            return jsonify({"Message": "Filepath is missing"}), 400

        if not uid:
            return jsonify({"Message": "UID is missing"}), 400

        query = "UPDATE customer SET cu_avatar = %s WHERE cu_id = %s;"
        values = (filepath, uid)

        try:
            self.cur.execute(query, values)
            if self.cur.rowcount > 0:
                return jsonify({"Message": "File Uploaded Successfully"}), 200
            else:
                return jsonify({"Message": "File Not Uploaded"}), 400
        except Exception as e:
            return jsonify({"Message": str(e)}), 500

    def user_login_model(self, data):
        if not data:
            return jsonify({"Message": "Data is missing"}), 400

        query = "SELECT  cu_avatar, cu_first_name, cu_last_name, cu_email, cu_phone, cu_password, cu_category, role_id from  customer WHERE cu_email = %s and cu_password = %s;"
        values = (
            data['Email'],
            data['Password'])
        self.cur.execute(query, values)
        result = self.cur.fetchall()
        userdata = result[0]
        exp_time = datetime.now() + timedelta(minutes =15)
        epoch_time = int(exp_time.timestamp())
        payload = {"data" :userdata,
                   "exp" :epoch_time
                   }
        jwttoken = jwt.encode(payload,"krishan",algorithm="HS256")
        return jsonify({"token": jwttoken, "data" : userdata,"Message": "User Login Successfully"}), 200
        # respose_data = {"data": (userdata, jwttoken), "Message": "User Login Successfully"}
        # return respose_data, 200