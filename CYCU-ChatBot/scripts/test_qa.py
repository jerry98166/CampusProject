#!/usr/bin/env python3
"""
Test QA Script
測試問答功能腳本

此腳本用於測試問答系統是否正常運作
使用方法: python scripts/test_qa.py
"""
import sys
from pathlib import Path

# 添加 src 目錄到 Python 路徑
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from config import get_config
from services.qa_service import QAService
from utils.logger import setup_logger


def test_questions():
    """測試問題列表"""
    return [
        "中原大學的學則是什麼？",
        "如何申請獎學金？",
        "學生請假的規定是什麼？",
        "轉系的辦法是什麼？",
        "學生申訴的流程是什麼？"
    ]


def main():
    """主函數"""
    # 獲取配置
    config = get_config()
    
    # 設置日誌
    logger = setup_logger(
        'test_qa',
        config.LOG_DIR / 'test_qa.log',
        config.LOG_LEVEL
    )
    
    print("=" * 70)
    print("CYCU ChatBot - 問答系統測試")
    print("=" * 70)
    print()
    
    try:
        # 初始化問答服務
        print("正在初始化問答服務...")
        qa_service = QAService()
        print("✓ 問答服務初始化成功")
        print()
        
        # 獲取測試問題
        questions = test_questions()
        
        print(f"準備測試 {len(questions)} 個問題")
        print("=" * 70)
        print()
        
        # 逐個測試問題
        for i, question in enumerate(questions, 1):
            print(f"[問題 {i}/{len(questions)}]")
            print(f"Q: {question}")
            print()
            
            try:
                # 獲取答案
                answer = qa_service.get_answer(question)
                print(f"A: {answer}")
                
            except Exception as e:
                logger.error(f"處理問題時發生錯誤: {e}", exc_info=True)
                print(f"✗ 錯誤: {e}")
            
            print()
            print("-" * 70)
            print()
        
        print("=" * 70)
        print("測試完成！")
        print("=" * 70)
        
        # 互動模式
        print()
        print("進入互動模式（輸入 'quit' 或 'exit' 結束）")
        print("=" * 70)
        print()
        
        while True:
            try:
                question = input("請輸入問題: ").strip()
                
                if question.lower() in ['quit', 'exit', '退出']:
                    print("再見！")
                    break
                
                if not question:
                    continue
                
                print()
                answer = qa_service.get_answer(question)
                print(f"回答: {answer}")
                print()
                print("-" * 70)
                print()
                
            except KeyboardInterrupt:
                print("\n\n再見！")
                break
            except Exception as e:
                logger.error(f"錯誤: {e}", exc_info=True)
                print(f"發生錯誤: {e}")
        
        return 0
        
    except Exception as e:
        logger.error(f"測試過程中發生錯誤: {e}", exc_info=True)
        print(f"\n✗ 錯誤: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
