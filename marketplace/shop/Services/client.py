from django.core.mail import send_mail


def send_msg_AdminMail(message):
    try:
        send_mail(
            'ՀԱՃԱԽՈՐԴԻ ՀԱՐՑ',
            message,
            'davidkostandyan71@gmail.com',
            ['davidkostandyan71@gmail.com'],
        )
        return True
    except Exception as e:
        print(e)
    return False


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip