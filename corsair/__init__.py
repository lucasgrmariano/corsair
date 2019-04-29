from base64 import b64encode


def gen_auth(username, password):
    return b64encode(f'{username}:{password}'.encode('utf-8'))


class CorsairError(Exception):
    pass
