# API 文檔

## 概述

CYCU ChatBot 提供 RESTful API 用於聊天問答功能。所有 API 端點都使用 JSON 格式進行數據交換。

## 基礎 URL

```
http://localhost:8080/api/chat
```

生產環境請替換為實際的伺服器地址。

## 認證

目前版本不需要認證。未來版本可能會添加 API Key 認證機制。

---

## API 端點

### 1. 發送問題

向 AI 提問並獲取回答。

**端點**: `POST /api/chat/ask`

**請求標頭**:
```
Content-Type: application/json
```

**請求體**:
```json
{
  "question": "string (必填，長度 2-1000 字元)"
}
```

**成功回應** (200 OK):
```json
{
  "response": "AI 生成的回答內容",
  "status": "success"
}
```

**錯誤回應** (400 Bad Request):
```json
{
  "error": "錯誤訊息",
  "status": "error"
}
```

**錯誤回應** (500 Internal Server Error):
```json
{
  "error": "伺服器錯誤訊息",
  "status": "error"
}
```

**範例請求**:
```bash
curl -X POST http://localhost:8080/api/chat/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "中原大學的學則是什麼？"}'
```

**範例回應**:
```json
{
  "response": "根據中原大學學則，學則是規範學生在學期間的各項權利義務...",
  "status": "success"
}
```

---

### 2. 重置對話

清除當前的對話上下文，開始新的對話。

**端點**: `POST /api/chat/reset`

**請求標頭**: 無特殊要求

**請求體**: 無

**成功回應** (200 OK):
```json
{
  "message": "對話已重置",
  "status": "success"
}
```

**錯誤回應** (500 Internal Server Error):
```json
{
  "error": "重置對話失敗",
  "status": "error"
}
```

**範例請求**:
```bash
curl -X POST http://localhost:8080/api/chat/reset
```

---

### 3. 獲取對話歷史

獲取當前會話的對話歷史記錄。

**端點**: `GET /api/chat/history`

**請求標頭**: 無特殊要求

**請求參數**: 無

**成功回應** (200 OK):
```json
{
  "history": [
    {
      "role": "human",
      "content": "用戶的問題"
    },
    {
      "role": "ai",
      "content": "AI 的回答"
    }
  ],
  "status": "success"
}
```

**範例請求**:
```bash
curl -X GET http://localhost:8080/api/chat/history
```

---

### 4. 健康檢查

檢查服務是否正常運行。

**端點**: `GET /health`

**請求標頭**: 無特殊要求

**請求參數**: 無

**成功回應** (200 OK):
```json
{
  "status": "healthy",
  "service": "CYCU ChatBot",
  "version": "2.0.0"
}
```

**範例請求**:
```bash
curl -X GET http://localhost:8080/health
```

---

## 錯誤代碼

| HTTP 狀態碼 | 說明 |
|------------|------|
| 200 | 請求成功 |
| 400 | 錯誤的請求（參數錯誤、格式錯誤等） |
| 404 | 找不到資源 |
| 500 | 伺服器內部錯誤 |

---

## 錯誤處理

所有錯誤回應都遵循以下格式：

```json
{
  "error": "詳細的錯誤訊息",
  "status": "error"
}
```

常見錯誤訊息：

- `"問題不能為空"` - 未提供問題內容
- `"問題太短，請輸入至少2個字元"` - 問題長度不足
- `"問題太長，請限制在1000個字元以內"` - 問題超過長度限制
- `"請求格式錯誤"` - JSON 格式不正確
- `"處理問題時發生錯誤，請稍後再試"` - 伺服器處理錯誤

---

## 限制

### 速率限制

目前版本未實施速率限制。建議客戶端實施合理的請求頻率控制。

### 請求大小限制

- 問題長度：2-1000 個字元
- 請求體大小：最大 1MB

---

## 最佳實踐

1. **錯誤處理**: 始終檢查回應的 `status` 欄位
2. **超時設置**: 建議設置 30-60 秒的請求超時時間
3. **重試機制**: 對於 5xx 錯誤，可實施重試機制（建議最多重試 3 次）
4. **用戶體驗**: 在等待回應時顯示載入動畫

---

## JavaScript 範例

```javascript
async function askQuestion(question) {
    try {
        const response = await fetch('http://localhost:8080/api/chat/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question })
        });
        
        const data = await response.json();
        
        if (response.ok && data.status === 'success') {
            return data.response;
        } else {
            throw new Error(data.error || '未知錯誤');
        }
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// 使用範例
askQuestion('中原大學的學則是什麼？')
    .then(answer => console.log(answer))
    .catch(error => console.error(error));
```

---

## Python 範例

```python
import requests

def ask_question(question):
    url = 'http://localhost:8080/api/chat/ask'
    payload = {'question': question}
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        data = response.json()
        
        if response.ok and data['status'] == 'success':
            return data['response']
        else:
            raise Exception(data.get('error', '未知錯誤'))
    except requests.exceptions.RequestException as e:
        print(f'API Error: {e}')
        raise

# 使用範例
try:
    answer = ask_question('中原大學的學則是什麼？')
    print(answer)
except Exception as e:
    print(f'Error: {e}')
```

---

## 版本歷史

- **v2.0.0** (2026-03-07): 重構版本，模組化架構
- **v1.0.0** (初始版本): 基本問答功能

---

## 支援

如有問題或建議，請聯絡開發團隊或提交 GitHub Issue。
