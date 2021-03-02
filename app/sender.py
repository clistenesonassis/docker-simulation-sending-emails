import psycopg2
import redis
import json
import os
from bottle import Bottle, request


class Sender(Bottle):
    def __init__(self):
        super().__init__()
        self.route('/', method='POST', callback=self.send)

        redis_host = os.getenv('REDIS_HOST')
        redis_port = os.getenv('REDIS_PORT')
        redis_db = os.getenv('REDIS_DB')
        self.queue = redis.StrictRedis(
            host=redis_host, port=redis_port, db=redis_db)

        db_host = os.getenv('DB_HOST',)
        db_user = os.getenv('DB_USER')
        db_name = os.getenv('DB_NAME')
        db_password = os.getenv('DB_PASSWORD')

        DSN = f'dbname={db_name} user={db_user} host={db_host} password={db_password}'
        self.conn = psycopg2.connect(DSN)

    def register_message(self, subject, message):
        SQL = 'INSERT INTO emails (subject, message) VALUES (%s, %s)'
        cur = self.conn.cursor()
        cur.execute(SQL, (subject, message))
        self.conn.commit()
        cur.close()

        msg = {
            'subject': subject,
            'message': message,
        }
        self.queue.rpush('sender', json.dumps(msg))

        print('Recorded Message!')

    def send(self):
        email = request.forms.get('email')
        message = request.forms.get('message')
        subject = request.forms.get('subject')

        self.register_message(subject, message)

        return 'Enviando Msg!!! email: {} subject: {} Messagem: {}'.format(
            email, subject, message
        )


if __name__ == '__main__':
    sender = Sender()
    sender.run(host='0.0.0.0', port=8080, debug=True)
