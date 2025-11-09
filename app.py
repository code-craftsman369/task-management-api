from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

# JSONファイルのパス
DATA_FILE = 'tasks.json'

#　データを読み込む関数
def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# データを保存する関数
def save_tasks():
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


#　メモリ内データストレージ
tasks = load_tasks()
task_id_counter = max([task['id'] for task in tasks], default=0) + 1

@app.route('/')
def home():
    return jsonify({"message": "Task Management API"})

@app.route('/tasks', methods = ['GET'])
def get_tasks():
    """タスク一覧取得(フィルタリング対応)"""
    status = request.args.get('status')

    if status == 'completed':
        filtered_tasks = [task for task in tasks if task['completed']]
        return jsonify({"tasks": filtered_tasks})
    elif status == 'incomplete':
        filtered_tasks = [task for task in tasks if not task['completed']]
        return jsonify({"tasks": filtered_tasks})

    return jsonify({"tasks": tasks})

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_counter
    data = request.get_json()

    # エラーハンドリング
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
    
    if not data['title'].strip():
        return jsonify({"error": "Title cannot be empty"}), 400

    new_task = {
        "id": task_id_counter,
        "title": data.get("title"),
        "completed": False
    }

    tasks.append(new_task)
    task_id_counter += 1

    save_tasks()

    return jsonify(new_task), 201

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    # タスクIDで検索
    for task in tasks:
        if task['id'] == task_id:
            return jsonify(task)

    # 見つからない場合
    return jsonify({"error": "Task not found"}), 404


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    # タスクを検索
    for task in tasks:
        if task['id'] == task_id:
            # リクエストからデータを取得
            data = request.get_json()

            # タスクを更新
            if 'title' in data:
                task['title'] = data['title']
            if 'completed' in data:
                task['completed'] = data['completed']

            save_tasks()

            return jsonify(task)
        
    # 見つからない場合
    return jsonify({"error": "Task not found"}), 404

@app.route('/tasks/<int:task_id>/toggle', methods=['PATCH'])
def toggle_task(task_id):
    """タスクの完了状態を切り替え"""
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = not task['completed']
            save_tasks()
            return jsonify({
                "message": "Task status toggled",
                "task": task
            })

    return jsonify({"error": "Task nof found"}), 404


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks

    # タスクを検索して削除
    for i, task in enumerate(tasks):
        if task['id'] == task_id:
            deleted_task = tasks.pop(i)
            save_tasks()
            return jsonify({"message": "Task deleted", "task": deleted_task})

    # 見つからない場合
    return jsonify({"error": "Task nof found"}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5001)

