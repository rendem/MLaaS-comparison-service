from django.conf import settings
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import VisualRecognitionV3
from watson_developer_cloud import WatsonApiException
from ibm_cloud_sdk_core import ApiException
import json

with open('scripts/ibm.json') as json_file:
    data = json.load(json_file)
    API_KEY = data['apikey']
    API_URL = data['url']

authenticator = IAMAuthenticator(API_KEY)

vr_service = VisualRecognitionV3(version='2018-03-19', authenticator=authenticator)
vr_service.set_service_url(API_URL)
vr_service.set_default_headers({'x-watson-learning-opt-out': "true"})
vr_service.set_disable_ssl_verification(True)

# creating classifier
with open('democrat/democrat1.zip', 'rb') as democrat1, \
        open('democrat/democrat2.zip', 'rb') as democrat2, \
        open('democrat/democrat3.zip', 'rb') as democrat3, \
        open('democrat/democrat4.zip', 'rb') as democrat4, \
        open('democrat/democrat5.zip', 'rb') as democrat5, \
        open('democrat/democrat6.zip', 'rb') as democrat6, \
        open('democrat/democrat7.zip', 'rb') as democrat7, \
        open('democrat/democrat8.zip', 'rb') as democrat8,\
        open('republican/republican1.zip', 'rb') as r1, \
        open('republican/republican2.zip', 'rb') as r2, \
        open('republican/republican3.zip', 'rb') as r3, \
        open('republican/republican4.zip', 'rb') as r4, \
        open('republican/republican5.zip', 'rb') as r5, \
        open('republican/republican6.zip', 'rb') as r6, \
        open('republican/republican7.zip', 'rb') as r7, \
        open('republican/republican8.zip', 'rb') as r8, \
        open('republican/republican9.zip', 'rb') as r9:
    try:
        result = vr_service.create_classifier(
            name='pol_classifier',
            democrat_positive_examples=[democrat1, democrat2, democrat3, democrat4, democrat5, democrat6, democrat7, democrat8],
            republican_positive_examples=[r1, r2, r3, r4, r5, r6, r7, r8, r9]).get_result()
        print(json.dumps(result, indent=2))
    except WatsonApiException as ex:
        print(f'Status code: {ex.code}')
        print(f'Error message: {ex.message}')
    except ApiException as ApiEx:
        print(f'Status code: {ApiEx.code}')
        print(f'Error message: {ApiEx.message}')
