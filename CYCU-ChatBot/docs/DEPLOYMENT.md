# 部署指南

本指南說明如何在不同環境中部署 CYCU ChatBot。

---

## 目錄

- [環境需求](#環境需求)
- [本地部署](#本地部署)
- [Docker 部署](#docker-部署)
- [生產環境部署](#生產環境部署)
- [Nginx 配置](#nginx-配置)
- [SSL 證書](#ssl-證書)
- [監控與維護](#監控與維護)

---

## 環境需求

### 硬體需求

- **CPU**: 2 核心或以上
- **記憶體**: 4GB RAM（建議 8GB）
- **硬碟**: 10GB 可用空間（含向量資料庫）

### 軟體需求

- Python 3.8 或以上
- pip 套件管理器
- (可選) Docker 和 Docker Compose
- (可選) Nginx 反向代理

---

## 本地部署

### 1. 克隆專案

```bash
git clone https://github.com/yourusername/CYCU-ChatBot.git
cd CYCU-ChatBot
```

### 2. 建立虛擬環境

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate     # Windows
```

### 3. 安裝依賴

```bash
pip install -r requirements.txt
```

### 4. 配置環境變數

```bash
cp .env.example .env
```

編輯 `.env` 文件，填入您的配置：

```env
OPENAI_API_KEY=sk-your-api-key-here
FLASK_ENV=development
FLASK_HOST=0.0.0.0
FLASK_PORT=8080
```

### 5. 準備資料

將 PDF 文件放置到 `data/raw/regulations/` 目錄：

```bash
mkdir -p data/raw/regulations
# 複製 PDF 文件到此目錄
```

### 6. 建立向量資料庫

```bash
python scripts/build_vector_store.py
```

這個過程可能需要數分鐘，取決於文件數量。

### 7. 啟動應用

```bash
python src/app.py
```

應用將在 http://localhost:8080 上運行。

---

## Docker 部署

### 1. 準備環境

確保已安裝 Docker 和 Docker Compose。

### 2. 配置環境變數

```bash
cp .env.example .env
```

編輯 `.env` 文件。

### 3. 建立向量資料庫

在首次啟動前，需要先建立向量資料庫：

```bash
# 方法 1: 在本地建立（推薦）
python scripts/build_vector_store.py

# 方法 2: 在 Docker 容器中建立
docker-compose run --rm cycu-chatbot python scripts/build_vector_store.py
```

### 4. 啟動容器

```bash
docker-compose up -d
```

### 5. 查看日誌

```bash
docker-compose logs -f
```

### 6. 停止服務

```bash
docker-compose down
```

---

## 生產環境部署

### 使用 Gunicorn

生產環境建議使用 Gunicorn 作為 WSGI 伺服器。

#### 1. 安裝 Gunicorn

```bash
pip install gunicorn
```

#### 2. 啟動應用

```bash
gunicorn -w 4 -b 0.0.0.0:8080 --chdir src app:app
```

參數說明：
- `-w 4`: 4 個 worker 進程
- `-b 0.0.0.0:8080`: 綁定地址和端口
- `--chdir src`: 切換到 src 目錄
- `app:app`: 模組名稱:應用實例

#### 3. 使用系統服務

建立 systemd 服務文件 `/etc/systemd/system/cycu-chatbot.service`:

```ini
[Unit]
Description=CYCU ChatBot Service
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/path/to/CYCU-ChatBot
Environment="PATH=/path/to/CYCU-ChatBot/venv/bin"
ExecStart=/path/to/CYCU-ChatBot/venv/bin/gunicorn \
    -w 4 \
    -b 127.0.0.1:8080 \
    --chdir /path/to/CYCU-ChatBot/src \
    app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

啟動服務：

```bash
sudo systemctl daemon-reload
sudo systemctl start cycu-chatbot
sudo systemctl enable cycu-chatbot
sudo systemctl status cycu-chatbot
```

---

## Nginx 配置

### 反向代理配置

建立 Nginx 配置文件 `/etc/nginx/sites-available/cycu-chatbot`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 靜態文件
    location /assets/ {
        alias /path/to/CYCU-ChatBot/frontend/assets/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # API 端點
    location /api/ {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 超時設置（問答可能需要較長時間）
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # 其他請求
    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 健康檢查
    location /health {
        proxy_pass http://127.0.0.1:8080;
        access_log off;
    }

    # 日誌
    access_log /var/log/nginx/cycu-chatbot-access.log;
    error_log /var/log/nginx/cycu-chatbot-error.log;
}
```

啟用配置：

```bash
sudo ln -s /etc/nginx/sites-available/cycu-chatbot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## SSL 證書

### 使用 Let's Encrypt

```bash
# 安裝 Certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# 獲取證書
sudo certbot --nginx -d your-domain.com

# 自動續期
sudo certbot renew --dry-run
```

Certbot 會自動修改 Nginx 配置文件，添加 SSL 配置。

---

## 監控與維護

### 日誌管理

**應用日誌**:
- 位置: `logs/app.log`
- 查看: `tail -f logs/app.log`

**Nginx 日誌**:
- 訪問日誌: `/var/log/nginx/cycu-chatbot-access.log`
- 錯誤日誌: `/var/log/nginx/cycu-chatbot-error.log`

**Docker 日誌**:
```bash
docker-compose logs -f
```

### 備份

定期備份以下內容：

1. **向量資料庫**:
```bash
tar -czf vector_store_backup_$(date +%Y%m%d).tar.gz data/vector_store/
```

2. **配置文件**:
```bash
cp .env .env.backup
```

3. **PDF 資料** (如果有更新):
```bash
tar -czf pdf_data_backup_$(date +%Y%m%d).tar.gz data/raw/
```

### 效能監控

使用 `htop` 或其他工具監控：
- CPU 使用率
- 記憶體使用率
- 磁碟 I/O

### 健康檢查

設置定期健康檢查：

```bash
#!/bin/bash
# health_check.sh

HEALTH_URL="http://localhost:8080/health"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $HEALTH_URL)

if [ $RESPONSE -eq 200 ]; then
    echo "Service is healthy"
    exit 0
else
    echo "Service is unhealthy (HTTP $RESPONSE)"
    exit 1
fi
```

添加到 crontab：
```bash
*/5 * * * * /path/to/health_check.sh
```

---

## 疑難排解

### 問題：無法連接到 OpenAI API

**解決方案**:
1. 檢查 API Key 是否正確
2. 檢查網路連接
3. 檢查防火牆設置

### 問題：向量資料庫載入失敗

**解決方案**:
1. 確認向量資料庫文件存在
2. 重新建立向量資料庫：`python scripts/build_vector_store.py`

### 問題：記憶體不足

**解決方案**:
1. 增加系統記憶體
2. 減少 Gunicorn worker 數量
3. 優化向量資料庫大小

---

## 安全建議

1. **API Key 保護**: 永遠不要將 API Key 提交到版本控制
2. **防火牆**: 只開放必要的端口（80, 443）
3. **定期更新**: 保持依賴套件更新
4. **HTTPS**: 生產環境必須使用 HTTPS
5. **訊問記錄**: 適當記錄用戶查詢（遵守隱私政策）

---

## 擴展性考慮

當用戶量增加時：

1. **水平擴展**: 運行多個應用實例
2. **負載均衡**: 使用 Nginx 或專業負載均衡器
3. **快取**: 實施 Redis 快取常見問題
4. **資料庫**: 考慮將對話歷史存儲到資料庫

---

## 更新流程

```bash
# 1. 備份
tar -czf backup_$(date +%Y%m%d).tar.gz data/ logs/

# 2. 拉取最新代碼
git pull origin main

# 3. 更新依賴
pip install -r requirements.txt

# 4. 重啟服務
sudo systemctl restart cycu-chatbot
```

---

如有問題，請參考專案 README 或聯絡技術支援團隊。
