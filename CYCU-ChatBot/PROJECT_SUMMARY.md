# CYCU ChatBot - 專案規劃完整總結

## 📊 專案概況

**專案名稱**: CYCU ChatBot - 中原大學智能問答系統  
**版本**: 2.0.0  
**建立日期**: 2026年3月7日  
**技術棧**: Python, Flask, LangChain, OpenAI GPT-4, FAISS, HTML/CSS/JavaScript

---

## 🎯 專案目標

建立一個專業、可維護、可擴展的智能問答系統，用於回答中原大學相關問題。

### 核心功能
1. ✅ 基於 RAG 的智能問答
2. ✅ 支援多輪對話（上下文記憶）
3. ✅ 友善的網頁聊天界面
4. ✅ 支援深色/淺色主題切換
5. ✅ 語音輸入支援
6. ✅ 響應式設計（手機/桌面）

---

## 📁 完整專案結構

```
CYCU-ChatBot/
│
├── 📄 README.md                      # 專案說明文檔
├── 📄 requirements.txt               # Python 依賴套件清單
├── 📄 .env.example                   # 環境變數範例文件
├── 📄 .gitignore                     # Git 忽略規則
├── 📄 Dockerfile                     # Docker 建構文件
├── 📄 docker-compose.yml             # Docker Compose 配置
├── 📄 setup.sh                       # 快速設置腳本
│
├── 📂 docs/                          # 📚 文檔目錄
│   ├── API.md                        # API 使用文檔
│   ├── DEPLOYMENT.md                 # 部署指南
│   ├── DEVELOPMENT.md                # 開發指南
│   └── MIGRATION.md                  # 遷移指南
│
├── 📂 data/                          # 🗄️ 資料目錄
│   ├── raw/                          # 原始資料
│   │   └── regulations/              # PDF 法規文件（180+ 個文件）
│   ├── processed/                    # 處理後的資料
│   └── vector_store/                 # FAISS 向量資料庫
│
├── 📂 scripts/                       # 🔧 工具腳本
│   ├── build_vector_store.py         # 建立向量資料庫
│   ├── merge_pdfs.py                 # 合併 PDF 文件
│   ├── test_qa.py                    # 測試問答功能
│   └── migrate_from_old_project.py   # 從舊專案遷移
│
├── 📂 src/                           # 💻 源代碼
│   ├── __init__.py
│   ├── app.py                        # Flask 主應用入口
│   ├── config.py                     # 配置管理模組
│   │
│   ├── 📂 api/                       # 🌐 API 路由層
│   │   ├── __init__.py
│   │   └── chat.py                   # 聊天 API 端點
│   │
│   ├── 📂 services/                  # 🔨 業務邏輯層
│   │   ├── __init__.py
│   │   ├── qa_service.py             # 問答服務
│   │   └── document_service.py       # 文檔處理服務
│   │
│   └── 📂 utils/                     # 🛠️ 工具函數
│       ├── __init__.py
│       ├── logger.py                 # 日誌工具
│       └── validators.py             # 驗證工具
│
├── 📂 frontend/                      # 🎨 前端資源
│   ├── index.html                    # 主頁面
│   └── 📂 assets/                    # 靜態資源
│       ├── 📂 css/                   # 樣式文件
│       │   ├── main.css              # 主要樣式
│       │   └── mobile.css            # 手機響應式樣式
│       ├── 📂 js/                    # JavaScript
│       │   └── app.js                # 主應用腳本
│       └── 📂 images/                # 圖片資源
│           └── cycu_logo.png         # 中原大學 Logo
│
├── 📂 tests/                         # 🧪 測試目錄
│   ├── __init__.py
│   ├── test_api.py                   # API 端點測試
│   └── test_services.py              # 服務層測試
│
└── 📂 logs/                          # 📝 日誌目錄（運行時生成）
    └── app.log                       # 應用日誌
```

---

## 🏗️ 架構設計

### 三層架構

```
┌─────────────────────────────────────┐
│         前端層 (Frontend)            │
│  HTML + CSS + JavaScript            │
└─────────────────────────────────────┘
                 ↓ HTTP/JSON
┌─────────────────────────────────────┐
│         API 層 (API Routes)         │
│  Flask Blueprints + REST API        │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│      業務邏輯層 (Services)            │
│  QA Service + Document Service      │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│      資料層 (Data Layer)             │
│  FAISS Vector Store + OpenAI API    │
└─────────────────────────────────────┘
```

### 技術組件

1. **後端框架**: Flask
2. **AI 框架**: LangChain
3. **向量資料庫**: FAISS
4. **LLM 模型**: OpenAI GPT-4
5. **文檔處理**: PyPDF, LangChain Document Loaders
6. **前端**: 原生 HTML/CSS/JavaScript

---

## 📦 主要功能模組

### 1. 配置管理 (`src/config.py`)
- 環境變數管理
- 多環境配置（開發/生產/測試）
- 路徑管理
- 參數配置

### 2. API 層 (`src/api/`)
- **POST `/api/chat/ask`**: 發送問題獲取回答
- **POST `/api/chat/reset`**: 重置對話
- **GET `/api/chat/history`**: 獲取對話歷史
- **GET `/health`**: 健康檢查

### 3. 問答服務 (`src/services/qa_service.py`)
- 向量資料庫初始化和載入
- LLM 問答鏈建立
- 對話記憶管理
- 相似度檢索

### 4. 文檔服務 (`src/services/document_service.py`)
- PDF 文件載入
- 文檔切分
- 批量處理

### 5. 工具函數 (`src/utils/`)
- 日誌系統
- 輸入驗證
- 錯誤處理

---

## 🔧 工具腳本

