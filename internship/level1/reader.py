import pandas as pd
import requests
import io

url = "https://raw.githubusercontent.com/provectus/internship/main/dataeng/02-src-data/"
order = ''
index = 0

try:
    temp = pd.read_csv('hash_id.csv')
    hash_id = temp.to_dict()
    temp = pd.read_csv('img_paths.csv')
    img_urls = temp.to_dict()
except Exception as e:
    print(e)
    hash_id = {}
    img_urls = {}

try:
    output_file = pd.read_csv('output.csv')
except Exception as e:
    output_file = pd.DataFrame()

while True:
    if index // 10 == 0:
        order = '100' + str(index)
    elif index // 10 < 10:
        order = '10' + str(index)
    else:
        order = '1' + str(index)
    temp_url = url + order + '.csv'
    read_data = requests.get(temp_url).content

    file = pd.read_csv(io.StringIO(read_data.decode('utf-8')))
    img_path = url + order + '.jpg'
    file['img_path'] = img_path
    file.insert(0, "user_id", index, True)

    if file.empty:
        print('data processing is finished')
        break

    if str(index) in hash_id.keys():
        if img_path in img_urls.keys():
            index += 1
            continue
        else:
            output_file.at[index, 'img_path'] = img_path
            img_urls[index] = [img_path]
    else:
        hash_id[index] = [order]
        img_urls[img_path] = [img_path]
        output_file = output_file.append(file, True)
    index += 1

output_file.to_csv('output.csv')

table_id = pd.DataFrame.from_dict(hash_id)
table_id.to_csv('hash_id.csv')

img_paths = pd.DataFrame.from_dict(img_urls)
img_paths.to_csv('img_paths.csv')
