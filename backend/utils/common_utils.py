import datetime


def process_log_string(request):
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ip = request.headers.get('X-Real-Ip')
    request_method = request.method
    request_uri = request.url
    http_user_agent = request.user_agent
    return f'[{date:.20s}] [{ip:.20s}] [{request_method:.3s}] {request_uri} {http_user_agent}'
