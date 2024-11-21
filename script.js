// 當頁面載入後，延遲 1 秒顯示歡迎訊息
window.onload = function() {
    setTimeout(function() {
        addMessage('bot', '哈囉！可以問我任何關於中原大學的問題～😊😊');
    }, 2000); // 延遲 1 秒 (2000 毫秒)
};

// 監聽 'click' 事件，當按下發送按鈕時發送訊息
document.getElementById('send-btn').addEventListener('click', function () {
    sendMessage();
});

// 監聽 'keydown' 事件，當按下 Enter 鍵時發送訊息
document.getElementById('user-input').addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {  // 檢查是否按下了 Enter 鍵
        sendMessage();
    }
});

// 切換主題功能
document.getElementById('theme-toggle').addEventListener('click', function () {
    document.body.classList.toggle('dark-theme');
    const icon = document.querySelector('#theme-toggle i');
    icon.classList.toggle('fa-moon');
    icon.classList.toggle('fa-sun');
});

// 發送訊息的函式
function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (userInput.trim() !== "") {
        addMessage('user', userInput);
        document.getElementById('user-input').value = "";
        // 模擬請求後端處理
        simulateBotResponse(userInput);
    }
}

// 新增訊息到對話框的函式
function addMessage(sender, message) {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender + '-message');
    
    const textNode = document.createTextNode(message);
    messageDiv.appendChild(textNode);

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// 模擬機器人回覆的函式
function simulateBotResponse(userMessage) {
    showLoading();
    setTimeout(function () {
        hideLoading();
        const botResponse = "這是機器人的回覆: " + userMessage;
        addMessage('bot', botResponse);
    }, 1500);
}

// 顯示載入中的動畫
function showLoading() {
    document.getElementById('loading').style.display = 'block';
}

// 隱藏載入中的動畫
function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}