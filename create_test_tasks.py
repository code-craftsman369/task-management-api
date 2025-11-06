import requests

# タスクを2つ作成
tasks_to_create = [
    {"title": "Flask学習"},
    {"title":"API開発"}
]

for task_data in tasks_to_create:
    response = requests.post(
        'http://127.0.0.1:5000/tasks',
        json=task_data
    )
    print(f"作成しました:{response.json()}")

# タスク一覧を確認
response = requests.get('http:127.0.0.1:5000/tasks')
print(f"\nタスク一覧: {response.json()}")


