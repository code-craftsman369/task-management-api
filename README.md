# Task Management API

Flaskベースのシンプルなタスク管理REST API

## 🌟 機能

### 基本機能
- ✅ タスクの作成（CREATE）
- ✅ タスク一覧取得（READ）
- ✅ タスク詳細取得（READ）
- ✅ タスク更新（UPDATE）
- ✅ タスク削除（DELETE）
- ✅ タスク完了状態の切り替え（PATCH）
- ✅ 全タスク削除

### 高度な機能（Day 11追加）
- 🔍 **検索機能**：タイトル・説明でキーワード検索
- 🎯 **フィルタリング**：ステータス（完了/未完了）、優先度で絞り込み
- 📊 **ソート機能**：作成日時、優先度、期限で並び替え
- ⏰ **期限管理**：タスクに期限を設定
- ⚠️ **期限切れ検出**：期限切れタスクを自動検出
- 💾 **データ永続化**：JSONファイルに自動保存

## 🛠 技術スタック

- **Python** 3.13
- **Flask** 3.1
- **JSON** データストレージ

## 📦 インストール

### 1. リポジトリをクローン
```bash
git clone https://github.com/code-craftsman369/task-management-api.git
cd task-management-api
```

### 2. 依存パッケージをインストール
```bash
pip install flask
```

## 🚀 使い方

### サーバーを起動
```bash
python app.py
```

サーバーは `http://localhost:5001` で起動します。

## 📖 API エンドポイント

### 1. タスク作成

**POST** `/tasks`
```bash
curl -X POST http://localhost:5001/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "買い物",
    "description": "牛乳とパンを買う",
    "priority": "high",
    "deadline": "2025-11-15T18:00:00"
  }'
```

**レスポンス例**：
```json
{
  "id": 1,
  "title": "買い物",
  "description": "牛乳とパンを買う",
  "completed": false,
  "priority": "high",
  "deadline": "2025-11-15T18:00:00",
  "created_at": "2025-11-10T10:00:00.000000",
  "updated_at": "2025-11-10T10:00:00.000000"
}
```

---

### 2. タスク一覧取得

**GET** `/tasks`

#### 基本的な取得
```bash
curl http://localhost:5001/tasks
```

#### 検索（タイトル・説明）
```bash
curl "http://localhost:5001/tasks?search=買い物"
```

#### フィルタリング
```bash
# 完了済みタスク
curl "http://localhost:5001/tasks?status=completed"

# 未完了タスク
curl "http://localhost:5001/tasks?status=incomplete"

# 高優先度タスク
curl "http://localhost:5001/tasks?priority=high"
```

#### ソート
```bash
# 優先度順（降順）
curl "http://localhost:5001/tasks?sort_by=priority&order=desc"

# 期限順（昇順）
curl "http://localhost:5001/tasks?sort_by=deadline&order=asc"

# 作成日時順（降順）
curl "http://localhost:5001/tasks?sort_by=created_at&order=desc"
```

#### 複合クエリ
```bash
# 高優先度 + 期限順
curl "http://localhost:5001/tasks?priority=high&sort_by=deadline&order=asc"
```

---

### 3. 特定タスク取得

**GET** `/tasks/{id}`
```bash
curl http://localhost:5001/tasks/1
```

---

### 4. タスク更新

**PUT** `/tasks/{id}`
```bash
curl -X PUT http://localhost:5001/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "買い物（更新）",
    "completed": true,
    "deadline": "2025-11-20T18:00:00"
  }'
```

---

### 5. タスク完了状態の切り替え

**PATCH** `/tasks/{id}/toggle`
```bash
curl -X PATCH http://localhost:5001/tasks/1/toggle
```

---

### 6. タスク削除

**DELETE** `/tasks/{id}`
```bash
curl -X DELETE http://localhost:5001/tasks/1
```

---

### 7. 全タスク削除

**DELETE** `/tasks/all`
```bash
curl -X DELETE http://localhost:5001/tasks/all
```

---

### 8. 期限切れタスク取得

**GET** `/tasks/overdue`
```bash
curl http://localhost:5001/tasks/overdue
```

**レスポンス例**：
```json
{
  "count": 2,
  "tasks": [
    {
      "id": 1,
      "title": "月次レポート",
      "deadline": "2025-11-01T23:59:59",
      "completed": false
    }
  ]
}
```

## 📊 データ構造

### タスクオブジェクト
```json
{
  "id": 1,
  "title": "タスクのタイトル",
  "description": "タスクの説明（オプション）",
  "completed": false,
  "priority": "medium",
  "deadline": "2025-11-15T18:00:00",
  "created_at": "2025-11-10T10:00:00.000000",
  "updated_at": "2025-11-10T10:00:00.000000"
}
```

### フィールド説明

| フィールド | 型 | 必須 | 説明 | デフォルト値 |
|-----------|-----|------|------|-------------|
| `id` | int | - | 自動採番されるID | - |
| `title` | string | ✓ | タスクのタイトル | - |
| `description` | string | - | タスクの説明 | "" |
| `completed` | boolean | - | 完了状態 | false |
| `priority` | string | - | 優先度（high/medium/low） | "medium" |
| `deadline` | string | - | 期限（ISO 8601形式） | null |
| `created_at` | string | - | 作成日時 | 自動設定 |
| `updated_at` | string | - | 更新日時 | 自動設定 |

## 🎯 使用例

### ユースケース1：今日の優先タスクを確認
```bash
# 高優先度 + 期限が近い順
curl "http://localhost:5001/tasks?priority=high&sort_by=deadline&order=asc"
```

### ユースケース2：期限切れタスクを確認
```bash
curl http://localhost:5001/tasks/overdue
```

### ユースケース3：特定のキーワードでタスク検索
```bash
curl "http://localhost:5001/tasks?search=会議"
```

## 💾 データ保存

タスクデータは `tasks.json` ファイルに保存されます。
サーバーを再起動してもデータは保持されます。

## 🧪 テスト

### テストデータの作成
```bash
# 高優先度・期限あり
curl -X POST http://localhost:5001/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "プレゼン資料作成",
    "description": "来週の営業会議用",
    "priority": "high",
    "deadline": "2025-11-15T17:00:00"
  }'

# 中優先度・期限あり
curl -X POST http://localhost:5001/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "月次レポート提出",
    "description": "10月分の売上レポート",
    "priority": "medium",
    "deadline": "2025-11-20T12:00:00"
  }'

# 低優先度・期限なし
curl -X POST http://localhost:5001/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "備品の整理",
    "description": "オフィスの備品棚を整理する",
    "priority": "low"
  }'
```

## 📝 学習内容

このプロジェクトを通じて学んだこと：

- Flask による REST API 設計
- CRUD 操作の実装
- クエリパラメータの処理
- データのフィルタリング・ソート
- 日時データの扱い（datetime）
- JSON ファイルを使ったデータ永続化
- エラーハンドリング

## 🔜 今後の改善予定

- [ ] データベース連携（SQLite → PostgreSQL）
- [ ] ユーザー認証機能
- [ ] タスクのカテゴリ分類
- [ ] タスクの優先度自動調整
- [ ] 繰り返しタスク機能
- [ ] Web UIの追加

## 📄 ライセンス

MIT License

## 👤 作成者

- GitHub: [@code-craftsman369](https://github.com/code-craftsman369)
