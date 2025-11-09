# Task Management API

シンプルなタスク管理REST API（Python Flask実装）

## 機能

- タスクのCRUD操作（作成・読取・更新・削除）
- タスクの完了/未完了切り替え
- ステータスによるフィルタリング
- JSONファイルでのデータ永続化

## セットアップ

### 1. リポジトリをクローン
```bash
git clone https://github.com/code-craftsman369/task-management-api.git
cd task-management-api
```

### 2. 仮想環境を作成・有効化
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# または
venv\Scripts\activate  # Windows
```

### 3. 依存関係をインストール
```bash
pip install -r requirements.txt
```

### 4. サーバーを起動
```bash
python app.py
```

サーバーは `http://localhost:5001` で起動します。

## API エンドポイント

### 基本情報
```bash
GET /
```

レスポンス例：
```json
{
  "message": "Task Management API"
}
```

### タスク一覧取得
```bash
GET /tasks
GET /tasks?status=completed    # 完了済みのみ
GET /tasks?status=incomplete   # 未完了のみ
```

レスポンス例：
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "買い物に行く",
      "completed": false
    }
  ]
}
```

### タスク作成
```bash
POST /tasks
Content-Type: application/json

{
  "title": "新しいタスク"
}
```

### 特定タスク取得
```bash
GET /tasks/{id}
```

### タスク更新
```bash
PUT /tasks/{id}
Content-Type: application/json

{
  "title": "更新されたタスク",
  "completed": true
}
```

### タスクの完了切り替え
```bash
PATCH /tasks/{id}/toggle
```

レスポンス例：
```json
{
  "message": "Task status toggled",
  "task": {
    "id": 1,
    "title": "買い物に行く",
    "completed": true
  }
}
```

### タスク削除
```bash
DELETE /tasks/{id}
```

## 使用例（curl）
```bash
# タスク作成
curl -X POST http://localhost:5001/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"レポートを書く"}'

# 全タスク取得
curl http://localhost:5001/tasks

# タスク完了切り替え
curl -X PATCH http://localhost:5001/tasks/1/toggle

# 完了済みタスクのみ取得
curl "http://localhost:5001/tasks?status=completed"

# タスク削除
curl -X DELETE http://localhost:5001/tasks/1
```

## 技術スタック

- Python 3.x
- Flask 3.1.2
- JSON（データ永続化）

## 学習の進捗

- ✅ Day 8: 基本的なCRUD操作の実装
- ✅ Day 9: エラーハンドリングとデータ永続化
- ✅ Day 10: フィルタリング機能とToggle機能の追加

## ライセンス

MIT License
