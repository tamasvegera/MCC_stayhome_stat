from flask import Flask, json
import stat_calc

main_api = Flask(__name__)

@main_api.route('/StayHomeStat', methods=['GET'])
def get_stayhome_stat():
    return json.dumps(stat_calc.get_stat())
