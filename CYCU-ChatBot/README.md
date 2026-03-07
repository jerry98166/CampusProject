# CYCU ChatBot - 中原大學智能問答系統

<div align="center">
  <img src="frontend/assets/images/cycu_logo.png" alt="CYCU Logo" width="200"/>
  
  [![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
  [![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
  [![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
</div>

## 📖 專案簡介

CYCU ChatBot 是一個專為中原大學打造的智能問答聊天機器人，旨在幫助學生、教職員工及訪客快速了解學校的各項規章制度、政策辦法等資訊。

### 核心功能
- 🤖 **智能問答**：基於 RAG (Retrieval-Augmented Generation) 技術，提供準確的問答服務
- 📚 **法規查詢**：涵蓋中原大學 180+ 項規章制度文件
- 💬 **上下文對話**：支援多輪對話，理解上下文關聯
- 🎨 **友善界面**：直觀的網頁聊天介面，支援深色/淺色主題切換
- 🔊 **語音輸入**：支援語音輸入問題（待開發）

### 技術架構
- **後端**：Flask + LangChain + OpenAI GPT-4
- **向量資料庫**：FAISS
- **前端**：HTML5 + CSS3 + JavaScript
- **資料來源**：中原大學官方法規文件（PDF格式）

## 🚀 快速開始

### 環境需求
- Python 3.8 或以上版本
- pip (Python 套件管理器)
- OpenAI API Key
- (可選) Docker 與 Docker Compose

### 安裝步驟

1. **克隆專案**
```bash
git clone https://github.com/yourusername/CYCU-ChatBot.git
cd CYCU-ChatBot
```

2. **建立虛擬環境**
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate     # Windows
```

3. **安裝依賴套件**
```bash
pip install -r requirements.txt
```

4. **配置環境變數**
```bash
cp .env.example .env
# 編輯 .env 文件，填入您的 OpenAI API Key
```

5. **建立向量資料庫**（首次執行）
```bash
python scripts/build_vector_store.py
```

6. **啟動應用**
```bash
python src/app.py
```

7. **訪問應用**
```
開啟瀏覽器訪問：http://localhost:8080
```

## 📋 使用 Docker 部署

```bash
# 建立並啟動容器
docker-compose up -d

# 查看日誌
docker-compose logs -f

# 停止容器
docker-compose down
```

## 📚 專案結構

```
CYCU-ChatBot/
├── data/              # 資料目錄（PDF文件、向量資料庫）
├── docs/              # 文檔（API文檔、部署指南等）
├── frontend/          # 前端代碼
├── scripts/           # 工具腳本
├── src/               # 後端源代碼
└── tests/             # 測試文件
```

詳細的專案結構說明請參考 [DEVELOPMENT.md](docs/DEVELOPMENT.md)

## 🔧 配置說明

### 環境變數
- `OPENAI_API_KEY`：OpenAI API 密鑰（必填）
- `FLASK_ENV`：Flask 運行環境（development/production）
- `VECTOR_STORE_PATH`：向量資料庫存儲路徑
- `PDF_DATA_PATH`：PDF 文件路徑

詳細配置說明請參考 [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

## 📖 API 文檔

### POST /api/chat/ask
發送問題並獲取回答

**請求體**
```json
{
  "question": "中原大學的學則是什麼？"
}
```

**回應**
```json
{
  "response": "根據中原大學學則...",
  "status": "success"
}
```

完整 API 文檔請參考 [docs/API.md](docs/API.md)

## 🧪 測試

```bash
# 運行所有測試
python -m pytest tests/

# 運行特定測試
python -m pytest tests/test_api.py

# 測試問答功能
python scripts/test_qa.py
```

## 🤝 貢獻指南

歡迎提交 Issue 或 Pull Request！

1. Fork 本專案
2. 建立您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的變更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟一個 Pull Request

## 📝 開發日誌

### Version 2.0 (2026/03/07) - 專案重構
- 重新規劃專案架構
- 模組化代碼結構
- 添加完整文檔
- 添加 Docker 支援
- 改進錯誤處理

### Version 1.0 (原始版本)
- 基本問答功能
- 簡單前端界面
- FAISS 向量資料庫整合

## 📄 授權

本專案採用 MIT 授權 - 詳見 [LICENSE](LICENSE) 文件

## 👥 開發團隊

- **專案負責人**：[您的名字]
- **指導教授**：[教授名字]
- **開發時間**：[年份]

## 📧 聯絡方式

如有任何問題或建議，請聯絡：
- Email: your.email@example.com
- GitHub Issues: [專案 Issues 頁面]

## 🙏 致謝

- 感謝中原大學提供法規文件資料
- 感謝 OpenAI 提供 GPT API
- 感謝所有開源社群的貢獻

---

<div align="center">
  Made with ❤️ for Chung Yuan Christian University
</div>
