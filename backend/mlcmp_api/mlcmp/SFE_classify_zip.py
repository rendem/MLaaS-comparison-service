import json
import os
from zipfile import ZipFile
from EinsteinVision.EinsteinVision import EinsteinVisionService
import base64


FOLDER = os.path.dirname(os.path.abspath(__file__))
pem_file = os.path.join(FOLDER, 'einstein_platform.pem')
sfe_file = os.path.join(FOLDER, 'sfe_file.json')

with open(sfe_file) as json_file:
    data = json.load(json_file)
    model_id = data['model_id']
    user_email = data['user_email']


def sf_classify_zip(file):

    evs = EinsteinVisionService(email=user_email, pem_file=pem_file)

    if evs.check_for_token() is None:
        evs.get_token()
        print('New Token received.')

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

                    encoded_image = base64.b64encode(image.read())
                    result = evs.get_b64_image_prediction(model_id, encoded_image)
                    result = result.json()
                    print(result)
                    print('#### result : ')
                    if 'message' not in result.keys():
                        actual_label: str = str(result['probabilities'][0].get('label'))
                        print(actual_label.lower())
                        print(expected_result.lower())
                        if expected_result.lower() == actual_label.lower():
                            confusion_matrix[expected_result.lower()]['true'] += 1
                        else:
                            confusion_matrix[expected_result.lower()]['false'] += 1
    print(confusion_matrix)
    return confusion_matrix
