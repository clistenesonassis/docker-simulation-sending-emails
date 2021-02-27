from bottle import route, run, request


@route('/', method='POST')
def send():
    email = request.forms.get('email')
    message = request.forms.get('message')
    subject = request.forms.get('subject')
    return 'Enviando Msg!!! email: {} subject: {} Messagem: {}'.format(
        email, subject, message
    )


if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=True)
