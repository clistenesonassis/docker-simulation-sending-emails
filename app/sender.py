import psycopg2
from bottle import route, run, request

DSN = 'dbname=email_sender user=example host=db password=123456'
SQL = 'INSERT INTO emails (subject, message) VALUES (%s, %s)'


def register_message(subject, message):
    conn = psycopg2.connect(DSN)
    cur = conn.cursor()
    cur.execute(SQL, (subject, message))
    conn.commit()
    cur.close()
    conn.close()

    print('Recorded Message!')


@route('/', method='POST')
def send():
    email = request.forms.get('email')
    message = request.forms.get('message')
    subject = request.forms.get('subject')

    register_message(subject, message)

    return 'Enviando Msg!!! email: {} subject: {} Messagem: {}'.format(
        email, subject, message
    )


if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=True)
