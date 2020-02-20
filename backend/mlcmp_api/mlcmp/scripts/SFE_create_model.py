import sys
from EinsteinVision.EinsteinVision import EinsteinVisionService
from requests.exceptions import HTTPError

model_id = '24VGIYH4UGPLGJCAB7UPAP7YNM'


def classify_image(file):

    evs = EinsteinVisionService(email='rendemehmetali@gmail.com', pem_file='einstein_platform.pem')

    if evs.check_for_token() is None:
        evs.get_token()
        print('New Token received.')

    evs.get_fileb64_image_prediction(model_id, file)
    # print(evs.get_datasets_info().json())
    # r=evs.create_dataset_synchronous('https://srv-file7.gofile.io/download/khU4yk/democrat.zip','image')
    # print(r.json())

    # res = evs.train_model('1168064', 'pol_classifier')
    # res =evs.get_model_info('24VGIYH4UGPLGJCAB7UPAP7YNM')
    # print(res.json())

'''
{'id': 1168064, 'name': 'democrat20', 'createdAt': '2020-02-10T09:23:05.000+0000', 
'updatedAt': '2020-02-10T09:23:21.000+0000', 
    'labelSummary': {
    'labels': [
        {'id': 3766899, 'datasetId': 1168064,'name': 'republican', 'numExamples': 12}, 
        {'id': 3766900, 'datasetId': 1168064, 'name': 'democrat', 'numExamples': 16}]},
        
 ~~~~~~~~~~~~~~~~model
 'modelId': '24VGIYH4UGPLGJCAB7UPAP7YNM'
 
'''