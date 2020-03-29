import stat_calc, api, daily_reward_handler
import threading, schedule, time

stat_calc.init_files()

stat_calc_thread = threading.Thread(target=stat_calc.block_checker, args=())
stat_calc_thread.start()

api.main_api.run(port=5555, host='0.0.0.0')
schedule.every().day.at("23:00").do(daily_reward_handler.daily_reward)

while stat_calc.is_first_scan_done() == False:
    pass

daily_reward_handler.daily_reward()

while True:
    schedule.run_pending()