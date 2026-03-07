#!/usr/bin/env python3
"""
Build Vector Store Script
建立向量資料庫腳本

此腳本將載入所有 PDF 文件並建立 FAISS 向量資料庫
使用方法: python scripts/build_vector_store.py
"""
import sys
import os
from pathlib import Path

# 添加 src 目錄到 Python 路徑
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from config import get_config
from services.document_service import DocumentService
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from utils.logger import setup_logger


def main():
    """主函數"""
    # 獲取配置
    config = get_config()
    
    # 設置日誌
    logger = setup_logger(
        'build_vector_store',
        config.LOG_DIR / 'build_vector_store.log',
        config.LOG_LEVEL
    )
    
    logger.info("=" * 60)
    logger.info("開始建立向量資料庫")
    logger.info("=" * 60)
    
    try:
        # 檢查 PDF 資料目錄
        pdf_data_path = config.PDF_DATA_PATH
        logger.info(f"PDF 資料目錄: {pdf_data_path}")
        
        if not pdf_data_path.exists():
            logger.error(f"PDF 資料目錄不存在: {pdf_data_path}")
            logger.info(f"請將 PDF 文件放置在: {pdf_data_path}")
            return 1
        
        # 檢查是否有 PDF 文件
        pdf_files = list(pdf_data_path.rglob("*.pdf"))
        if not pdf_files:
            logger.error(f"在 {pdf_data_path} 中找不到任何 PDF 文件")
            return 1
        
        logger.info(f"找到 {len(pdf_files)} 個 PDF 文件")
        
        # 初始化文檔服務
        logger.info("初始化文檔服務...")
        doc_service = DocumentService()
        
        # 處理文檔
        logger.info("開始載入和處理文檔...")
        documents = doc_service.process_documents(str(pdf_data_path))
        
        if not documents:
            logger.error("未能載入任何文檔")
            return 1
        
        logger.info(f"成功處理 {len(documents)} 個文檔片段")
        
        # 初始化 embeddings
        logger.info("初始化 OpenAI Embeddings...")
        embeddings = OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY)
        
        # 建立向量資料庫
        logger.info("建立 FAISS 向量資料庫（這可能需要幾分鐘）...")
        vector_store = FAISS.from_documents(documents, embeddings)
        
        # 儲存向量資料庫
        vector_store_path = str(config.VECTOR_STORE_PATH)
        logger.info(f"儲存向量資料庫到: {vector_store_path}")
        vector_store.save_local(vector_store_path)
        
        logger.info("=" * 60)
        logger.info("向量資料庫建立完成！")
        logger.info("=" * 60)
        logger.info(f"向量資料庫位置: {vector_store_path}")
        logger.info(f"文檔數量: {len(documents)}")
        logger.info("")
        logger.info("您現在可以啟動應用程式:")
        logger.info("  python src/app.py")
        
        return 0
        
    except Exception as e:
        logger.error(f"建立向量資料庫時發生錯誤: {str(e)}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
