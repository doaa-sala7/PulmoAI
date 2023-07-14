import datetime
import json
from firebase_admin import credentials, firestore, initialize_app, storage, auth
import firebase_admin
import pyrebase

storage_loaction = "pulmoai-b3fa7.appspot.comg/images"

config = {
    "apiKey": "AIzaSyBMDEOOYHVWtPYuzC1eaYw_vU_XOsd4SYg",
    "authDomain": "pulmoai-b3fa7.firebaseapp.com",
    "projectId": "pulmoai-b3fa7",
    "storageBucket": "pulmoai-b3fa7.appspot.com",
    "messagingSenderId": "244590506149",
    "appId": "1:244590506149:web:b05d76aed1127694225d4c",
    "measurementId": "G-Q4C767572X",
    # "serviceAccount": r"Creds\firestore-creds.json",
    "databaseURL": "https://pulmoai-b3fa7-default-rtdb.europe-west1.firebasedatabase.app/",
}


# * old method for firebase
# import pyrebase
# firebase = pyrebase.initialize_app(config)
# firebase_storage = firebase.storage()
# firebase_auth = firebase.auth()

# # * Set up a credential
# cred = credentials.Certificate(r"Creds\firestore-creds.json")
# initialize_app(cred)
# db = firestore.client()

# * new method for firebase using firebase_admin
cred = credentials.Certificate(r"Creds\firestore-creds.json")
firebase = firebase_admin.initialize_app(credential=cred, options=config)
firebase_storage = storage.bucket()
firebase_auth = auth
db = firestore.client()


def get_locations(collection, document):
    images_retrieved = (
        db.collection(collection).document(document).get().to_dict()["images"]
    )
    locations = [image["location"] for image in images_retrieved]
    return locations


def create_user(collection, display_name, uid, password):
    print("creating New User...")
    db.collection(collection).document(uid).set(
        {
            "uid": uid,
            "name": display_name,
            "images": [],
            "password": password, #TODO: Hash password
        }
    )


def get_name_from_uid(collection, uid):
    return db.collection(collection).document(uid).get().to_dict()["name"]


def create_form_data(
    image_type="Xray",
    image_path="static/sample/covid4.png",
    description="This is a sample description",
    id="patient1",
    diagnose="Covid",
):
    filename = image_path.split("/")[-1]
    data = {
        "image_type": image_type,
        "description": description,
        "id": id,
        "filename": filename,
        "location": storage_loaction + "/" + filename,
        "diagnose": diagnose,
    }
    return data, image_path


def search_similar_images(images, filename):
    for idx, image in enumerate(images):
        if image["filename"] == filename:
            return idx, True
    return -1, False


def updateDB(
    collection,
    document,
    data,
    upload_path,
    create_new_user=False,
):
    results = db.collection(collection).document(document).get()
    if results.exists:
        images = results.to_dict()["images"]

        filename = data["filename"]
        cloud_path = "images/" + filename
        idx, image_found = search_similar_images(images, filename)
        firebase_storage.blob(cloud_path).upload_from_filename(upload_path)

        if image_found:
            images[idx] = data
            print("Image Updated")
        else:
            images.append(data)
            print("Image Added")

        db.collection(collection).document(document).update({"images": images})
    else:
        print("Document does not exist")
    # if create_new_user:
    #     create_user(collection, document, document)
    #     updateDB(collection, document, data, upload_path)
    #     print("New User Created")


def create_timed_url(location):
    filename = location.split("/")[-1]
    blob = firebase_storage.blob("images/" + filename)
    expiration = datetime.datetime.now() + datetime.timedelta(minutes=60)
    timed_url = blob.generate_signed_url(expiration=expiration, version="v4")
    return timed_url


def requestDB(collection, document):
    all_data = db.collection(collection).document(document).get().to_dict()["images"]
    for item in all_data:
        item["url"] = create_timed_url(item["location"])
    db.collection(collection).document(document).update({"images": all_data})
    return all_data


def request_image_info(collection, document, filename):
    all_data = db.collection(collection).document(document).get().to_dict()["images"]
    for item in all_data:
        if item["filename"] == filename:
            return item
    return None

def verify_password(collection, document, password):
    if password == db.collection(collection).document(document).get().to_dict()["password"]:
        return True
    else:
        return False


def login_fb(email):
    try:
        msg = firebase_auth.get_user_by_email(email)
        print("Authentication successful.")
    except firebase_auth.UserNotFoundError:
        msg = "User not found."
    except:
        msg = "Invalid Email or Password."
    return msg





def signup_fb(email, password, username):
    try:
        msg = firebase_auth.create_user(
            email=email, password=password, display_name=username
        )
        
        print("Signed in successfully")
    except firebase_auth.EmailAlreadyExistsError:
        msg = "User already exists."
    except:
        msg = "User already exists."

    return msg


def download(filename):
    download_path = f"static/download/downloaded.{filename.split('.')[-1]}"
    blob = firebase_storage.blob("images/" + filename)
    blob.download_to_filename(download_path)
    print("Image downloaded successfully.")
    return download_path
    


if __name__ == "__main__":
    # create_user("Users", "name", "1234", "password")
    download('covid1.jpeg')
