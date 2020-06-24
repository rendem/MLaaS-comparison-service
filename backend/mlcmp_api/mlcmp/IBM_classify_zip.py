import json
import os
from zipfile import ZipFile
from ibm_watson import VisualRecognitionV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from watson_developer_cloud import WatsonApiException
from ibm_cloud_sdk_core import ApiException
import pandas

FOLDER = os.path.dirname(os.path.abspath(__file__))
ibm_file = os.path.join(FOLDER, 'scripts/ibm.json')

with open(ibm_file) as json_file:
    data = json.load(json_file)
    API_KEY = data['apikey']
    API_URL = data['url']


def classify_zip(file):
    authenticator = IAMAuthenticator(API_KEY)
    vr_service = VisualRecognitionV3(
        version='2018-03-19',
        authenticator=authenticator
    )

    vr_service.set_service_url(API_URL)
    vr_service.set_default_headers({'x-watson-learning-opt-out': "true"})
    vr_service.set_disable_ssl_verification(True)

    confusion_matrix = {'democrat': {'true': 0, 'false': 0}, 'republican': {'true': 0, 'false': 0}}

    with ZipFile('./media/files/' + str(file), 'r') as zip_file:
        print('########## printing zip file')
        for image_file in zip_file.namelist():
            print(image_file.split('/'))
            if image_file.split('/')[1] is not '':
                with zip_file.open(image_file, 'r') as image:
                # with open(image_file, 'rb') as image:
                    expected_result: str = str(image_file.split('/')[0])
                    print('# image file: #')
                    print(image)
                    try:
                        classes = vr_service.classify(
                            images_file=image,
                            threshold=0.0,
                            classifier_ids=['polc_660192415']).get_result()
                        print('#### result : ')
                        print(str(classes['images'][0].get('classifiers')[0].get('classes')[0].get('class')))
                        actual_label: str = str(classes['images'][0].get('classifiers')[0].get('classes')[0].get('class'))

                        print(actual_label.lower())
                        print(expected_result.lower())
                        if expected_result.lower() == actual_label.lower():
                            confusion_matrix[expected_result.lower()]['true'] += 1
                        else:
                            confusion_matrix[expected_result.lower()]['false'] += 1

                    except WatsonApiException as ex:
                        print(f'Status code: {ex.code}')
                        print(f'Error message: {ex.message}')
                    except ApiException as ApiEx:
                        print(f'Status code: {ApiEx.code}')
                        print(f'Error message: {ApiEx.message}')
    print(confusion_matrix)
    return confusion_matrix

