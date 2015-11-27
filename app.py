from flask import Flask, jsonify, request
import schedules
import credentials
app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_home():
    return jsonify({'message': 'Hello, World!'})

@app.route('/schedule', methods=['POST'])
def get_schedule():
    if not request.json or \
    not 'username' in request.json or not 'password' in request.json:
        abort(400)
    s = schedules.get_student_schedule(request.json['username'], request.json['password'])
    if s is None:
        abort(505)
    return jsonify({'schedule': schedules.build_schedule(s)})


if __name__ == '__main__':
    app.run(debug=True)