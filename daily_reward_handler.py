import stat_calc, wallet_json_rpc

coins_per_hour = 1         # basic reward: 0.5 MCC / 30min -> 1MCC/h
daily_reward_account = 334000

# USE DESCENDING ORDER!!!
reward_chart = {        #   daily hour, reward %
    16: 400,            # 16 hours at home a day and 400% reward
    8: 200,
    4: 100,
    2: 50
}

def send_daily_reward(account, reward):
    print("Sending daily reward: account:   " + account + " reward: " +str(reward))
   #wallet_json_rpc.send_payment(daily_reward_account, account, reward, "StayHome daily reward")
    pass

def daily_reward():
    global coins_per_hour, daily_reward_account

    print("Checking daily rewards")

    accounts = stat_calc.get_accounts()

    for account in accounts:
        for hour in reward_chart:
            if accounts[account]["today_reward"] >= hour*coins_per_hour:
                reward = accounts[account]["today_reward"] * reward_chart[hour]/100
                try:
                    send_daily_reward(account, reward)
                    accounts[account]["today_reward"] = 0
                    stat_calc.add_daily_reward_to_sum(reward)
                except Exception as e:
                    print("ERROR: sending daily reward to: " + account + ", amount: ")
                    print(e)

