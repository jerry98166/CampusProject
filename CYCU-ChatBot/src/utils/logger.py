"""
Logger Utility Module
日誌工具模組
"""
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler


def setup_logger(name: str, log_file: Path, level: str = 'INFO'):
    """
    設定日誌記錄器
    
    Args:
        name: 日誌記錄器名稱
        log_file: 日誌文件路徑
        level: 日誌級別
        
    Returns:
        配置好的日誌記錄器
    """
    # 建立日誌記錄器
    logger = logging.getLogger(name)
    
    # 防止重複添加處理器
    if logger.handlers:
        return logger
    
    # 設定日誌級別
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # 日誌格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 控制台處理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件處理器（滾動日誌）
    try:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"無法建立日誌文件 {log_file}: {e}")
    
    return logger


def get_logger(name: str):
    """
    獲取日誌記錄器
    
    Args:
        name: 日誌記錄器名稱
        
    Returns:
        日誌記錄器
    """
    return logging.getLogger(name)
