import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
from pyngrok import conf, ngrok

# 載入 .env 檔案中的環境變數
load_dotenv()

# 設定 ngrok 的路徑
conf.get_default().ngrok_path = "/opt/homebrew/bin/ngrok"

# 建立 Flask 應用程式
app = Flask(__name__)
CORS(app)

# 確保 OpenAI API 金鑰存在
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("金鑰未正確設定。請確保 .env 檔案中包含 OPENAI_API_KEY")

# PDF 文件與向量資料庫的路徑
pdf_path = "/Users/gaomenglin/Desktop/university-query-platform/cycu_merged.pdf"
vector_store_path = "/Users/gaomenglin/Desktop/university-query-platform/vector_store"

# 檢查是否有已保存的向量資料庫
if os.path.exists(vector_store_path):
    print("從檔案載入向量資料庫...")
    vector_store = FAISS.load_local(vector_store_path, OpenAIEmbeddings(openai_api_key=openai_api_key))
else:
    print("沒有找到向量資料庫，重新生成...")
    # 載入 PDF 文件並生成向量
    pdf_loader = PyPDFLoader(pdf_path)
    documents = pdf_loader.load()
    embedding = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vector_store = FAISS.from_documents(documents, embedding)
    # 儲存向量資料庫
    vector_store.save_local(vector_store_path)
    print("向量資料庫已儲存至:", vector_store_path)

# 創建檢索器
retriever = vector_store.as_retriever()

# 使用 ConversationBufferMemory 來保存對話上下文
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 創建問答鏈
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
        result = qa_chain({"question": question})
        answer = result["answer"]

        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 啟動 Ngrok
if __name__ == "__main__":
    public_url = ngrok.connect(8080)
    print(f" * Ngrok tunnel \"{public_url}\" -> http://127.0.0.1:8080")
    app.run(host="0.0.0.0", port=8080)