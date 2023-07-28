from corsheaders.signals import check_request_enabled

PUBLIC_API_PATH = [
    '/api/v1/events/accept-payment/',
    '/api/v1/events/money-transfer/'
]


def cors_allow_api_to_everyone(sender, request, **kwargs):
    return request.path in PUBLIC_API_PATH


check_request_enabled.connect(cors_allow_api_to_everyone)
