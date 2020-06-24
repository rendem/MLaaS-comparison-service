import json
import os
from ibm_watson import VisualRecognitionV3
from watson_developer_cloud import WatsonApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException

FOLDER = os.path.dirname(os.path.abspath(__file__))
ibm_file = os.path.join(FOLDER, 'scripts/ibm.json')

with open(ibm_file) as json_file:
    data = json.load(json_file)
    API_KEY = data['apikey']
    API_URL = data['url']


def classify_image(file):
    authenticator = IAMAuthenticator(API_KEY)

    vr_service = VisualRecognitionV3(version='2018-03-19', authenticator=authenticator)
    vr_service.set_service_url(API_URL)
    vr_service.set_default_headers({'x-watson-learning-opt-out': "true"})
    vr_service.set_disable_ssl_verification(True)

    try:
        with open('./media/images/' + str(file), 'rb') as images_file:
            try:
                classes = vr_service.classify(
                    images_file=images_file,
                    threshold=0.0,
                    classifier_ids=['polc_660192415']).get_result()
                print(json.dumps(classes, indent=2))
            except WatsonApiException as ex:
                print(f'Status code: {ex.code}')
                print(f'Error message: {ex.message}')
            except ApiException as ApiEx:
                print(f'Status code: {ApiEx.code}')
                print(f'Error message: {ApiEx.message}')
    except FileNotFoundError:
        print('File insertion wasn\'t successful. Please try with different name or file source')
    return classes
