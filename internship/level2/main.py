from flask import Flask, render_template, request, escape
import psycopg2
import psycopg2.extras
from psycopg2.extensions import register_adapter, AsIs
import io
import os.path
import pandas as pd
import requests
import numpy

import pathlib

'''--------query select function--------'''
def query_select(img_status, min_age, max_age):
    min_age *= 365 * 24 * 3600
    max_age += 365 * 24 * 3600
    conn = None
    data = None

    try:
        with psycopg2.connect(dbname='p-data',
                              user='postgres',
                              password='postgres',
                              host='localhost',
                              port=5432) as conn:
            with conn.cursor() as cur:
                if img_status == 'True':
                    cur.execute(
                        'SELECT * FROM users WHERE birth > min_age AND birth < max_age AND image_path is not null')
                else:
                    cur.execute('SELECT * FROM users WHERE birth > min_age AND birth < max_age AND image_path is null')
                data = cur.fetchall()
                for record in data:
                    print(record)
                conn.commit()
    except Exception as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()

    return data


'''-------data processing function------'''
def adapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)


def adapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)


def register_types():
    register_adapter(numpy.float64, adapt_numpy_float64)
    register_adapter(numpy.int64, adapt_numpy_int64)


def save_files(output_file, hash_id, img_urls):
    path = pathlib.Path().resolve() / 'csv_files'
    output_file.to_csv(os.path.join(path, r'output.csv'))

    table_id = pd.DataFrame.from_dict(hash_id)
    table_id.to_csv(os.path.join(path, r'hash_id.csv'))

    img_paths = pd.DataFrame.from_dict(img_urls)
    img_paths.to_csv(os.path.join(path, r'img_paths.csv'))


def start_processing():
    register_types()

    url = "https://raw.githubusercontent.com/provectus/internship/main/dataeng/02-src-data/"
    order = ''
    index = 96
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

    # save_files(output_file, hash_id, img_urls)

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
                conn.commit()
    except Exception as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()
    return "data processing is finished"


'''-------------------------------------'''
app = Flask(__name__)


def log_request(req: 'flask_request') -> None:
    with open('vsearch.log', 'a') as journal:
        print(req.form, req.remote_addr, file=journal, sep='|')


@app.route('/output', methods=['GET', 'POST'])
def create_query() -> 'html':
    # img_status = request.form['is_image_exists']
    # min_age = request.form['min_age']
    # max_age = request.form['max_age']
    title = 'Here should be the results:'
    results = str(query_select(True, 0, 60))
    log_request(request)
    return render_template('output.html',
                           the_title=title,
                           the_results=results, )


@app.route('/status', methods=['POST'])
def do_processing() -> 'html':
    title = 'Is data processing finished?'
    result = start_processing()
    return render_template('status.html',
                           the_title=title,
                           the_result=result, )


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    title = 'Welcome to data processing web page!'
    return render_template('index.html',
                           the_title=title,)


@app.route('/viewlog')
def view_log() -> 'html':
    contents = []
    with open('vsearch.log') as log:
        for line in log:
            contents.append((escape(line)).split('|'))
    titles = ('Form Data', 'Remote_addr', 'User_agent', 'Results')
    return render_template('viewlog.html',
                           the_title='View Log',
                           the_row_titles=titles,
                           the_data=contents, )


if __name__ == '__main__':
    app.run(debug=True)
