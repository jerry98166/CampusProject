"""
QA Service Module
問答服務核心業務邏輯
"""
import os
from typing import Dict, List, Any

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

from config import get_config
from utils.logger import get_logger

logger = get_logger(__name__)
config = get_config()


class QAService:
    """問答服務類"""
    
    def __init__(self):
        """初始化問答服務"""
        self.config = config
        self.embeddings = None
        self.vector_store = None
        self.qa_chain = None
        self.chat_history = []
        
        self._initialize()
    
    def _initialize(self):
        """初始化向量資料庫和問答鏈"""
        try:
            logger.info("正在初始化問答服務...")
            
            # 初始化 embeddings
            self.embeddings = OpenAIEmbeddings(
                openai_api_key=self.config.OPENAI_API_KEY
            )
            
            # 載入或建立向量資料庫
            self._load_vector_store()
            
            # 建立問答鏈
            self._create_qa_chain()
            
            logger.info("問答服務初始化完成")
            
        except Exception as e:
            logger.error(f"初始化問答服務時發生錯誤: {str(e)}", exc_info=True)
            raise
    
    def _load_vector_store(self):
        """載入向量資料庫"""
        vector_store_path = str(self.config.VECTOR_STORE_PATH)
        
        if os.path.exists(vector_store_path):
            logger.info(f"從 {vector_store_path} 載入向量資料庫...")
            try:
                self.vector_store = FAISS.load_local(
                    vector_store_path,
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                logger.info("向量資料庫載入成功")
            except Exception as e:
                logger.error(f"載入向量資料庫失敗: {str(e)}")
                raise ValueError(
                    f"向量資料庫載入失敗。請確保 {vector_store_path} 存在且格式正確，"
                    "或運行 scripts/build_vector_store.py 重新建立向量資料庫"
                )
        else:
            raise ValueError(
                f"向量資料庫不存在於 {vector_store_path}。"
                "請先運行 scripts/build_vector_store.py 建立向量資料庫"
            )
    
    def _create_qa_chain(self):
        """建立問答鏈"""
        if not self.vector_store:
            raise ValueError("向量資料庫未初始化")
        
        # 建立檢索器
        retriever = self.vector_store.as_retriever(
            search_kwargs={"k": self.config.SIMILARITY_SEARCH_K}
        )
        
        # 建立 LLM
        llm = ChatOpenAI(
            model=self.config.OPENAI_MODEL,
            openai_api_key=self.config.OPENAI_API_KEY,
            temperature=0.3
        )
        
        # 定義提示模板
        template = """你是中原大學的 AI 助理，專門回答關於學校規章制度的問題。
請根據以下提供的上下文資訊來回答問題。如果問題無法從提供的資訊中找到答案，請誠實地說你不知道。

上下文資訊：
{context}

問題：{question}

請提供詳細且準確的回答："""
        
        prompt = ChatPromptTemplate.from_template(template)
        
        # 建立 LCEL 鏈
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        
        self.qa_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        
        logger.info("問答鏈建立成功")
    
    def get_answer(self, question: str) -> str:
        """
        獲取問題的答案
        
        Args:
            question: 用戶的問題
            
        Returns:
            AI 生成的答案
        """
        if not self.qa_chain:
            raise ValueError("問答鏈未初始化")
        
        try:
            logger.info(f"處理問題: {question[:50]}...")
            
            # 調用問答鏈
            answer = self.qa_chain.invoke(question)
            
            # 保存對話歷史
            self.chat_history.append({"role": "user", "content": question})
            self.chat_history.append({"role": "assistant", "content": answer})
            
            return answer
            
        except Exception as e:
            logger.error(f"生成答案時發生錯誤: {str(e)}", exc_info=True)
            return "抱歉，處理您的問題時發生錯誤，請稍後再試。"
    
    def reset_memory(self):
        """重置對話記憶"""
        try:
            self.chat_history = []
            logger.info("對話記憶已重置")
        except Exception as e:
            logger.error(f"重置記憶時發生錯誤: {str(e)}", exc_info=True)
            raise
    
    def get_chat_history(self) -> List[Dict[str, Any]]:
        """
        獲取對話歷史
        
        Returns:
            對話歷史列表
        """
        try:
            return self.chat_history
        except Exception as e:
            logger.error(f"獲取對話歷史時發生錯誤: {str(e)}", exc_info=True)
            return []
