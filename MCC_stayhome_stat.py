import stat_calc, api
import threading

stat_calc.init_files()

stat_calc_thread = threading.Thread(target=stat_calc.block_checker, args=())
stat_calc_thread.start()

api.main_api.run(port=5555)