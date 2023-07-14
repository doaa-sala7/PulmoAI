import tensorflow as tf
from keras.preprocessing import image
from keras.utils import load_img, img_to_array

# import matplotlib.pyplot as plt
# import matplotlib
# matplotlib.use("TKAgg")
from plots import plot_prediction, plot_image
import tensorflow_addons as tfa
from PIL import Image
import numpy as np
import urllib.request
import warnings
import plotly
import json

warnings.filterwarnings("ignore")
# warnings.warn("deprecated", DeprecationWarning)
warnings.simplefilter(action="ignore", category=FutureWarning)


# path = r"static\model\CT-Model"


def load_tf_model(path):
    loaded_model = tf.keras.models.load_model(path)
    return loaded_model


def prepare_image(path):
    img = load_img(path, target_size=(224, 224))
    img = img_to_array(img)
    img_normalized = img / 255.0
    img_batch = np.expand_dims(img_normalized, axis=0)
    return img_batch


def make_prediction(img_batch, model):
    class_dict = {0: "covid", 1: "normal", 2: "pneumonia"}
    # class_dict = {value: key for key, value in class_dict.items()}
    prediction = model.predict(img_batch)
    return prediction

def swap_model(model, new_path):
    del model
    tf.keras.backend.clear_session()
    model = load_tf_model(new_path)
    return model


def Load_predict(
    used_image_url,
    models_path,
    model,
    image_type,
    debug_mode: bool = False,
):
    # * Handling the image
    image = plot_image(used_image_url)
    image_fig = json.dumps(image, cls=plotly.utils.PlotlyJSONEncoder)

    if debug_mode:
        #* don't load model
        predictions_fig = plot_prediction(image_type= image_type)
        predictions_fig = json.dumps(
            predictions_fig, cls=plotly.utils.PlotlyJSONEncoder
        )
    else:
        # * loading default model    
        adjusted_image = prepare_image(used_image_url)
        model = swap_model(model, models_path) 
        predictions = make_prediction(adjusted_image, model)[0]
        predictions_fig = plot_prediction(predictions, image_type)
        predictions_fig = json.dumps(
            predictions_fig, cls=plotly.utils.PlotlyJSONEncoder
        )
        
    # * saving jsonfig and imagefig to json file
    with open("Creds/imagefig.json", "w") as file:
        json.dump(image_fig, file)
    with open("Creds/predictionsfig.json", "w") as file:
        json.dump(predictions_fig, file)
    
    return image_fig, predictions_fig




if __name__ == "__main__":
    # * loading ct model
    from plots import plot_prediction

    # lstm_path = r"static\model\CNN-LSTM_best_model"
    # cnn_path = r"static\model\CNN_best_model"
    # ct_path = r"static\model\CT-Model"

    # img_path = r'static\download\downloaded.jpeg'

    # model = tf.keras.models.load_model('ct_on_cnn.h5')
    # model.save('CT-CNN-Model')

    # adjusted_image = prepare_image(img_path)
    # print(adjusted_image.shape)
    # model = load_tf_model(lstm_path)
    # predictions  = make_prediction(adjusted_image, model)[0]
    # fig = plot_prediction(predictions)
    # fig.show()

    # model = swap_model(model, cnn_path)
    # print(make_prediction(adjusted_image, model))

    # model = swap_model(model, ct_path)
    # print(make_prediction(adjusted_image, model))
