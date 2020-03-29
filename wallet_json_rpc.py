import requests, json

wallet_server_ip = 'http://localhost'
wallet_server_port = 4003
wallet_server_ip_port = wallet_server_ip + ':' + str(wallet_server_port)

wallet_password = ""
basic_payment_fee = 0.0001

class WalletPubKeyError(Exception):
    pass

class WalletInvalidOperationError(Exception):
    pass

class WalletNotReadyError(Exception):
    pass

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

def get_pending_operations():
    block_op_count = 0
    operations = []

    while True:
        msg = {"jsonrpc": "2.0", "method": "getpendings", "params": {"start": block_op_count, "max": 100}}
        response_raw = requests.post(wallet_server_ip_port, json=msg)
        response = json.loads(response_raw.text)

        temp_op_count = len(response["result"])
        for i in range(temp_op_count):
            operations.append(response["result"][i])
        block_op_count += temp_op_count

        if temp_op_count < 100:     # block operations are requested in batches of 100. If there are less ops, we can quit.
            return operations

def send_payment(from_account, to_account, amount, payload):
    from_account = int(from_account)
    to_account = int(to_account)
    amount = float(amount)

    payload = payload.encode('hex')
    msg = {"jsonrpc":"2.0","method":"sendto","params":{"sender":from_account,"target":to_account,"amount":amount,"fee":basic_payment_fee,"payload":payload,"payload_method":"none","pwd":wallet_password},"id":123}
    response_raw = requests.post(wallet_server_ip_port, json=msg)
    response = json.loads(response_raw.text)

    if "result" in response:
        print("Payment sent from: " + str(from_account) + " to: " + str(to_account) + ", amount: " + str(amount))
    else:
        if response["error"]["code"] == 1004:
            raise WalletInvalidOperationError
        elif response["error"]["code"] == 1005:       # invalid public key -> orphan
            raise WalletPubKeyError
        else:
            print(response)
            raise Exception