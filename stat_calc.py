import wallet_json_rpc, json, time

main_account = 1
stat_first_block = 229000
needed_payload = "4D617261646A204F7474686F6E"       # Maradj Otthon
stat = {"last_checked_block":stat_first_block-1, "sum_coins": 0}
checked_accounts = []

def check_block(block):
    global stat, checked_accounts

    ops = wallet_json_rpc.get_block_operations(block)

    #iterating through operations in a block
    for op in ops:
        if op["payload"] == needed_payload and op["account"] == main_account:
            # adding coins to sum
            stat["sum_coins"] += op["amount"]*(-1)      # sending coins is a negative value

            # store account as checked
            if op["dest_account"] not in checked_accounts:
                checked_accounts.append(op["dest_account"])

    stat["last_checked_block"] = block

    # write results to file at every block
    stat_file = open("stat.txt", "w")
    stat_file.write(json.dumps(stat))
    stat_file.close()

    checked_accounts_file = open("checked_accounts.txt", "w")
    checked_accounts_file.write(json.dumps(checked_accounts))
    checked_accounts_file.close()

    print(str(block) + " checked")

# open or create stat and checked_accounts files
try:
    stat_file = open("stat.txt", "r")
    stat = json.loads(stat_file.read())
    stat_file.close()
except FileNotFoundError:
    stat_file = open("stat.txt", "w")
    stat_file.write(json.dumps(stat))
    stat_file.close()

try:
    checked_accounts_file = open("checked_accounts.txt", "r")
    checked_accounts = json.loads(checked_accounts_file.read())
    checked_accounts_file.close()
except FileNotFoundError:
    checked_accounts_file = open("checked_accounts.txt", "w")
    checked_accounts_file.write(json.dumps(checked_accounts))
    checked_accounts_file.close()

current_block = wallet_json_rpc.get_last_block()

# iterating through blocks till current block
# checking last_block for eternity
while True:
    if stat["last_checked_block"] != wallet_json_rpc.get_last_block():
        for block in range(stat["last_checked_block"] + 1, current_block):
            check_block(block)
            print("Sum coins: " + str(stat["sum_coins"]) + "    Accounts count: " + str(len(checked_accounts)))
    time.sleep(10)