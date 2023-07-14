from flask import Blueprint, render_template, request, redirect
from fbapp import (
    login_fb,
    signup_fb,
    create_user,
    get_name_from_uid,
    requestDB,
    verify_password,
)
import json

auth = Blueprint("auth", __name__)


@auth.route("/signup", methods=["POST", "GET"])  # type: ignore
def signup_button():
    print(request.method)
    if request.method == "POST":
        return render_template("signup.html", boolean=True)
    elif request.method == "GET":
        return render_template("signup.html", boolean=True)


@auth.route("/login", methods=["POST", "GET"])
def login_button():
    if request.method == "POST":
        return render_template("login.html", show_msg=False)
    elif request.form.get("login") == "LOGIN":
        return render_template("signup.html", show_msg=False)
    else:
        return render_template("home.html", show_msg=False)


@auth.route("/signup_complete", methods=["POST", "GET"])
def signup_complete():
    if request.method == "POST":
        data = request.form.to_dict()
        email = data["email"]
        password = data["password"]
        name = data["usrname"]
        msg = signup_fb(email, password, name)
        if type(msg) == str:
            return render_template("signup.html", msg=msg, show_msg=True)
        else:
            name = msg.display_name  # type: ignore
            localId = msg.uid  # type: ignore
            with open("Creds/loged_in_user.json", "w") as file:
                json.dump({"name": name, "localId": localId}, file)
            create_user("Users", name, localId, password)
            return render_template("main.html", name=name, localId=localId)
    else:
        return "something went wrong. Try again!"


@auth.route("/login_complete", methods=["POST", "GET"])
def login_complete():
    if request.method == "POST":
        data = request.form.to_dict()
        email = data["email"]
        password = data["password"]
        msg = login_fb(email)
        if type(msg) == str:
            return render_template("login.html", msg=msg, show_msg=True)
        else:
            if verify_password("Users", msg.uid, password) == False:  # type: ignore
                return render_template(
                    "login.html", msg="Invalid Password.", show_msg=True
                )

            else:
                # localId = msg["localId"] # type: ignore
                localId = msg.uid  # type: ignore
                name = get_name_from_uid("Users", localId)
                with open("Creds/loged_in_user.json", "w") as file:
                    json.dump({"name": name, "localId": localId}, file)

                requested_db = requestDB("Users", localId)
                print(requested_db)
                return render_template(
                    "main.html", name=name, requested_db=requested_db
                )
    else:
        return "something went wrong. Try again!"


@auth.route("/logout", methods=["POST", "GET"])
def logout():
    if request.method == "POST":
        return render_template("home.html", boolean=False)
    elif request.method == "GET":
        return render_template("home.html", boolean=False)
    else:
        return "something went wrong. Try again!"


@auth.route("/reload", methods=["POST", "GET"])  # type: ignore
def reload():
    if request.method == "POST":
        return "reload successful"
