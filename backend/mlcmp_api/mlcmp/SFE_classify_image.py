import sys
from EinsteinVision.EinsteinVision import EinsteinVisionService
import base64
import os
import json

FOLDER = os.path.dirname(os.path.abspath(__file__))
pem_file = os.path.join(FOLDER, 'einstein_platform.pem')
sfe_file = os.path.join(FOLDER, 'sfe_file.json')

with open(sfe_file) as json_file:
    data = json.load(json_file)
    model_id = data['model_id']
    user_email = data['user_email']


def sf_classify_image(file):

    evs = EinsteinVisionService(email=user_email, pem_file=pem_file)

    if evs.check_for_token() is None:
        evs.get_token()
        print('New Token received.')

    with open('./media/images/' + str(file), 'rb') as images_file:
        encoded_image = base64.b64encode(images_file.read())
        result = evs.get_b64_image_prediction(model_id, encoded_image)
        print(result.json())
        return result.json()


