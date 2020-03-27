import requests, json

wallet_server_ip = 'http://localhost'
wallet_server_port = 4003
wallet_server_ip_port = wallet_server_ip + ':' + str(wallet_server_port)


def get_last_block():
    msg = {"jsonrpc": "2.0", "method": "getblockcount", "params": {"last": 1}, "id": 123}
    response_raw = requests.post(wallet_server_ip_port, json=msg)
    response = json.loads(response_raw.text)
    last_block = response["result"]
    return last_block


print(get_last_block())