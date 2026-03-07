"""
Chat API Module
聊天相關的 API 端點
"""
from flask import Blueprint, request, jsonify
from services.qa_service import QAService
from utils.logger import get_logger
from utils.validators import validate_question

# 建立藍圖
chat_bp = Blueprint('chat', __name__)

# 獲取日誌記錄器
logger = get_logger(__name__)

# 初始化問答服務
qa_service = QAService()


@chat_bp.route('/ask', methods=['POST'])
def ask_question():
    """
    處理用戶問題並返回答案
    
    Request Body:
        {
            "question": "用戶的問題"
        }
    
    Response:
        {
            "response": "AI的回答",
            "status": "success"
        }
    """
    try:
        # 獲取請求數據
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': '請求格式錯誤',
                'status': 'error'
            }), 400
        
        question = data.get('question', '').strip()
        
        # 驗證問題
        is_valid, error_message = validate_question(question)
        if not is_valid:
            return jsonify({
                'error': error_message,
                'status': 'error'
            }), 400
        
        logger.info(f"收到問題: {question}")
        
        # 獲取答案
        answer = qa_service.get_answer(question)
        
        logger.info(f"回答已生成")
        
        return jsonify({
            'response': answer,
            'status': 'success'
        }), 200
        
    except Exception as e:
        logger.error(f"處理問題時發生錯誤: {str(e)}", exc_info=True)
        return jsonify({
            'error': '處理問題時發生錯誤，請稍後再試',
            'status': 'error'
        }), 500


@chat_bp.route('/reset', methods=['POST'])
def reset_conversation():
    """
    重置對話上下文
    
    Response:
        {
            "message": "對話已重置",
            "status": "success"
        }
    """
    try:
        qa_service.reset_memory()
        logger.info("對話上下文已重置")
        
        return jsonify({
            'message': '對話已重置',
            'status': 'success'
        }), 200
        
    except Exception as e:
        logger.error(f"重置對話時發生錯誤: {str(e)}", exc_info=True)
        return jsonify({
            'error': '重置對話失敗',
            'status': 'error'
        }), 500


@chat_bp.route('/history', methods=['GET'])
def get_chat_history():
    """
    獲取對話歷史
    
    Response:
        {
            "history": [...],
            "status": "success"
        }
    """
    try:
        history = qa_service.get_chat_history()
        
        return jsonify({
            'history': history,
            'status': 'success'
        }), 200
        
    except Exception as e:
        logger.error(f"獲取對話歷史時發生錯誤: {str(e)}", exc_info=True)
        return jsonify({
            'error': '獲取對話歷史失敗',
            'status': 'error'
        }), 500
