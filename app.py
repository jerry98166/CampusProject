from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os
from pyngrok import conf, ngrok
import logging

# 載入 .env 檔案中的環境變數
load_dotenv()

# 設定 ngrok 的路徑
conf.get_default().ngrok_path = "/opt/homebrew/bin/ngrok"

# 建立 Flask 應用程式
app = Flask(__name__)
CORS(app)

# 從環境變數中讀取 OpenAI API 金鑰
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("金鑰未正確設定。請確保 .env 檔案中包含 OPENAI_API_KEY")

# 向量資料庫檔案路徑
vector_store_path = "/path/to/your/vector_store"

# 檢查向量資料庫是否已經存在
if os.path.exists(vector_store_path):
    # 讀取已儲存的向量資料庫
    vector_store = FAISS.load_local(vector_store_path, OpenAIEmbeddings(openai_api_key=openai_api_key))
    logging.info("讀取已儲存的向量資料庫")
else:
    # 載入 PDF 文件
    pdf_loader = PyPDFLoader("/path/to/your/pdf.pdf")
    documents = pdf_loader.load()

    # 建立向量資料庫
    embedding = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vector_store = FAISS.from_documents(documents, embedding)

    # 儲存向量資料庫
    vector_store.save_local(vector_store_path)
    logging.info("儲存新的向量資料庫")

# 創建檢索器
retriever = vector_store.as_retriever()

# 使用 ConversationBufferMemory 來保存對話上下文
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 創建一個帶有對話記憶的問答鏈
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-4", openai_api_key=openai_api_key), 
    retriever=retriever,
    memory=memory
)

# 問答功能，保持上下文
@app.route("/ask", methods=["POST"])
def ask_question():
    data = request.json
    question = data.get("question")

    if not question:
        return jsonify({"error": "問題不能為空"}), 400

    try:
        # 生成回覆
        result = qa_chain({"question": question})
        answer = result["answer"]

        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 啟動 Ngrok
if __name__ == "__main__":
    # 建立 Ngrok 隧道，將本地 8080 端口暴露給外部
    public_url = ngrok.connect(8080)
    print(f" * Ngrok tunnel \"{public_url}\" -> http://127.0.0.1:8080")

    # 啟動 Flask 伺服器
    app.run(host="0.0.0.0", port=8080)