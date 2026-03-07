"""
CYCU ChatBot Main Application
Flask 應用程式主入口
"""
import os
from flask import Flask, send_from_directory
from flask_cors import CORS

from config import get_config
from api.chat import chat_bp
from utils.logger import setup_logger

# 取得配置
config = get_config()

# 初始化 Flask 應用
app = Flask(__name__, 
            static_folder='../frontend',
            static_url_path='')
app.config.from_object(config)

# 設定 CORS
CORS(app, resources={r"/api/*": {"origins": config.CORS_ORIGINS}})

# 設定日誌
logger = setup_logger(__name__, config.LOG_FILE, config.LOG_LEVEL)

# 註冊藍圖
app.register_blueprint(chat_bp, url_prefix='/api/chat')


@app.route('/')
def index():
    """提供前端首頁"""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/health')
def health_check():
    """健康檢查端點"""
    return {
        'status': 'healthy',
        'service': 'CYCU ChatBot',
        'version': '2.0.0'
    }, 200


@app.errorhandler(404)
def not_found(error):
    """404 錯誤處理"""
    return {'error': '找不到請求的資源'}, 404


@app.errorhandler(500)
def internal_error(error):
    """500 錯誤處理"""
    logger.error(f"Internal server error: {error}")
    return {'error': '伺服器內部錯誤'}, 500


def main():
    """主函數"""
    logger.info(f"Starting CYCU ChatBot on {config.FLASK_HOST}:{config.FLASK_PORT}")
    logger.info(f"Environment: {os.getenv('FLASK_ENV', 'development')}")
    
    # 如果啟用 Ngrok（開發環境）
    if config.USE_NGROK and config.NGROK_AUTH_TOKEN:
        try:
            from pyngrok import conf, ngrok
            conf.get_default().auth_token = config.NGROK_AUTH_TOKEN
            public_url = ngrok.connect(config.FLASK_PORT)
            logger.info(f"Ngrok tunnel: {public_url} -> http://127.0.0.1:{config.FLASK_PORT}")
        except Exception as e:
            logger.warning(f"Failed to start Ngrok: {e}")
    
    # 啟動應用
    app.run(
        host=config.FLASK_HOST,
        port=config.FLASK_PORT,
        debug=config.DEBUG
    )


if __name__ == '__main__':
    main()
