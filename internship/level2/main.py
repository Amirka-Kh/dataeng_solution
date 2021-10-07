# import level1.reader
import psycopg2
import psycopg2.extras

conn = None

try:
    with psycopg2.connect(dbname='p-data',
                            user='postgres',
                            password='postgres',
                            host='localhost',
                            port=5432) as conn:
        with conn.cursor() as cur:
            # cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            cur.execute('DROP TABLE IF EXISTS users')

            create_script = ''' CREATE TABLE IF NOT EXISTS users (
                                    id int PRIMARY KEY,
                                    first_name varchar(40) NOT NULL,
                                    last_name varchar(40) NOT NULL,
                                    birth bigint,
                                    img_path varchar(100))'''
            cur.execute(create_script)

            insert_script = '''INSERT INTO users (id, first_name, last_name, birth, img_path)
                                VALUES (%s, %s, %s, %s, %s)'''
            insert_values = [(100, 'James', 'Moris', 13421452341, 'https://www.google.com'),
                             (101, 'Jack', 'Minet', 13421412441, 'https://www.google.com')]

            for record in insert_values:
                cur.execute(insert_script, record)

            #
            # update_value = 'https://www.youtube.com'
            # update_script = "UPDATE users SET img_path = %s"
            # cur.execute(update_script, update_value)
            update_script = "UPDATE users SET img_path = 'www.youtube.com'"
            cur.execute(update_script)

            delete_script = '''DELETE FROM users WHERE first_name = %s'''
            cur.execute(delete_script, ('Jack',))

            cur.execute('SELECT * FROM users')
            for record in cur.fetchall():
                print(record)
                # print(record[0], record[2])
                # print(record['id']) # for DictCursor

            conn.commit()
except Exception as e:
    print(e)
finally:
    if conn is not None:
        conn.close()



