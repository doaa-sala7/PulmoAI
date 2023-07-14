import json, os, plotly
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as io
from flask import (
    Blueprint,
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)

from PIL import Image
from werkzeug.utils import secure_filename

from fbapp import *
from model import *
from plots import *
from utils import (
    create_fig,
    fetch_image_url_filename,
    fetch_user,
    save_image_url_filename,
    search_file,
    theme_selector,
)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
UPLOADED_IMAGES = r"static\uploads"
UPLOADED_DESC = r"static\desc"

XRAY_CNN_PATH = r"static\model\CNN_best_model"
XRAY_LSTM_PATH = r"static\model\CNN-LSTM_best_model"

CT_CNN_PATH = r"static\model\CT-CNN-Model"
CT_SE_CNN_PATH = r"static\model\CT-SE-Model"

diagnose_classes = ["Not-diagnosed", "Covid", "Pneumonia", "Normal"]
model = None


def allowed_files(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def create_app(model):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "helloworld"
    app.config["UPLOAD_FOLDER"] = UPLOADED_IMAGES
    app.config["UPLOAD_DESC"] = UPLOADED_DESC
    app.config["XRAY_CNN_PATH"] = XRAY_CNN_PATH
    app.config["XRAY_LSTM_PATH"] = XRAY_LSTM_PATH
    app.config["CT_CNN_PATH"] = CT_CNN_PATH
    app.config["CT_SE_CNN_PATH"] = CT_SE_CNN_PATH
    app.config["DOWNLOAD_IMAGE"] = None

    def get_model_pathes(image_type: str) -> dict:
        if image_type == "Xray":  # type: ignore
            models_pathes = {
                "X-ray CNN AI Model": app.config["XRAY_CNN_PATH"],
                "X-ray CNN-LSTM AI Model": app.config["XRAY_LSTM_PATH"],
            }
        else:
            models_pathes = {
                "CT SE-CNN AI Model": app.config["CT_SE_CNN_PATH"],
                "CT CNN AI Model": app.config["CT_CNN_PATH"],
            }
        return models_pathes

    from auth import auth

    app.register_blueprint(auth, url_prefix="/")

    @app.route("/home.html")
    def logo_home():
        return render_template("home.html")

    @app.route("/")
    def home():
        return render_template("home.html")

    #################################################################################
    ################################# CLOUD UPLOAD ##################################
    #################################################################################

    @app.route("/upload", methods=["GET", "POST"])  # type: ignore
    def upload():
        name, uid = fetch_user()
        if request.method == "POST":
            image = request.files["images"]
            filename = secure_filename(image.filename)  # type: ignore

            # * EMPTY NAME CASE
            if filename == "":
                return render_template(
                    "upload.html",
                    msg="No selected file",
                    msg_type="danger",
                    name=name,
                    localId=uid,
                    filename="upload",
                )
            else:
                image_path = os.path.join(UPLOADED_IMAGES, filename)
                image.save(image_path)
                data_sent = request.form.to_dict()

            if image.filename == "":
                return render_template(
                    "upload.html",
                    msg="No selected file",
                    msg_type="danger",
                    name=name,
                    localId=uid,
                )

            else:
                data_recovered, image_path = create_form_data(
                    image_type=data_sent["image_type"],
                    image_path=image_path.replace("\\", "/"),
                    description=data_sent["description"],
                    id=data_sent["id"],
                    diagnose=data_sent["diagnose"],
                )
                updateDB("Users", uid, data_recovered, image_path)

            msg = "File uploaded successfully"
            msg_type = "success"

            ################################# UPLOAD ########################################

            if request.form.get("action") == "Upload":
                return render_template(
                    "upload.html",
                    msg=msg,
                    name=name,
                    localId=uid,
                    filename=filename,
                    msg_type=msg_type,
                )

            ################################# UPLOAD & GO ###################################

            elif request.form.get("action") == "Upload_Go":
                theme = theme_selector()
                name, uid = fetch_user()
                requestDB("Users", uid)
                requested_image_data = request_image_info("Users", uid, filename)
                # return f"{requested_image_data}"

                # * saving working image info to json file
                if type(requested_image_data) == dict:
                    used_image_url, _ = save_image_url_filename(
                        requested_image_data["url"], filename
                    )

                else:
                    used_image_url, _ = fetch_image_url_filename()

                # * retrive the selected model from form
                models_pathes = get_model_pathes(requested_image_data["image_type"])  # type: ignore
                selected_model = request.form.get("model")  # type: ignore
                if selected_model == None:
                    selected_model = models_pathes[list(models_pathes.keys())[0]]

                # print(f"selected_model: {selected_model}")

                # * MODEL PREDICTION
                app.config["DOWNLOAD_IMAGE"] = download(filename)
                image_fig, predictions_fig = Load_predict(
                    app.config["DOWNLOAD_IMAGE"],
                    selected_model,
                    model,
                    image_type=requested_image_data["image_type"],
                    debug_mode=False,
                )

                return render_template(
                    "pulmoai.html",
                    name=name,
                    selected_model=selected_model,
                    models_pathes=models_pathes,
                    diagnose_classes=diagnose_classes,
                    theme=theme,
                    requested_image_data=requested_image_data,
                    graphJSON=predictions_fig,
                    imageJSON=image_fig,
                )

        elif request.method == "GET":
            msg = "Please select an image to upload"
            msg_type = "info"
            if request.form.get("action") == "Upload_Go":
                return render_template(
                    "upload.html",
                    msg="You have to upload an image fIrst",
                    msg_type="danger",
                    name=name,
                    localId=uid,
                    filename="upload",
                )
            else:
                return render_template(
                    "upload.html",
                    msg=msg,
                    name=name,
                    localId=uid,
                    filename="upload",
                    msg_type=msg_type,
                )

    #################################################################################
    ################################# CLOUD GALLERY #################################
    #################################################################################

    @app.route("/cloud_gallery", methods=["GET", "POST"])  # type: ignore
    def cloud_gallery():
        name, uid = fetch_user()
        requested_db = requestDB("Users", uid)
        if request.method == "POST":
            return render_template("main.html", requested_db=requested_db, name=name)
        elif request.method == "GET":
            return render_template("main.html", requested_db=requested_db, name=name)
        else:
            "Strange Request Method"

    #################################################################################
    ################################# IMAGE PREVIEW #################################
    #################################################################################

    @app.route("/<path:filename>", methods=["GET", "POST"])  # type: ignore
    def show_image(filename):
        if request.method == "POST":
            new_data = request.json
            with open("Creds/theme.json", "w") as file:
                json.dump(new_data, file)
            return jsonify(new_data)

        elif request.method == "GET":
            theme = theme_selector()
            name, uid = fetch_user()
            requested_image_data = request_image_info("Users", uid, filename)

            # * saving working image info to json file
            if type(requested_image_data) == dict:
                used_image_url, _ = save_image_url_filename(
                    requested_image_data["url"], filename
                )
            else:
                used_image_url, _ = fetch_image_url_filename()
            # from pprint import pprint
            # pprint(requested_image_data)

            # * retrive the selected model from form
            models_pathes = get_model_pathes(requested_image_data["image_type"])  # type: ignore
            selected_model = request.form.get("model")  # type: ignore
            if selected_model == None:
                selected_model = models_pathes[list(models_pathes.keys())[0]]

            # print(f"selected_model: {selected_model}")

            # * MODEL PREDICTION
            app.config["DOWNLOAD_IMAGE"] = download(filename)
            image_fig, predictions_fig = Load_predict(
                app.config["DOWNLOAD_IMAGE"],
                selected_model,
                model,
                image_type=requested_image_data["image_type"],
                debug_mode=False,
            )

            return render_template(
                "pulmoai.html",
                name=name,
                selected_model=selected_model,
                models_pathes=models_pathes,
                diagnose_classes=diagnose_classes,
                theme=theme,
                requested_image_data=requested_image_data,
                graphJSON=predictions_fig,
                imageJSON=image_fig,
            )

    #################################################################################
    ################################# PULMO ACTIONS #################################
    #################################################################################

    @app.route("/action", methods=["GET", "POST"])
    def pulmo_action():
        # * handeling theme
        theme = theme_selector()
        # * fetch image url from json file
        used_image_url, filename = fetch_image_url_filename()
        # * fetch user id
        name, uid = fetch_user()
        requested_image_data = request_image_info("Users", uid, filename)
        new_data = request.form.to_dict()
        requested_image_data["diagnose"] = new_data["diagnose"]  # type: ignore
        requested_image_data["description"] = new_data["description"]  # type: ignore
        models_pathes = get_model_pathes(requested_image_data["image_type"])  # type: ignore

        # * saving working image info to json file
        if type(requested_image_data) == dict:
            used_image_url, _ = save_image_url_filename(
                requested_image_data["url"], filename
            )
        else:
            used_image_url, _ = fetch_image_url_filename()

        if request.method == "POST":
            if request.form.get("action") == "Save":
                selected_model = request.form.get("model")
                # * pushing the change into firebase
                updateDB(
                    "Users", uid, requested_image_data, app.config["DOWNLOAD_IMAGE"]
                )

                # * reading jsonfig and imagefig from json file
                with open("Creds/imagefig.json", "r") as file:
                    image_fig = json.load(file)
                with open("Creds/predictionsfig.json", "r") as file:
                    predictions_fig = json.load(file)

                return render_template(
                    "pulmoai.html",
                    name=name,
                    selected_model=selected_model,
                    models_pathes=models_pathes,
                    diagnose_classes=diagnose_classes,
                    theme=theme,
                    requested_image_data=requested_image_data,
                    graphJSON=predictions_fig,
                    imageJSON=image_fig,
                )

            elif request.form.get("action") == "predict":
                selected_model = request.form.get("model")  # type: ignore

                # * MODEL PREDICTION
                app.config["DOWNLOAD_IMAGE"] = download(filename)
                image_fig, predictions_fig = Load_predict(
                    app.config["DOWNLOAD_IMAGE"],
                    selected_model,
                    model,
                    image_type=requested_image_data["image_type"],
                    debug_mode=False,
                )

                return render_template(
                    "pulmoai.html",
                    name=name,
                    selected_model=selected_model,
                    models_pathes=models_pathes,
                    diagnose_classes=diagnose_classes,
                    theme=theme,
                    requested_image_data=requested_image_data,
                    graphJSON=predictions_fig,
                    imageJSON=image_fig,
                )
            else:
                return "UNHANDLED REQUEST"
        else:
            return "GET REQUESTS ARE NOT ALLOWED"

    return app


if __name__ == "__main__":
    model = None
    app = create_app(model)
    app.run(debug=False)
