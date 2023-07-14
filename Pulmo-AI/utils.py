import json
import os
import plotly

from plots import plot_image, plot_prediction


def search_file(filename, path):
    for item in os.listdir(path):
        if filename == item.split(".")[0]:
            return "static/uploads/" + item
    else:
        return "file not found"


def create_fig(filename, path):
    image_path = search_file(filename, path)
    json_path = image_path.replace("uploads", "desc").split(".")[0] + ".json"
    with open(json_path) as f:
        json_dict = json.load(f)

    fig = plot_image(image_path)
    return fig, json_dict


def fetch_user():
    with open("Creds/loged_in_user.json", "r") as file:
        creds = json.load(file)
        uid = creds["localId"]
        name = creds["name"]
    return name, uid


def get_working_image_info():
    with open("Creds/pulmo-image.json", "r") as file:
        creds = json.load(file)
        uid = creds["localId"]
        name = creds["name"]
    return name, uid

def theme_selector():
    with open("Creds/theme.json", "rb") as file:
        theme = json.load(file)
        theme = theme["theme"]
    if theme == "dark":
        plotly.io.templates.default = "plotly_dark"
    else:
        plotly.io.templates.default = "plotly_dark"
    return theme
    
    
def fetch_image_url_filename():
    with open("Creds/pulmo-image.json", "r") as file:
        json_file = json.load(file)
        used_image_url  = json_file["used-image"]
        filename = json_file["filename"]
    return used_image_url, filename

def save_image_url_filename(used_image_url, filename):
    with open("Creds/pulmo-image.json", "w") as file:
        used_image = {
            "used-image": used_image_url,
            "filename": filename,
        }
        json.dump(used_image, file)
        return used_image_url, filename
    