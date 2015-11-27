from flask import Flask, jsonify, request
import schedules
import credentials
app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_home():
    return jsonify({'message': 'Hello, World!'})

@app.route('/schedule/my', methods=['POST'])
def get_schedule():
    if not request.json or \
    not 'username' in request.json or not 'password' in request.json:
        abort(400)
    s = schedules.get_student_schedule(
        request.json['username'], request.json['password'])
    if s is None:
        abort(505)
    return jsonify({'schedule': schedules.build_schedule(s)})

@app.route('/faculty', methods=['POST'])
def get_faculty_members():
    if not request.json or \
    not 'username' in request.json or not 'password' in request.json:
        abort(400)
    key = schedules.get_key(request.json['username'], request.json['password'])[0]
    if key is None:
        abort(505)

    return jsonify({'faculty_members': schedules.get_teacher_list(key)})

@app.route('/schedule/faculty/<_id>', methods=['POST'])
def get_faculty_schedule(_id):
    if not request.json or \
    not 'username' in request.json or not 'password' in request.json:
        abort(400)
    key = schedules.get_key(request.json['username'], request.json['password'])[0]
    if key is None:
        abort(505)

    return jsonify({'faculty_id': _id, 
        'schedule': schedules.select_faculty_calendar(_id, key)})


if __name__ == '__main__':
    app.run(debug=True)