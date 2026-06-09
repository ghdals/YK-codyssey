import csv
from pathlib import Path

import mysql.connector


def load_env():
    """'.env' 파일을 읽어 환경설정을 딕셔너리로 반환한다."""

    env_path = Path(__file__).parent / '.env'
    env = {}

    with open(env_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith('#'):
                continue

            key, value = line.split('=', 1)
            env[key] = value

    return env


def get_csv_path():
    return Path(__file__).parent / 'mars_weathers_data.csv'


def connect_mysql():
    # 수행과제 : Python 코드와 MySQL 연결

    env = load_env()

    return mysql.connector.connect(
        host=env['MYSQL_HOST'],
        user=env['MYSQL_USER'],
        password=env['MYSQL_PASSWORD'],
        database=env['MYSQL_DATABASE']
    )


def read_weather_csv():
    # 수행과제 : mars_weathers_data.csv 파일 읽기

    csv_path = get_csv_path()
    weather_data = []

    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            weather_data.append(row)

    return weather_data


def insert_weather_data(connection, weather_data):
    cursor = connection.cursor()

    # 수행과제 : CSV 내용을 INSERT 쿼리로 변환

    insert_query = '''
        INSERT INTO mars_weather (
            mars_date,
            temp,
            storm
        )
        VALUES (%s, %s, %s)
    '''

    # 수행과제 : INSERT 쿼리를 반복 실행하여 데이터 저장

    for row in weather_data:
        values = (
            row['mars_date'],
            int(row['temp']),
            int(row['storm'])
        )

        cursor.execute(insert_query, values)

    connection.commit()
    cursor.close()


def print_weather_summary(connection):
    cursor = connection.cursor()

    select_query = '''
        SELECT
            weather_id,
            mars_date,
            temp,
            storm
        FROM mars_weather
    '''

    cursor.execute(select_query)

    rows = cursor.fetchall()

    for row in rows:
        print(row)

    cursor.close()


def main():
    connection = connect_mysql()

    weather_data = read_weather_csv()

    print('[CSV 데이터 확인]')

    for row in weather_data:
        print(row)

    insert_weather_data(connection, weather_data)

    print('\n[MySQL 저장 데이터]')

    print_weather_summary(connection)

    connection.close()


if __name__ == '__main__':
    main()