from app import app
from models.user_model import user_model
from flask import request,send_file
from datetime import datetime
from models.auth_model import auth_model



obj = user_model()
auth = auth_model()


@app.route("/user/all")
@auth.token_auth("/user/all")
def all_users():
    return obj.all_user_model()

@app.route("/user/add", methods =["POST"])
def create_user():
    return obj.add_user(request.form)

@app.route("/user/update", methods =["PUT"])
def user_update():
    return obj.update_user(request.form)

@app.route("/user/delete/<Id>", methods =["DELETE"])
def user_delete(Id):
    return obj.delete_user(Id)

@app.route("/user/patch/<Id>", methods =["PATCH"])
def user_patch(Id):
    return obj.patch_user(request.form, Id)

@app.route("/user/getall/limit/<limit>/page/<page>", methods =["GET"])
def user_get_page(limit,page):
    return obj.page_user(limit,page)

@app.route("/user/<uid>/upload/avatar", methods =["PUT"])
def user_avatar(uid):
    file = request.files['avatar']
    time = datetime.now().timestamp()
    unique_file_name = str(time).replace(".","")
    file_name_split = file.filename.split(".")
    ext = file_name_split[-1]
    final_path = f"uploads/{unique_file_name}.{ext}"
    file.save(final_path)
    return obj.avatar_user(uid,final_path)


@app.route("/uploads/<filename>")
def upload_filename(filename):
    return send_file(f"uploads/{filename}")

@app.route("/user/login",methods = ["POST"])
def user_login():
    return obj.user_login_model(request.form)