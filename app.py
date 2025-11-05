from flask import Flask, jsonify, request

app = Flask(__name__)

#　メモリ内データストレージ
tasks = []
task_id_counter = 1

@app.route('/')
def home():
    return jsonify({"message": "Task Management API"})

@app.route('/tasks', methods = ['GET'])
def get_tasks():
    return jsonify({"tasks": tasks})

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_counter
    data = request.get_json()

    new_task = {
        "id": task_id_counter,
        "title": data.get("title"),
        "completed": False
    }

    tasks.append(new_task)
    task_id_counter += 1

    return jsonify(new_task), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
