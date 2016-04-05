from .client import HttpClient

_pool = {}


def get_client(api_address, username, password):
    client_id = api_address + username + password
    client = _pool.get(client_id, None)
    if not client:
        client = HttpClient(api_address, username, password, auto_close=True)
        _pool[client_id] = client
    return client