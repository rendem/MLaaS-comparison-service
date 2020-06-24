import chardet
import urllib.request
import urllib.error
import pandas as pd

with open('Democrats.csv', 'rb') as f:
    result_dem = chardet.detect(f.read())  # or readline if the file is large
with open('Republicans.csv', 'rb') as f:
    result_rep = chardet.detect(f.read())

democrat_url_list = pd.read_csv('Democrats.csv', encoding=result_dem['encoding']).image.tolist()
republican_url_list = pd.read_csv('Republicans.csv', encoding=result_rep['encoding']).image.tolist()

i = 1
for url in democrat_url_list:
    resource = urllib.request.urlopen(url)
    output = open("democrat/democrat-"+str(i)+".jpg", "wb")
    i += 1
    output.write(resource.read())
    output.close()

j = 1
for url in republican_url_list:
    try:
        resource = urllib.request.urlopen(url)
        output = open("republican/republican-"+str(j)+".jpg", "wb")
        j += 1
        output.write(resource.read())
        output.close()
    except urllib.error.HTTPError:
        print(urllib.error.HTTPError)
'''
print('started to put in zip')
with open('democrat.zip', 'wb') as fh:
    for url in democrat_url_list:
        response = requests.get(url)
        fh.write(response.content)


with open('republican.zip', 'wb') as fh:
    for url in republican_url_list:
        response = requests.get(url)
        fh.write(response.content)
print('finished to put in zip')


print('creating model')
with open('democrat.zip', 'rb') as democrat, open('republican.zip', 'rb') as republican:
    model = vr_service.create_classifier('pol_classifier_',
                                         positive_examples={"democrat": democrat},
                                         negative_examples=republican).get_result()
print(json.dumps(model, indent=2))
'''