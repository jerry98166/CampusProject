"""
CYCU ChatBot Configuration Module
應用程式配置管理
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 專案根目錄
BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    """基礎配置類"""
    
    # Flask 配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    FLASK_PORT = int(os.getenv('FLASK_PORT', 8080))
    
    # OpenAI 配置
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4')
    
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY 未設定。請在 .env 文件中設定此環境變數")
    
    # 路徑配置
    DATA_DIR = BASE_DIR / 'data'
    PDF_DATA_PATH = BASE_DIR / os.getenv('PDF_DATA_PATH', 'data/raw/regulations')
    VECTOR_STORE_PATH = BASE_DIR / os.getenv('VECTOR_STORE_PATH', 'data/vector_store')
    PROCESSED_DATA_PATH = BASE_DIR / os.getenv('PROCESSED_DATA_PATH', 'data/processed')
    LOG_DIR = BASE_DIR / 'logs'
    
    # 確保目錄存在
    PDF_DATA_PATH.mkdir(parents=True, exist_ok=True)
    VECTOR_STORE_PATH.mkdir(parents=True, exist_ok=True)
    PROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    # Ngrok 配置（開發用）
    USE_NGROK = os.getenv('USE_NGROK', 'false').lower() == 'true'
    NGROK_AUTH_TOKEN = os.getenv('NGROK_AUTH_TOKEN')
    
    # LangChain 配置
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 1000))
    CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 200))
    SIMILARITY_SEARCH_K = int(os.getenv('SIMILARITY_SEARCH_K', 4))
    
    # 日誌配置
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = LOG_DIR / os.getenv('LOG_FILE', 'app.log')
    
    # CORS 配置
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')
    
    # 快取配置
    CACHE_ENABLED = os.getenv('CACHE_ENABLED', 'false').lower() == 'true'
    CACHE_TYPE = os.getenv('CACHE_TYPE', 'simple')
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', 300))
    
    # 速率限制
    RATE_LIMIT_ENABLED = os.getenv('RATE_LIMIT_ENABLED', 'false').lower() == 'true'
    RATE_LIMIT_PER_MINUTE = int(os.getenv('RATE_LIMIT_PER_MINUTE', 20))


class DevelopmentConfig(Config):
    """開發環境配置"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """生產環境配置"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """測試環境配置"""
    DEBUG = True
    TESTING = True
    VECTOR_STORE_PATH = BASE_DIR / 'data/test_vector_store'


# 根據 FLASK_ENV 選擇配置
config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

def get_config():
    """獲取當前環境的配置"""
    env = os.getenv('FLASK_ENV', 'development')
    return config_dict.get(env, DevelopmentConfig)
