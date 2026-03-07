"""
Document Service Module
文檔處理服務
"""
import os
from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from config import get_config
from utils.logger import get_logger

logger = get_logger(__name__)
config = get_config()


class DocumentService:
    """文檔處理服務類"""
    
    def __init__(self):
        """初始化文檔服務"""
        self.config = config
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            length_function=len,
        )
    
    def load_pdf(self, pdf_path: str) -> List[Document]:
        """
        載入單個 PDF 文件
        
        Args:
            pdf_path: PDF 文件路徑
            
        Returns:
            文檔列表
        """
        try:
            logger.info(f"正在載入 PDF: {pdf_path}")
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            logger.info(f"成功載入 {len(documents)} 頁")
            return documents
        except Exception as e:
            logger.error(f"載入 PDF 失敗 {pdf_path}: {str(e)}")
            return []
    
    def load_pdf_directory(self, directory: str) -> List[Document]:
        """
        載入目錄下的所有 PDF 文件
        
        Args:
            directory: 目錄路徑
            
        Returns:
            所有文檔的列表
        """
        all_documents = []
        pdf_dir = Path(directory)
        
        if not pdf_dir.exists():
            logger.warning(f"目錄不存在: {directory}")
            return all_documents
        
        # 遞迴搜尋所有 PDF 文件
        pdf_files = list(pdf_dir.rglob("*.pdf"))
        logger.info(f"找到 {len(pdf_files)} 個 PDF 文件")
        
        for pdf_file in pdf_files:
            documents = self.load_pdf(str(pdf_file))
            if documents:
                all_documents.extend(documents)
        
        logger.info(f"總共載入 {len(all_documents)} 個文檔片段")
        return all_documents
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        切分文檔為較小的片段
        
        Args:
            documents: 原始文檔列表
            
        Returns:
            切分後的文檔片段
        """
        try:
            logger.info(f"正在切分 {len(documents)} 個文檔...")
            split_docs = self.text_splitter.split_documents(documents)
            logger.info(f"切分完成，得到 {len(split_docs)} 個片段")
            return split_docs
        except Exception as e:
            logger.error(f"切分文檔時發生錯誤: {str(e)}")
            return documents
    
    def process_documents(self, directory: str) -> List[Document]:
        """
        處理目錄下的所有文檔（載入並切分）
        
        Args:
            directory: 文檔目錄
            
        Returns:
            處理後的文檔片段列表
        """
        # 載入所有 PDF
        documents = self.load_pdf_directory(directory)
        
        if not documents:
            raise ValueError(f"未能從 {directory} 載入任何文檔")
        
        # 切分文檔
        split_docs = self.split_documents(documents)
        
        return split_docs
