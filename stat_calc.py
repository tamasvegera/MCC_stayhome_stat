import wallet_json_rpc, json, time

main_account = 1
stat_first_block = 229000
needed_payload = "4D617261646A204F7474686F6E"       # Maradj Otthon
stat = {"last_checked_block":stat_first_block-1, "sum_basic_rewards": 0, "sum_daily_rewards": 0}
checked_accounts = {}

first_scan_done = False

def is_first_scan_done():
    global first_scan_done

    return first_scan_done

def get_accounts():
    return checked_accounts

def get_stat():
    temp_stat = {"distributed_basic_reward":stat["sum_basic_rewards"], "distributed_daily_reward": stat["sum_daily_rewards"], "distributed_accounts": len(checked_accounts)}
    return temp_stat

def add_daily_reward_to_sum(reward):
    stat["sum_daily_rewards"] += reward

def check_op(op):
    global stat, checked_accounts

    if op["payload"] == needed_payload and op["account"] == main_account:
        # adding coins to sum
        stat["sum_basic_rewards"] += op["amount"] * (-1)  # sending coins is a negative value

        rewarded_account = str(op["dest_account"])

        # create new account if it's new. Sum_reward is not used yet.
        if rewarded_account not in checked_accounts:
            checked_accounts[rewarded_account] = {"sum_reward": op["amount"] * (-1), "today_reward": 0}

        else:
            checked_accounts[rewarded_account]["sum_reward"] += op["amount"] * (-1)

        # if this operation happened today then add to today_reward
        if int(op["time"] / 86400) == int(time.time() / 86400):
            checked_accounts[rewarded_account]["today_reward"] += op["amount"] * (-1)

def check_block(block):
    global stat, checked_accounts

    ops = wallet_json_rpc.get_block_operations(block)

    #iterating through operations in a block
    for op in ops:
        check_op(op)

    stat["last_checked_block"] = block

    # write results to file at every block
    stat_file = open("stat.txt", "w")
    stat_file.write(json.dumps(stat))
    stat_file.close()

    checked_accounts_file = open("checked_accounts.txt", "w")
    checked_accounts_file.write(json.dumps(checked_accounts))
    checked_accounts_file.close()

    print(str(block) + " checked")

def init_files():
    global stat, checked_accounts
    # open or create stat and checked_accounts files
    try:
        stat_file = open("stat.txt", "r")
        stat = json.loads(stat_file.read())
        stat_file.close()
    except:
        stat_file = open("stat.txt", "w")
        stat_file.write(json.dumps(stat))
        stat_file.close()

    try:
        checked_accounts_file = open("checked_accounts.txt", "r")
        checked_accounts = json.loads(checked_accounts_file.read())
        checked_accounts_file.close()
    except:
        checked_accounts_file = open("checked_accounts.txt", "w")
        checked_accounts_file.write(json.dumps(checked_accounts))
        checked_accounts_file.close()

def block_checker():
    global first_scan_done

    # iterating through blocks till current block
    # checking last_block for eternity
    while True:
        current_block = wallet_json_rpc.get_last_block()
        if stat["last_checked_block"] != current_block:
            for block in range(stat["last_checked_block"] + 1, current_block):
                check_block(block)
                print("Sum coins: " + str(stat["sum_basic_rewards"]) + "    Accounts count: " + str(len(checked_accounts)))
        first_scan_done = True
        time.sleep(10)