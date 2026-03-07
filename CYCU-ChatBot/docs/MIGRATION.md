# 專案重構說明

## 📋 重構概述

這個文檔說明了從舊版本到新版本 (v2.0) 的重構內容和遷移步驟。

---

## 🎯 重構目標

1. **模組化架構**: 將代碼拆分為清晰的模組和層次
2. **可維護性**: 提高代碼可讀性和可維護性
3. **可擴展性**: 便於未來功能擴展
4. **專業化**: 符合生產環境的標準
5. **文檔完整**: 提供完整的API和開發文檔

---

## 📂 新舊專案結構對比

### 舊版本結構
```
university-query-platform/
├── app.py              # 所有後端邏輯混在一起
├── fun.py              # A* 演算法（未使用）
├── index.html          # 前端頁面
├── script_test.js      # 前端 JS
├── style_test.css      # 前端 CSS
├── cycu.pdf            # PDF 文件
└── vector_store/       # 向量資料庫
```

### 新版本結構
```
CYCU-ChatBot/
├── README.md           ✨ 完整的專案說明
├── requirements.txt    ✨ 標準化依賴管理
├── .env.example        ✨ 環境變數範例
├── Docker 支援         ✨ 容器化部署
│
├── docs/               ✨ 完整文檔
│   ├── API.md
│   ├── DEPLOYMENT.md
│   └── DEVELOPMENT.md
│
├── data/               ✨ 資料管理
│   ├── raw/
│   ├── processed/
│   └── vector_store/
│
├── scripts/            ✨ 工具腳本
│   ├── build_vector_store.py
│   ├── merge_pdfs.py
│   ├── test_qa.py
│   └── migrate_from_old_project.py
│
├── src/                ✨ 模組化源代碼
│   ├── app.py         # 應用入口
│   ├── config.py      # 配置管理
│   ├── api/           # API 層
│   ├── services/      # 業務邏輯層
│   └── utils/         # 工具函數
│
├── frontend/           ✨ 前端資源
│   ├── index.html
│   └── assets/
│       ├── css/
│       ├── js/
│       └── images/
│
└── tests/              ✨ 測試框架
    ├── test_api.py
    └── test_services.py
```

---

## 🔄 主要改進

### 1. 代碼架構改進

#### 舊版本問題
- 所有邏輯混在 `app.py` 一個文件中
- 沒有明確的分層
- 硬編碼路徑
- 缺少錯誤處理

#### 新版本改進
```
✓ 三層架構: API → Services → Utils
✓ 配置集中管理
✓ 完善的錯誤處理
✓ 日誌系統
✓ 類型提示
```

### 2. 配置管理

#### 舊版本
```python
# 硬編碼在代碼中
pdf_path = "/Users/gaomenglin/Desktop/university-query-platform/cycu_merged.pdf"
```

#### 新版本
```python
# 使用環境變數和配置類
from config import get_config
config = get_config()
pdf_path = config.PDF_DATA_PATH
```

### 3. API 設計

#### 舊版本
- 單一 `/ask` 端點
- 沒有 API 文檔
- 簡單的錯誤回應

#### 新版本
- 多個端點: `/ask`, `/reset`, `/history`
- 完整的 API 文檔
- 標準化的錯誤處理
- 健康檢查端點

### 4. 前端改進

#### 舊版本
- 單一 HTML/CSS/JS 文件
- 硬編碼 API URL
- 基本的 UI

#### 新版本
- 模組化的前端結構
- 動態 API URL 配置
- 改進的 UI/UX
- 響應式設計
- 主題切換功能

---

## 🚀 遷移步驟

### 步驟 1: 準備新環境

```bash
# 1. 進入新專案目錄
cd CYCU-ChatBot

# 2. 建立虛擬環境
python -m venv venv
source venv/bin/activate

# 3. 安裝依賴
pip install -r requirements.txt
```

### 步驟 2: 遷移資料

```bash
# 執行遷移腳本
python scripts/migrate_from_old_project.py
```

或手動遷移：

```bash
# 複製 PDF 文件
cp -r ../cycu_law/*.pdf data/raw/regulations/

# 複製圖片
cp ../university-query-platform/cycu_image.png \
   frontend/assets/images/cycu_logo.png
```

### 步驟 3: 配置環境

```bash
# 1. 建立環境變數文件
cp .env.example .env

# 2. 編輯 .env，從舊專案複製必要的配置
# 特別是 OPENAI_API_KEY
```

### 步驟 4: 建立向量資料庫

```bash
# 重新建立向量資料庫（推薦）
python scripts/build_vector_store.py

# 或者複製舊的向量資料庫（如果相容）
# cp -r ../university-query-platform/vector_store/* data/vector_store/
```

