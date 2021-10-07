import io
import os.path
import pandas as pd
import psycopg2.extras
import requests
import numpy
from psycopg2.extensions import register_adapter, AsIs
import pathlib


def adapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)


def adapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)


register_adapter(numpy.float64, adapt_numpy_float64)
register_adapter(numpy.int64, adapt_numpy_int64)

url = "https://raw.githubusercontent.com/provectus/internship/main/dataeng/02-src-data/"
order = ''
index = 0
conn = None  # to connect database

# I keep dictionaries to check if data record has change
try:
    temp = pd.read_csv('./csv_files/hash_id.csv')
    hash_id = temp.to_dict()
    os.path.remove('./csv_files/hash_id.csv')
    temp = pd.read_csv('./csv_files/img_paths.csv')
    img_urls = temp.to_dict()
    os.path.remove('./csv_files/img_paths.csv')
except Exception as e:
    hash_id = {}
    img_urls = {}

try:
    output_file = pd.read_csv('./csv_files/output.csv')
    os.path.remove('./csv_files/output.csv')
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
            output_file.at[int(index), 'img_path'] = img_path
            img_urls[index] = [img_path]
    else:
        hash_id[index] = [order]
        img_urls[img_path] = [img_path]
        output_file = output_file.append(file, True)
    index += 1

path = pathlib.Path().resolve() / 'csv_files'
output_file.to_csv(os.path.join(path, r'output.csv'))

table_id = pd.DataFrame.from_dict(hash_id)
table_id.to_csv(os.path.join(path, r'hash_id.csv'))

img_paths = pd.DataFrame.from_dict(img_urls)
img_paths.to_csv(os.path.join(path, r'img_paths.csv'))

try:
    with psycopg2.connect(dbname='p-data',
                          user='postgres',
                          password='postgres',
                          host='localhost',
                          port=5432) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            # for now it is the easiest to process new data
            # it is very bad in terms of computational cost
            cur.execute('DROP TABLE IF EXISTS users')

            create_script = ''' CREATE TABLE IF NOT EXISTS users (
                                    id bigint PRIMARY KEY,
                                    first_name varchar(40) NOT NULL,
                                    last_name varchar(40) NOT NULL,
                                    birth bigint,
                                    img_path varchar(100))'''
            cur.execute(create_script)

            output_list = list(output_file.to_records(index=False))
            insert_script = '''INSERT INTO users (id, first_name, last_name, birth, img_path)
                                VALUES (%s, %s, %s, %s, %s)'''
            for record in output_list:
                cur.execute(insert_script, record)

            # update_script = "UPDATE users WHERE id = 1 SET img_path = 'www.youtube.com'"
            # cur.execute(update_script)

            cur.execute('SELECT * FROM users')
            for record in cur.fetchall():
                print(record)
            conn.commit()
except Exception as e:
    print(e)
finally:
    if conn is not None:
        conn.close()
