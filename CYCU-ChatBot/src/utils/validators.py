"""
Validators Utility Module
驗證工具模組
"""
from typing import Tuple


def validate_question(question: str) -> Tuple[bool, str]:
    """
    驗證用戶問題的有效性
    
    Args:
        question: 用戶輸入的問題
        
    Returns:
        (是否有效, 錯誤訊息)
    """
    # 檢查是否為空
    if not question:
        return False, "問題不能為空"
    
    # 檢查長度
    if len(question) < 2:
        return False, "問題太短，請輸入至少2個字元"
    
    if len(question) > 1000:
        return False, "問題太長，請限制在1000個字元以內"
    
    # 檢查是否只包含空白字元
    if question.isspace():
        return False, "問題不能只包含空白字元"
    
    return True, ""


def validate_api_key(api_key: str) -> bool:
    """
    驗證 API 密鑰格式
    
    Args:
        api_key: API 密鑰
        
    Returns:
        是否有效
    """
    if not api_key:
        return False
    
    # OpenAI API Key 通常以 sk- 開頭
    if not api_key.startswith('sk-'):
        return False
    
    # 長度檢查（OpenAI API Key 通常較長）
    if len(api_key) < 20:
        return False
    
    return True


def sanitize_input(text: str) -> str:
    """
    清理用戶輸入
    
    Args:
        text: 原始文本
        
    Returns:
        清理後的文本
    """
    # 移除前後空白
    text = text.strip()
    
    # 替換多個連續空白為單個空白
    import re
    text = re.sub(r'\s+', ' ', text)
    
    return text
