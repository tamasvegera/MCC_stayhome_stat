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

def get_block_operations(block):
    block_op_count = 0
    operations = []

    while True:
        msg = {"jsonrpc": "2.0", "method": "getblockoperations", "params": {"block": block, "start": block_op_count, "max": 100}}
        response_raw = requests.post(wallet_server_ip_port, json=msg)
        response = json.loads(response_raw.text)

        temp_op_count = len(response["result"])
        for i in range(temp_op_count):
            operations.append(response["result"][i])
        block_op_count += temp_op_count

        if temp_op_count < 100:     # block operations are requested in batches of 100. If there are less ops, we can quit.
            return operations