### 1. `build_vector_store.py`
**用途**: 建立 FAISS 向量資料庫  
**使用**: `python scripts/build_vector_store.py`

### 2. `merge_pdfs.py`
**用途**: 合併多個 PDF 文件  
**使用**: `python scripts/merge_pdfs.py`

### 3. `test_qa.py`
**用途**: 測試問答功能  
**使用**: `python scripts/test_qa.py`

### 4. `migrate_from_old_project.py`
**用途**: 從舊專案遷移資料  
**使用**: `python scripts/migrate_from_old_project.py`

### 5. `setup.sh`
**用途**: 一鍵自動化設置  
**使用**: `./setup.sh`

---

## 📚 文檔系統

### 1. README.md
- 專案簡介
- 快速開始
- 安裝步驟
- 基本使用

### 2. docs/API.md
- API 端點詳細說明
- 請求/回應格式
- 錯誤處理
- 使用範例（JavaScript/Python）

### 3. docs/DEPLOYMENT.md
- 本地部署
- Docker 部署
- 生產環境部署
- Nginx 配置
- SSL 證書
- 監控與維護

### 4. docs/DEVELOPMENT.md
- 開發環境設置
- 專案結構說明
- 代碼規範
- 測試指南
- 調試技巧
- 貢獻指南

### 5. docs/MIGRATION.md
- 舊版與新版對比
- 遷移步驟
- 注意事項
- 疑難排解

---

## 🧪 測試框架

### 測試覆蓋

1. **API 測試** (`tests/test_api.py`)
   - 健康檢查
   - 問答端點
   - 錯誤處理
   - 邊界條件

2. **服務測試** (`tests/test_services.py`)
   - QA 服務
   - 文檔服務
   - 工具函數

### 測試執行

```bash
# 運行所有測試
pytest tests/

# 生成覆蓋率報告
pytest --cov=src --cov-report=html tests/
```

---

## 🐳 Docker 支援

### Dockerfile
- 基於 Python 3.10
- 多階段建構
- 最小化映像大小

### docker-compose.yml
- 服務配置
- 卷掛載
- 網路設置
- 健康檢查

### 使用方式

```bash
# 建立並啟動
docker-compose up -d

# 查看日誌
docker-compose logs -f

# 停止服務
docker-compose down
```

---

## 🎨 前端設計

### 功能特點

1. **響應式設計**: 支援手機/平板/桌面
2. **主題切換**: 深色/淺色模式
3. **語音輸入**: 支援 Web Speech API
4. **動態交互**: 載入動畫、訊息氣泡
5. **友善 UX**: 時間戳、滾動效果、錯誤提示

### 技術實現

- 原生 JavaScript（無框架依賴）
- CSS Grid/Flexbox 布局
- CSS Variables 主題系統
- 漸進式網頁應用 (PWA) 準備

---

## 🔐 安全考慮

1. **API Key 保護**: 使用環境變數
2. **輸入驗證**: 防止注入攻擊
3. **錯誤處理**: 不洩露敏感訊息
4. **CORS 配置**: 限制來源
5. **HTTPS**: 生產環境強制使用

---

## 📈 效能優化

1. **向量檢索**: FAISS 高效檢索
2. **文檔切分**: 優化 chunk 大小
3. **記憶體管理**: 適當的快取策略
4. **日誌分級**: 減少不必要的日誌

---

## 🚀 部署選項

### 選項 1: 本地開發
```bash
python src/app.py
```

### 選項 2: Gunicorn 生產
```bash
gunicorn -w 4 -b 0.0.0.0:8080 --chdir src app:app
```

### 選項 3: Docker 容器
```bash
docker-compose up -d
```

### 選項 4: 使用 Nginx 反向代理
```
Nginx (80/443) → Gunicorn (8080) → Flask App
```

---

## 📊 專案統計

- **總程式碼行數**: ~2,500+ 行
- **Python 模組**: 11 個
- **API 端點**: 4 個
- **測試文件**: 2 個
- **文檔頁面**: 5 個
- **工具腳本**: 5 個
- **支援 PDF**: 180+ 個

---

## 🎓 學習資源

### 專案用到的技術

1. **Flask**: https://flask.palletsprojects.com/
2. **LangChain**: https://python.langchain.com/
3. **FAISS**: https://faiss.ai/
4. **OpenAI**: https://platform.openai.com/docs/
5. **Docker**: https://docs.docker.com/

---

## 📝 待開發功能 (Future Roadmap)

### 短期計劃
- [ ] 添加用戶認證系統
- [ ] 實施 Redis 快取
- [ ] 添加對話記錄持久化
- [ ] 支援更多文件格式（Word, Excel）
- [ ] 添加管理後台

### 中期計劃
- [ ] 多輪對話優化
- [ ] 添加情感分析
- [ ] 支援多語言
- [ ] 實施 A/B 測試
- [ ] 添加分析儀表板

### 長期計劃
- [ ] 微服務架構
- [ ] Kubernetes 部署
- [ ] AI 模型微調
- [ ] 知識圖譜整合
- [ ] 移動應用開發

---

## 🤝 貢獻者

- **專案負責人**: [您的名字]
- **指導教授**: [教授名字]
- **開發團隊**: 中原大學資訊工程學系

---

## 📞 聯絡方式

- **Email**: your.email@example.com
- **GitHub**: https://github.com/yourusername/CYCU-ChatBot
- **網站**: https://your-website.com

---

## 📄 授權

本專案採用 MIT 授權條款。

---

## 🙏 致謝

- 感謝中原大學提供資料支援
- 感謝 OpenAI 提供 GPT API
- 感謝開源社群的各項工具和框架

---

<div align="center">

**CYCU ChatBot v2.0**  
*為中原大學打造的智能問答系統*

Made with ❤️ in Taiwan

</div>
