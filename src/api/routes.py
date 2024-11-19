"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from os import getenv
from flask import Flask, request, jsonify, url_for, Blueprint
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt, jwt_required
from api.models import db, User, TokenBlockedList
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from datetime import timedelta
import os
import requests
import json

app = Flask(__name__)
bcrypt = Bcrypt(app)


app=Flask(__name__)
bcrypt=Bcrypt(app)
api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/login', methods=['POST'])
def user_login():
    body = request.get_json()
    # 1. Valido los campos del body de la peticion
    if "email" not in body:
        return jsonify({"msg": "El campo email es requerido"}), 400
    if "password" not in body:
        return jsonify({"msg": "El campo password es requerido"}), 400

    # 2. Busco al usuario en la base de datos con el correo
    user = User.query.filter_by(email=body["email"]).first()

    # 2.1 Si el usuario no aparece, retorna un error 404
    if user is None:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    # 3 Verifico el campo password del body con el password del usuario de la base de datos
    password_checked = bcrypt.check_password_hash(
        user.password, body["password"])
    # 3.1 Si no se verifica se retorna un error de clave inválida 401
    if password_checked == False:
        return jsonify({"msg": "Clave invalida"}), 401

    # 4 Generar el token
    role = "admin"
    if user.id % 2 == 0:
        role = "user"
    token = create_access_token(
        identity=user.id, additional_claims={"role": role})
    output = {"token": token}

    return jsonify(output), 200


@api.route("/userinfo", methods=['GET'])
@jwt_required()
def user_info():
    user = User.query.filter_by(id=get_jwt_identity()).first()
    if user is None:
        return jsonify({"msg": "User not foud"}), 404
    payload = get_jwt()
    return jsonify({"user": user.id, "role": payload["role"]})

""" 
@api.route("/profilepic", methods=["PUT"])
@jwt_required()
def user_picture():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({"msg": "User not found"}), 404
    # Recibo el archivo
    file = request.files["profilePic"]
    extension = file.filename.split(".")[1]
    # Guardo el archivo de la peticion en un archivo temporal
    temp = NamedTemporaryFile(delete=False)
    file.save(temp.name)
    # Subir el archivo a Firebase
    bucket = storage.bucket()
    filename = "usersPictures/" + str(user_id) + "." + extension
    resource = bucket.blob(filename)
    resource.upload_from_filename(temp.name, content_type="image/" + extension)
    user.profile_pic = filename
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "Picture updated", "profilePicture": user.getProfilePicture()})
 """

@api.route("/userinfoadmin", methods=['GET'])
@jwt_required()
def user_info_admin():
    payload = get_jwt()
    if payload["role"] != "admin":
        return jsonify({"msg": "Acceso denegado"}), 401

    user = get_jwt_identity()
    payload = get_jwt()
    return jsonify({"user": user, "role": payload["role"]})

@api.route("/requestpasswordrecovery", methods=['POST'])
def request_password_recovery():
    email = request.get_json()['email']
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"msg": "Usuario no encontrado"}), 404
    password_token = create_access_token(
        identity=user.id, additional_claims={"type": "password"})
    url = os.getenv("FRONTEND_URL")
    url = url+"/changepassword?token=" + password_token

    # ______________________________
    # ENVIO DE CORREO
    # ______________________________
    send_mail_url = os.getenv("MAIL_SEND_URL")
    private_key = os.getenv("MAIL_PRIVATE_KEY")
    service_id = os.getenv("MAIL_SERVICE_ID")
    template_id = os.getenv("MAIL_TEMPLATE_ID")
    user_id = os.getenv("MAIL_USER_ID")
    data = {
        "service_id": service_id,
        "template_id": template_id,
        "user_id": user_id,
        "accessToken": private_key,
        "template_params": {
            "url": url
        }
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(
        send_mail_url, headers=headers, data=json.dumps(data))

    print(response.text)
    if response.status_code == 200:
        return jsonify({"msg": "Revise su correo para el cambio de clave "})

    else:
        return jsonify({"msg": "Ocurrio un error con el envio de correo "}), 400


@api.route("/signup",methods=["POST"])
def user_signup():
    # Recibo los datos de la peticion
    body=request.get_json()
    # Valido que tenga los campos que necesito para crear el usuario
    if body["email"] is None:
      return jsonify({"msg":"Debe especificar un email"}),400
    if body["password"] is None:
      return jsonify({"msg":"Debe especificar una contraseña"}),400
    # Se encripta la clave que se va a guardar
    body["password"]=bcrypt.generate_password_hash(body["password"]).decode("utf-8")
    # Se guarda en la base de datos
    user=User(email=body["email"], password=body["password"], is_active=True)
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg":"Usuario creado", "user":user.serialize()})


@api.route("/logout", methods=["POST"])
@jwt_required()
def user_logout():
   token_data=get_jwt()
   token_blocked=TokenBlockedList(jti=token_data["jti"])
   db.session.add(token_blocked)
   db.session.commit()
   return jsonify({"msg":"Session cerrada"})


@api.route("/changepassword", methods=["PATCH"])
@jwt_required()
def user_change_password():
  user=User.query.get(get_jwt_identity())
  if user is None:
      return jsonify({"msg": "Usuario no encontrado"}), 404
  
  new_password=request.get_json()["new_password"]
  user.password=bcrypt.generate_password_hash(new_password).decode("utf-8")
  db.session.add(user)
  #db.session.commit()

  token_data=get_jwt()
  if token_data["type"]=="password":
      token_blocked=TokenBlockedList(jti=token_data["jti"])
      db.session.add(token_blocked)
  
  db.session.commit()

  return jsonify({"msg":"Password updated"})
  """ 

@api.route("/profilepic", methods=["PATCH"])
@jwt_required()
def user_profile_picture():
  user_id=get_jwt_identity()
  user=User.query.get(user_id)
  if user is None:
      return jsonify({"msg": "Usuario no encontrado"}), 404
  file=request.files["profilePicture"]
  name=request.form["name"]
  print(name)
  extension=file.filename.split(".")[-1]
  temp=NamedTemporaryFile(delete=False)
  file.save(temp.name)

  bucket=storage.bucket(name="clase-imagenes-flask.appspot.com")
  filename="pictureslatam-35/" + str(user_id) + "."+extension
  resource=bucket.blob(filename)
  resource.upload_from_filename(temp.name, content_type="image/"+extension)

  user.profile_pic=filename
  db.session.add(user)
  db.session.commit()

  return jsonify({"msg":"Foto actualizada"})

@api.route("/profilepic", methods=["GET"])
@jwt_required()
def user_profile_picture_get():
  user_id=get_jwt_identity()
  user=User.query.get(user_id)
  if user is None:
      return jsonify({"msg": "Usuario no encontrado"}), 404
  
  bucket=storage.bucket(name="clase-imagenes-flask.appspot.com")
  resource=bucket.blob(user.profile_pic)
  picture_url=resource.generate_signed_url(version="v4",expiration=timedelta(minutes=15),method="GET")
  return jsonify({"url":picture_url}) """