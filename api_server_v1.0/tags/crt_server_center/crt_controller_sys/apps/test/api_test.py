from sanic import Sanic
from sanic.response import json

app = Sanic('test')


@app.route("/", methods=['GET'])
async def test(request):
    return json({"hello": "world"})


@app.route('/api/v1_0/new/update_state_api', methods=['POST'])
def index(request):
    if request.json:
        print(request.json)
    return json({'ok': 1})


@app.route('/api/v1_0/new/operate_reports_api', methods=['POST'])
def index1(request):
    if request.json:
        # print(request.json)
        print('操作事件数量：', len(request.json.get("records")))
    return json({'ok': 1})


@app.route('/api/v1_0/new/alarm_reports_api', methods=['POST'])
def index2(request):
    if request.json:
        # print(request.json)
        print('报警事件数量：', len(request.json.get("records")))
    return json({'ok': 1})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
