from flask import Flask, jsonify, request, render_template
import json
import os
from datetime import datetime

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
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """タスク一覧取得（検索・フィルタリング・ソート対応）"""
    # クエリパラメータの取得
    status = request.args.get('status')
    priority = request.args.get('priority')
    search = request.args.get('search')
    sort_by = request.args.get('sort_by', 'created_at')
    order = request.args.get('order', 'asc')

    # フィルタリング用のリストをコピー
    filtered_tasks = tasks.copy()
    
    # ステータスでフィルタリング
    if status == 'completed':
        filtered_tasks = [task for task in filtered_tasks if task.get('completed')]
    elif status == 'incomplete':
        filtered_tasks = [task for task in filtered_tasks if not task.get('completed')]
    
    # 優先度でフィルタリング
    if priority:
        filtered_tasks = [task for task in filtered_tasks if task.get('priority') == priority]
    
    # キーワード検索（タイトルと説明）
    if search:
        search_lower = search.lower()
        filtered_tasks = [
            task for task in filtered_tasks
            if search_lower in task.get('title', '').lower() or
               search_lower in task.get('description', '').lower()
        ]

    # ソート処理
    reverse = (order == 'desc')

    if sort_by == 'priority':
        # 優先度でソート（high > medium > low）
        priority_order = {'high': 3, 'medium': 2, 'low': 1}
        filtered_tasks.sort(
            key=lambda x: priority_order.get(x.get('priority', 'medium'), 0),
            reverse=reverse
        )
    elif sort_by == 'deadline':
        # 期限でソート（Noneは最後に）
        filtered_tasks.sort(
            key=lambda x: x.get('deadline') if x.get('deadline') else '9999-12-31',
            reverse=reverse
        )
    else:  # created_at または updated_at
        filtered_tasks.sort(
            key=lambda x: x.get(sort_by, x.get('created_at', '')),
            reverse=reverse
        )

    return jsonify(filtered_tasks)

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_counter
    data = request.get_json()

    # エラーハンドリング
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
    
    if not data['title'].strip():
        return jsonify({"error": "Title cannot be empty"}), 400

    # 期限のバリデーション（あれば）
    deadline = None
    if 'deadline' in data and data['deadline']:
        try:
            deadline = datetime.fromisoformat(data['deadline'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': '期限の形式が正しくありません（YYYY-MM-DDTHH:MM:SS形式）'}), 400

    new_task = {
        "id": task_id_counter,
        "title": data.get("title"),
        "description": data.get("description", ""),
        "completed": False,
        "priority": data.get("priority", "medium"),
        "deadline": deadline.isoformat() if deadline else None,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
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

            # 期限のバリデーション（更新する場合）
            if 'deadline' in data and data['deadline']:
                try:
                    deadline = datetime.fromisoformat(data['deadline'].replace('Z', '+00:00'))
                    task['deadline'] = deadline.isoformat()
                except ValueError:
                    return jsonify({'error': '期限の形式が正しくありません'}), 400
            elif 'deadline' in data and data['deadline'] is None:
                task['deadline'] = None

            # その他のフィールドを更新
            if 'title' in data:
                task['title'] = data['title']
            if 'description' in data:
                task['description'] = data['description']
            if 'completed' in data:
                task['completed'] = data['completed']
            if 'priority' in data:
                task['priority'] = data['priority']
            
            task['updated_at'] = datetime.now().isoformat()

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

    return jsonify({"error": "Task not found"}), 404


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
    return jsonify({"error": "Task not found"}), 404

@app.route('/tasks/all', methods=['DELETE'])
def delete_all_tasks():
    global tasks

    # タスクの数を数える
    count = len(tasks)
    # すべてのタスクを削除
    tasks = []
    # ファイルに保存
    save_tasks()
    # 結果を返す
    return jsonify({"message": "ALL tasks deleted", "count": count})

@app.route('/tasks/overdue', methods=['GET'])
def get_overdue_tasks():
    """期限切れタスクの取得"""
    now = datetime.now()
    overdue_tasks = [
        task for task in tasks
        if task.get('deadline') and
           datetime.fromisoformat(task['deadline']) < now and
           not task.get('completed')
    ]

    return jsonify({
        'count': len(overdue_tasks),
        'tasks': overdue_tasks
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
    