### 步驟 5: 測試

```bash
# 1. 測試問答功能
python scripts/test_qa.py

# 2. 運行測試
pytest tests/

# 3. 啟動應用
python src/app.py
```

### 步驟 6: 驗證

訪問 http://localhost:8080 驗證以下功能：

- [ ] 頁面正常載入
- [ ] 可以發送問題並獲得回答
- [ ] 對話上下文正常工作
- [ ] 主題切換功能正常
- [ ] 語音輸入正常（如果支援）

---

## 🔍 功能對比

| 功能 | 舊版本 | 新版本 | 說明 |
|------|--------|--------|------|
| 基本問答 | ✓ | ✓ | 保持 |
| 對話記憶 | ✓ | ✓ | 改進 |
| 健康檢查 | ✗ | ✓ | 新增 |
| 對話重置 | ✗ | ✓ | 新增 |
| 歷史記錄 | ✗ | ✓ | 新增 |
| API 文檔 | ✗ | ✓ | 新增 |
| 測試框架 | ✗ | ✓ | 新增 |
| Docker 支援 | ✗ | ✓ | 新增 |
| 日誌系統 | 簡單 | 完整 | 改進 |
| 錯誤處理 | 基本 | 完善 | 改進 |
| 配置管理 | 硬編碼 | 環境變數 | 改進 |

---

## 📝 代碼遷移範例

### 範例 1: API 調用

**舊版本**:
```javascript
fetch('https://c1b5-111-243-149-149.ngrok-free.app/ask', {
    method: 'POST',
    body: JSON.stringify({ question: userInput })
})
```

**新版本**:
```javascript
fetch('/api/chat/ask', {  // 相對路徑，自動適應環境
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question: userInput })
})
```

### 範例 2: 配置讀取

**舊版本**:
```python
openai_api_key = os.getenv("OPENAI_API_KEY")
pdf_path = "/Users/gaomenglin/Desktop/university-query-platform/cycu_merged.pdf"
```

**新版本**:
```python
from config import get_config
config = get_config()
openai_api_key = config.OPENAI_API_KEY
pdf_path = config.PDF_DATA_PATH
```

---

## ⚠️ 注意事項

### 1. 向量資料庫兼容性

舊版本的向量資料庫**可能**與新版本不兼容。建議：
- 重新建立向量資料庫（推薦）
- 或測試舊資料庫是否可用

### 2. API URL 變更

新版本的 API 端點路徑有變化：
- 舊: `/ask`
- 新: `/api/chat/ask`

如果有外部調用，需要更新。

### 3. 環境變數

確保所有必要的環境變數都已設置：
```env
OPENAI_API_KEY=your_key_here
FLASK_ENV=development
```

### 4. Python 版本

確保使用 Python 3.8 或以上版本。

---

## 🐛 疑難排解

### 問題 1: 找不到模組

```
ModuleNotFoundError: No module named 'src'
```

**解決方案**: 確保在專案根目錄執行命令：
```bash
cd CYCU-ChatBot
python src/app.py
```

### 問題 2: 向量資料庫載入失敗

```
ValueError: 向量資料庫不存在
```

**解決方案**: 建立向量資料庫：
```bash
python scripts/build_vector_store.py
```

### 問題 3: PDF 文件找不到

```
未能從 xxx 載入任何文檔
```

**解決方案**: 確認 PDF 文件在正確位置：
```bash
ls data/raw/regulations/
# 應該顯示多個 PDF 文件
```

---

## 📚 參考文檔

完成遷移後，請參考以下文檔：

- [README.md](../README.md) - 專案概述和快速開始
- [docs/API.md](../docs/API.md) - API 使用文檔
- [docs/DEPLOYMENT.md](../docs/DEPLOYMENT.md) - 部署指南
- [docs/DEVELOPMENT.md](../docs/DEVELOPMENT.md) - 開發指南

---

## ✅ 遷移檢查清單

完成遷移後，請確認：

- [ ] 所有 PDF 文件已複製到 `data/raw/regulations/`
- [ ] 圖片資源已複製到 `frontend/assets/images/`
- [ ] `.env` 文件已正確配置
- [ ] 向量資料庫已成功建立
- [ ] 測試通過 `pytest tests/`
- [ ] 應用可以正常啟動
- [ ] 前端可以正常訪問
- [ ] 問答功能正常工作
- [ ] 舊專案可以安全歸檔/刪除

---

## 🎉 完成！

恭喜！您已成功遷移到新版本的 CYCU ChatBot。

新版本提供了：
- ✨ 更好的代碼組織
- 📚 完整的文檔
- 🧪 測試框架
- 🐳 Docker 支援
- 🚀 更易於擴展和維護

如有任何問題，請參考文檔或提交 Issue。
