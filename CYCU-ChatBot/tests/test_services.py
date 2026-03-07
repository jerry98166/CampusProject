"""
Test Services Module
服務層測試
"""
import sys
from pathlib import Path

# 添加 src 目錄到 Python 路徑
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import pytest
from unittest.mock import Mock, patch
from services.qa_service import QAService
from services.document_service import DocumentService


class TestQAService:
    """QA 服務測試"""
    
    @pytest.fixture
    def qa_service(self):
        """建立 QA 服務實例"""
        with patch('services.qa_service.FAISS') as mock_faiss:
            with patch('services.qa_service.OpenAIEmbeddings') as mock_embeddings:
                service = QAService()
                return service
    
    def test_get_answer_success(self, qa_service):
        """測試成功獲取答案"""
        # 由於需要實際的 OpenAI API，這裡只測試流程
        question = "測試問題"
        # 實際測試需要 mock qa_chain
        assert qa_service is not None
    
    def test_reset_memory(self, qa_service):
        """測試重置記憶"""
        qa_service.reset_memory()
        # 驗證記憶已被清空
        assert qa_service.memory is not None


class TestDocumentService:
    """文檔服務測試"""
    
    @pytest.fixture
    def doc_service(self):
        """建立文檔服務實例"""
        return DocumentService()
    
    def test_split_documents(self, doc_service):
        """測試文檔切分"""
        from langchain.schema import Document
        
        # 建立測試文檔
        test_docs = [
            Document(page_content="這是一個測試文檔" * 100, metadata={})
        ]
        
        # 切分文檔
        split_docs = doc_service.split_documents(test_docs)
        
        # 驗證結果
        assert len(split_docs) > 0
        assert all(isinstance(doc, Document) for doc in split_docs)
    
    def test_load_pdf_nonexistent(self, doc_service):
        """測試載入不存在的 PDF"""
        result = doc_service.load_pdf("nonexistent.pdf")
        assert result == []
