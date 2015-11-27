from flask import Flask, jsonify, request, abort
import schedules
import labs
app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_home():
    return app.send_static_file('index.html')

@app.route('/schedule/my', methods=['POST'])
def get_schedule():
    if not request.json or \
    not 'username' in request.json or not 'password' in request.json:
        abort(400)
    info = get_key(request.json['username'], request.json['password'])
    key = info[0]
    _id = info[1]
    if key is None:
        abort(401)

    s = schedules.get_student_schedule(key, _id)
    return jsonify({'user_id': _id, 'schedule': s})

@app.route('/faculty', methods=['POST'])
def get_faculty_members():
    if not request.json or \
    not 'username' in request.json or not 'password' in request.json:
        abort(400)
    key = schedules.get_key(request.json['username'], request.json['password'])[0]
    if key is None:
        abort(401)

    return jsonify({'faculty_members': schedules.get_teacher_list(key)})

@app.route('/schedule/faculty/<_id>', methods=['POST'])
def get_faculty_schedule(_id):
    if not request.json or \
    not 'username' in request.json or not 'password' in request.json:
        abort(400)
    key = schedules.get_key(request.json['username'], request.json['password'])[0]
    if key is None:
        abort(401)

    return jsonify({'faculty_id': _id, 
        'schedule': schedules.select_faculty_calendar(_id, key)})

@app.route('/schedule/compare/<op1>/<op2>', methods=['POST'])
def compare_schedules(op1, op2):
    if not request.json or \
    not 'username' in request.json or not 'password' in request.json:
        abort(400)
    key, _id = schedules.get_key(request.json['username'], request.json['password'])
    if key is None:
        abort(401)

    if op1 == 'me':
        s1 = schedules.get_student_schedule(key, _id)
    else:
        s1 = schedules.select_faculty_calendar(op1, key)

    if op2 == 'me':
        s2 = schedules.get_student_schedule(key, _id)
    else:
        s2 = schedules.select_faculty_calendar(op2, key)

    return jsonify({
        'person1': op1 if op1 != 'me' else _id,
        'person2': op2 if op2 != 'me' else _id,
        'common_labs': labs.intersect_schedules(s1, s2)
        })



if __name__ == '__main__':
    app.run(debug=True)