from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
import copy
from urllib.parse import urljoin, urlencode
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
# app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, async_mode='eventlet', logger=True, engineio_logger=True, cors_allowed_origins="*")


initial_heroes = ['Sara', 'Shinobu', 'Feiyan', 'Albedo', 'Keqing', 'Chongyun',
          'Tohma', 'Shougun', 'Fischl', 'Ayaka', 'Yelan', 'Yunjin', 'Collei', 'Ganyu', 'Tartaglia',
          'Tighnari', 'Kazuha', 'Yae', 'Bennett', 'Gorou', 'Sayu', 'Shenhe', 'Rosaria_TT', 'Xingqiu',
          'Diluc', 'Ningguang', 'Cyno', 'Lisa', 'Kokomi', 'Nahida', 'Hutao', 'Layla',
          'Nilou', 'Zhongli', 'Dori', 'Ambor', 'Itto', 'Yoimiya', 'Klee', 'Ayato', 'Kaeya', 'Faruzan', 'Venti',
          'Mona', 'Barbara', 'Wanderer', 'Razor', 'Xinyan', 'Diona', 'Sucrose', 'Aloy', 'Qiqi', 'Candace', 'Xiao',
          'Eula', 'Qin', 'Heizo', 'Rosaria', 'Beidou', 'Xiangling', 'Noel']
initial_bp_order = ['ban', 'ban', 'ban', 'ban', 'ban', 'ban', 'pick', 'pick', 'pick', 'pick',
            'pick', 'pick', 'ban', 'ban', 'ban', 'ban', 'pick', 'pick', 'pick', 'pick', ]  # 预定的ban/pick顺序

heroes = copy.copy(initial_heroes)
bp_order = copy.copy(initial_bp_order)
bp_status = {}  # 初始化为空字典
teams = []


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        blue_team = request.form.get('blueTeam')
        red_team = request.form.get('redTeam')
        match_name = request.form.get('matchName')

        # Create the query parameters
        blue_team_params = urlencode({"blue_team": blue_team, "red_team": red_team, "bp_team": blue_team})
        red_team_params = urlencode({"red_team": red_team, "blue_team": blue_team, "bp_team": red_team})

        # Generate the links
        blue_team_link = urljoin(request.host_url, 'bp') + "?" + blue_team_params
        red_team_link = urljoin(request.host_url, 'bp') + "?" + red_team_params
        watch_link = urljoin(request.host_url, 'watch/' + match_name)

        # Render a new page with the links
        return render_template('links.html',
                               blue_team_link=blue_team_link,
                               red_team_link=red_team_link,
                               watch_link=watch_link)

    # If it's a GET request, render the home page
    return render_template('home.html')


@app.route('/bp', methods=['GET', 'POST'])
def bp():
    # Get the team names from the query parameters
    blue_team = request.args.get('blue_team')
    red_team = request.args.get('red_team')
    bp_team = request.args.get('bp_team')
    # Pass the bp state to the template
    return render_template('bp.html', blue_team=blue_team, red_team=red_team, bp_team=bp_team)


@socketio.on('initialize')
def handle_initialize(data):
    global heroes, bp_status, bp_order, teams
    heroes = copy.copy(initial_heroes)
    bp_order = copy.copy(initial_bp_order)
    bp_status = {}
    teams = []

    # 从前端收到的消息中获取队伍名
    team1 = data['team1']
    team2 = data['team2']
    # 将队伍名添加到队伍列表中
    # global teams
    teams.extend([team1, team2, team1, team2, team1, team2,
                  team1, team2, team2, team1, team1, team2,
                  team2, team1, team2, team1,
                  team2, team1, team1, team2])


@socketio.on('bp')
def handle_bp(data):
    team = data['team']
    choice = data['choice']
    action = data['action']  # 新增的字段，代表操作是ban还是pick
    print('debug1', team, choice, action)
    # 检查发送的队伍是否是当前应该操作的队伍，以及操作是否符合预定的顺序
    # if not teams or not bp_order or team != teams[0] or action != bp_order[0]:
    #     socketio.emit('error', 'Invalid action.')
    #     return
    teams.pop(0)  # 从队伍列表中移除第一个队伍
    bp_order.pop(0)  # 从操作顺序列表中移除第一个操作
    # 处理ban/pick操作
    if team not in bp_status:
        bp_status[team] = {'picked': [], 'banned': []}
    if action == 'ban':
        if choice in heroes:
            heroes.remove(choice)
            bp_status[team]['banned'].append(choice)
    elif action == 'pick':
        if choice in heroes:
            heroes.remove(choice)
            bp_status[team]['picked'].append(choice)
    bp_status['next_team'] = teams[0] if teams else None
    print('debug2', bp_status)
    socketio.emit('update_bp', bp_status)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
