import redis
import json
import os
from time import sleep
from random import randint

if __name__ == '__main__':
    redis_host = os.getenv('REDIS_HOST')
    redis_port = os.getenv('REDIS_PORT')
    redis_db = os.getenv('REDIS_DB')
    r = redis.Redis(
        host=redis_host, port=redis_port, db=redis_db)

    print('$ worker aguardando msg...')

    while True:
        message = json.loads(r.blpop('sender')[1])

        print('# LOG: Enviando msg...', message['subject'])
        sleep(randint(20, 50))
        print('# LOG: MSG enviada com sucesso!!')
