# 開發指南

本指南面向希望為 CYCU ChatBot 做出貢獻或進行本地開發的開發者。

---

## 目錄

- [開發環境設置](#開發環境設置)
- [專案結構](#專案結構)
- [開發工作流程](#開發工作流程)
- [代碼規範](#代碼規範)
- [測試](#測試)
- [調試](#調試)
- [貢獻指南](#貢獻指南)

---

## 開發環境設置

### 前置需求

- Python 3.8+
- pip
- Git
- VS Code 或其他 IDE（推薦）

### 初始設置

1. **克隆專案**
```bash
git clone https://github.com/yourusername/CYCU-ChatBot.git
cd CYCU-ChatBot
```

2. **建立虛擬環境**
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
```

3. **安裝開發依賴**
```bash
pip install -r requirements.txt
```

4. **配置環境變數**
```bash
cp .env.example .env
# 編輯 .env 填入開發用的配置
```

5. **安裝 pre-commit hooks**（可選）
```bash
pip install pre-commit
pre-commit install
```

---

## 專案結構

```
CYCU-ChatBot/
├── README.md                  # 專案說明
├── requirements.txt           # Python 依賴
├── .env.example              # 環境變數範例
├── .gitignore                # Git 忽略規則
├── Dockerfile                # Docker 建構文件
├── docker-compose.yml        # Docker Compose 配置
│
├── docs/                     # 📚 文檔
│   ├── API.md               # API 文檔
│   ├── DEPLOYMENT.md        # 部署指南
│   └── DEVELOPMENT.md       # 開發指南（本文件）
│
├── data/                     # 🗄️ 資料目錄
│   ├── raw/                 # 原始 PDF 文件
│   │   └── regulations/     # 法規文件
│   ├── processed/           # 處理後的資料
│   └── vector_store/        # 向量資料庫
│
├── scripts/                  # 🔧 工具腳本
│   ├── build_vector_store.py  # 建立向量資料庫
│   ├── merge_pdfs.py          # 合併 PDF
│   └── test_qa.py             # 測試問答
│
├── src/                      # 💻 源代碼
│   ├── __init__.py
│   ├── app.py               # Flask 主應用
│   ├── config.py            # 配置管理
│   │
│   ├── api/                 # 🌐 API 路由層
│   │   ├── __init__.py
│   │   └── chat.py          # 聊天 API
│   │
│   ├── services/            # 🔨 業務邏輯層
│   │   ├── __init__.py
│   │   ├── qa_service.py         # 問答服務
│   │   └── document_service.py   # 文檔服務
│   │
│   └── utils/               # 🛠️ 工具函數
│       ├── __init__.py
│       ├── logger.py        # 日誌工具
│       └── validators.py    # 驗證工具
│
├── frontend/                 # 🎨 前端
│   ├── index.html
│   └── assets/
│       ├── css/             # 樣式文件
│       ├── js/              # JavaScript
│       └── images/          # 圖片資源
│
└── tests/                    # 🧪 測試
    ├── __init__.py
    ├── test_api.py          # API 測試
    └── test_services.py     # 服務測試
```

### 關鍵組件說明

#### `src/app.py`
Flask 應用主入口，負責：
- 應用初始化
- 藍圖註冊
- 錯誤處理
- 靜態文件服務

#### `src/config.py`
配置管理模組，包含：
- 環境變數讀取
- 配置類定義
- 路徑設置

#### `src/api/chat.py`
聊天 API 端點，處理：
- 問答請求
- 對話重置
- 歷史記錄

#### `src/services/qa_service.py`
問答服務核心，負責：
- 向量資料庫載入
- LLM 問答鏈建立
- 對話記憶管理

#### `src/services/document_service.py`
文檔處理服務，負責：
- PDF 載入
- 文檔切分
- 批量處理

---

## 開發工作流程

### 1. 建立功能分支

```bash
git checkout -b feature/your-feature-name
```

### 2. 開發新功能

遵循以下原則：
- 保持代碼簡潔
- 添加適當的註釋
- 遵循 PEP 8 規範
- 編寫單元測試

### 3. 本地測試

```bash
# 運行測試
pytest tests/

# 運行特定測試
pytest tests/test_api.py::test_ask_question_success

# 生成覆蓋率報告
pytest --cov=src tests/
```

### 4. 代碼格式化

```bash
# 使用 black 格式化
black src/ tests/

# 使用 flake8 檢查
flake8 src/ tests/

# 使用 pylint 檢查
pylint src/
```

### 5. 提交變更

```bash
git add .
git commit -m "feat: add new feature description"
```

提交訊息格式：
- `feat:` 新功能
- `fix:` 錯誤修復
- `docs:` 文檔更新
- `style:` 代碼格式調整
- `refactor:` 代碼重構
- `test:` 測試相關
- `chore:` 其他雜項

### 6. 推送並建立 Pull Request

```bash
git push origin feature/your-feature-name
```

然後在 GitHub 上建立 Pull Request。

---

## 代碼規範

### Python 代碼規範

遵循 [PEP 8](https://peps.python.org/pep-0008/) 規範：

- **縮排**: 使用 4 個空格
- **行寬**: 最大 100 字元
- **命名**:
  - 類名: `PascalCase`
  - 函數/變數: `snake_case`
  - 常量: `UPPER_CASE`
  - 私有成員: `_leading_underscore`

### 文檔字串

使用 Google 風格的 docstring：

```python
def function_name(param1: str, param2: int) -> bool:
    """
    簡短的一行描述。
    
    詳細的多行描述（如果需要）。
    
    Args:
        param1: 參數1的說明
        param2: 參數2的說明
        
    Returns:
        返回值說明
        
    Raises:
        ValueError: 錯誤情況說明
    """
    pass
```

### 類型提示

使用 Python 類型提示：

```python
from typing import List, Dict, Optional

def process_data(items: List[str]) -> Dict[str, int]:
    """處理資料"""
    pass
```

### 錯誤處理

適當的錯誤處理：

```python
try:
    result = risky_operation()
except SpecificException as e:
    logger.error(f"Operation failed: {e}")
    # 處理錯誤
else:
    # 成功後的處理
finally:
    # 清理資源
```

---

## 測試

### 單元測試

使用 pytest 進行測試：

```python
# tests/test_example.py
import pytest
from src.services.qa_service import QAService

def test_qa_service_initialization():
    """測試 QA 服務初始化"""
    service = QAService()
    assert service is not None

def test_answer_generation():
    """測試答案生成"""
    service = QAService()
    answer = service.get_answer("測試問題")
    assert isinstance(answer, str)
    assert len(answer) > 0
```

### 執行測試

```bash
# 運行所有測試
pytest

# 運行並顯示詳細資訊
pytest -v

# 運行並生成覆蓋率報告
pytest --cov=src --cov-report=html

# 運行特定文件
pytest tests/test_api.py

# 運行特定測試
pytest tests/test_api.py::test_health_check
```

### Mock 和 Fixture

使用 fixture 和 mock：

```python
import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def mock_openai():
    """模擬 OpenAI API"""
    with patch('openai.ChatCompletion.create') as mock:
        mock.return_value = {'choices': [{'text': 'Mock response'}]}
        yield mock

def test_with_mock(mock_openai):
    """使用 mock 進行測試"""
    # 測試代碼
    pass
```

---

## 調試

### 日誌調試

使用日誌進行調試：

```python
from utils.logger import get_logger

logger = get_logger(__name__)

def debug_function():
    logger.debug("Debug information")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
```

### 使用 pdb

```python
import pdb

def problematic_function():
    x = 10
    pdb.set_trace()  # 設置斷點
    y = x * 2
    return y
```

### VS Code 調試

在 `.vscode/launch.json` 中配置：

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Flask",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "src/app.py",
                "FLASK_ENV": "development"
            },
            "args": [
                "run",
                "--no-debugger",
                "--no-reload"
            ],
            "jinja": true
        }
    ]
}
```

---

## 常見開發任務

### 添加新的 API 端點

1. 在 `src/api/chat.py` 或新建藍圖文件中定義路由
2. 在 `src/services/` 中實現業務邏輯
3. 在 `tests/test_api.py` 中添加測試
4. 更新 `docs/API.md` 文檔

### 修改向量資料庫配置

1. 修改 `src/config.py` 中的相關配置
2. 修改 `src/services/document_service.py` 中的處理邏輯
3. 重新建立向量資料庫：`python scripts/build_vector_store.py`

### 添加新的工具函數

1. 在 `src/utils/` 目錄下創建或修改文件
2. 添加適當的類型提示和文檔字串
3. 在 `tests/` 中添加測試

---

## 效能優化

### 快取策略

可以為常見問題添加快取：

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_function(param):
    """帶快取的函數"""
    pass
```

### 非同步處理

對於耗時操作，考慮使用非同步：

```python
import asyncio

async def async_operation():
    """非同步操作"""
    await asyncio.sleep(1)
    return "result"
```

---

## 貢獻指南

### Pull Request 流程

1. Fork 專案
2. 建立功能分支
3. 開發並測試
4. 確保代碼通過所有測試
5. 更新相關文檔
6. 提交 Pull Request
7. 等待 Code Review

### Code Review 檢查清單

- [ ] 代碼符合規範
- [ ] 有適當的測試覆蓋
- [ ] 文檔已更新
- [ ] 沒有引入新的警告
- [ ] 所有測試通過
- [ ] 沒有明顯的效能問題

---

## 資源

### 相關技術文檔

- [Flask 文檔](https://flask.palletsprojects.com/)
- [LangChain 文檔](https://python.langchain.com/)
- [FAISS 文檔](https://faiss.ai/)
- [OpenAI API 文檔](https://platform.openai.com/docs/)

### 推薦閱讀

- Python 最佳實踐
- RAG 系統設計模式
- 向量資料庫優化技巧
- Flask 應用部署指南

---

## 疑難排解

### 常見問題

**Q: 向量資料庫載入很慢**
A: 考慮使用 GPU 版本的 FAISS，或優化文檔切分大小

**Q: 記憶體使用過高**
A: 調整 chunk_size 和 batch_size 參數

**Q: API 回應時間長**
A: 考慮實施快取、使用更快的模型、或優化檢索參數

---

## 聯絡方式

- GitHub Issues: [專案 Issues](https://github.com/yourusername/CYCU-ChatBot/issues)
- Email: dev@example.com

---

感謝您為 CYCU ChatBot 做出貢獻！🎉
