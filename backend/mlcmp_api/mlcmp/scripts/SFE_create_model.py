import sys
from EinsteinVision.EinsteinVision import EinsteinVisionService
from requests.exceptions import HTTPError
import os
import json

FOLDER = os.path.dirname(os.path.abspath(__file__))
pem_file = os.path.join(FOLDER, 'einstein_platform.pem')
sfe_file = os.path.join(FOLDER, 'sfe_file.json')

with open(sfe_file) as json_file:
    data = json.load(json_file)
    model_id = data['model_id']
    user_email = data['user_email']


def classify_image(file):
    evs = EinsteinVisionService(email=user_email, pem_file='einstein_platform.pem')

    if evs.check_for_token() is None:
        evs.get_token()
        print('New Token received.')

    evs.get_fileb64_image_prediction(model_id, file)
    print(evs.get_datasets_info().json())
    r=evs.create_dataset_synchronous('your-file','image')
    print(r.json())

    # res = evs.train_model('1168064', 'pol_classifier')
    # res =evs.get_model_info('24VGIYH4UGPLGJCAB7UPAP7YNM')
    # print(res.json())

