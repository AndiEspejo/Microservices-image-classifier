import json
import os
import time

import numpy as np
import redis
import settings
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import decode_predictions, preprocess_input
from tensorflow.keras.preprocessing import image

db = redis.Redis(host=settings.REDIS_IP, port=settings.REDIS_PORT, db=settings.REDIS_DB_ID)

model = ResNet50(weights='imagenet')


def predict(image_name):
    """
    Load image from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.

    Parameters
    ----------
    image_name : str
        Image filename.

    Returns
    -------
    class_name, pred_probability : tuple(str, float)
        Model predicted class as a string and the corresponding confidence
        score as a number.
    """
    class_name = None
    pred_probability = None
    # TODO: Implement the code to predict the class of the image_name

    # Load image
    full_img_path = os.path.join(settings.UPLOAD_FOLDER, image_name)
    img = image.load_img(full_img_path, target_size=(224, 224))

    x = image.img_to_array(img)
    x_batch = np.expand_dims(x, axis=0)
    x_batch = preprocess_input(x_batch)

    preds = model.predict(x_batch)

    decoded_preds = decode_predictions(preds, top=1)[0]
    _, class_name, pred_probability = decoded_preds[0]

    # Convert probabilities to float and round it
    pred_probability = round(float(pred_probability), 4)

    return class_name, pred_probability


def classify_process():
    """
    Loop indefinitely asking Redis for new jobs.
    When a new job arrives, takes it from the Redis queue, uses the loaded ML
    model to get predictions and stores the results back in Redis using
    the original job ID so other services can see it was processed and access
    the results.

    Load image from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.
    """
    while True:
        job = db.brpop(settings.REDIS_QUEUE)
        job_data = json.loads(job[1])
        image_name = job_data['image_name']
        image_path = os.path.join(settings.UPLOAD_FOLDER, image_name)
        class_name, pred_probability = predict(image_path)

        # Important! Get and keep the original job ID
        job_id = job_data['id']
        class_name, pred_probability = predict(image_path)
        # Prepare a new JSON with the results
        output = {"prediction": class_name, "score": pred_probability}

        db.set(job_id, json.dumps(output))

        # Sleep for a bit
        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    # Now launch process
    print("Launching ML service...")
    classify_process()
