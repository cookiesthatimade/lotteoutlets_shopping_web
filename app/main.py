from flask import Flask, Response, request, render_template, jsonify
import pymysql
import time
import json
from pytz import timezone
import pytz
from logging.config import dictConfig
import logging.handlers  # 필요한 모듈을 가져옵니다.
import threading  # threading 모듈 추가
import os

# 로깅 설정 구성
dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'test_error.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'default',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file']
    }
})


app = Flask(__name__)

# DB 연결에 대한 락
connection_lock = threading.Lock()


# DB 연결 설정
def get_connection():
    connection = pymysql.connect(host='43.203.1.73',
                                 user='root',
                                 password='#leeseun80',
                                 db='subway',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


@app.route('/', methods=['GET', 'POST'])
def lotte1():
    return render_template('lotte1.html')


@app.route('/lotte2', methods=['GET', 'POST'])
def lotte2():
    return render_template('lotte2.html')


@app.route('/lotte3', methods=['GET', 'POST'])
def lotte3():
    return render_template('lotte3.html')


@app.route('/news', methods=['GET', 'POST'])
def news2():
    return render_template('news2.html')


############################################################################################
###### SSE#####
############################################################################################

@app.route('/sensing_data')
def sensing_data():
    def respond_to_client():

        while True:
            connection1 = pymysql.connect(host='3.34.168.81',
                                          user='stella',
                                          password='1111',
                                          db='sensor',
                                          cursorclass=pymysql.cursors.DictCursor)

            with connection1.cursor() as cursor:
                # 쿼리 실행하여 가장 최신의 데이터 하나 가져오기
                cursor.execute(
                    "SELECT * FROM `sensor`.`env_data` ORDER BY `date` DESC LIMIT 1;")
                latest_data = cursor.fetchone()  # 최신 데이터 가져오기

                # UTC로부터 대한민국 시간대로 변환
                korea_time = latest_data['date']

                # 데이터베이스에서 가져온 컬럼명을 기준으로 Dictionary 생성
                _data = json.dumps({'Date': korea_time.strftime("%Y-%m-%d %H:%M:%S"), 'temperature': latest_data['temperature'], 'humidity': latest_data['humidity'],
                                    'co2': latest_data['co2'], 'lux': latest_data['lux'], 'voc': latest_data['voc']})

                yield f"id: 1\ndata: {_data}\nevent: online\n\n"
                time.sleep(5)  # 5초로 설정

    return Response(respond_to_client(), mimetype='text/event-stream')


@app.route('/sensing_data2')
def sensing_data2():
    def respond_to_client():

        while True:
            connection2 = pymysql.connect(host='3.34.168.81',
                                          user='stella',
                                          password='1111',
                                          db='sensor2',
                                          cursorclass=pymysql.cursors.DictCursor)

            with connection2.cursor() as cursor:
                # 쿼리 실행하여 가장 최신의 데이터 하나 가져오기
                cursor.execute(
                    "SELECT * FROM `sensor2`.`env_data` ORDER BY `date` DESC LIMIT 1;")
                latest_data = cursor.fetchone()  # 최신 데이터 가져오기

                # UTC로부터 대한민국 시간대로 변환
                korea_time = latest_data['date']

                # 데이터베이스에서 가져온 컬럼명을 기준으로 Dictionary 생성
                _data = json.dumps({'Date': korea_time.strftime("%Y-%m-%d %H:%M:%S"), 'temperature': latest_data['temperature'], 'humidity': latest_data['humidity'],
                                    'co2': latest_data['co2'], 'lux': latest_data['lux'], 'voc': latest_data['voc']})

                yield f"id: 1\ndata: {_data}\nevent: online\n\n"
                time.sleep(5)  # 5초로 설정

    return Response(respond_to_client(), mimetype='text/event-stream')


if __name__ == '__main__':
    # 배포 시에 debug=False, host='0.0.0.0', port=80
    app.run(debug=True)


# qunicorn 실행 코드(window) : waitress-serve --listen=0.0.0.0:5000 main:app
# qunicorn 실행 코드(mac) : gunicorn --bind 0.0.0.0:5000 main:app
