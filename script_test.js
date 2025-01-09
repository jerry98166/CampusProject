// 當頁面載入後，延遲 1 秒顯示歡迎訊息
window.onload = function () {
    setTimeout(function () {
        addMessage('bot', '哈囉！可以問我任何關於中原大學的問題～😊😊');
    }, 2000); // 延遲 1 秒 (2000 毫秒)
};

// 監聽按鈕點擊事件
document.getElementById('send-btn').addEventListener('click', sendMessage);

// 監聽Enter鍵事件
document.getElementById('user-input').addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
        sendMessage();  // 當按下Enter鍵時，發送訊息
    }
});

// 語音辨識功能
if ('webkitSpeechRecognition' in window) {
    const recognition = new webkitSpeechRecognition();
    recognition.continuous = false; // 是否連續辨識
    recognition.interimResults = false; // 是否返回中間結果
    recognition.lang = 'zh-TW'; // 設定語言（繁體中文）

    const voiceBtn = document.getElementById('voice-btn');
    const userInput = document.getElementById('user-input');

    // 當點擊語音按鈕時，開始語音辨識
    voiceBtn.addEventListener('click', () => {
        recognition.start();
        voiceBtn.innerHTML = '<i class="fas fa-microphone-slash"></i> 辨識中...';
        voiceBtn.disabled = true; // 防止重複啟動
    });

    // 當辨識結果返回時，將語音轉換成文字
    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript; // 獲取辨識到的文字
        userInput.value = transcript; // 將文字顯示在輸入框中
        recognition.stop();
        voiceBtn.innerHTML = '<i class="fas fa-microphone"></i> 語音輸入';
        voiceBtn.disabled = false; // 重新啟用按鈕
    };

    // 當語音辨識結束
    recognition.onend = () => {
        voiceBtn.innerHTML = '<i class="fas fa-microphone"></i> 語音輸入';
        voiceBtn.disabled = false;
    };

    // 處理語音辨識錯誤
    recognition.onerror = (event) => {
        console.error('語音辨識錯誤:', event.error);
        alert('語音辨識失敗，請重試。');
        recognition.stop();
        voiceBtn.innerHTML = '<i class="fas fa-microphone"></i> 語音輸入';
        voiceBtn.disabled = false;
    };
} else {
    alert('您的瀏覽器不支援語音辨識功能，請嘗試使用 Chrome 瀏覽器。');
}

// 發送訊息的函式
async function sendMessage() {
    const userInput = document.getElementById('user-input').value;

    if (userInput.trim() !== "") {
        addMessage('user', userInput);  // 新增使用者訊息到聊天框
        document.getElementById('user-input').value = "";  // 清空輸入欄位

        // 顯示 "加載中" 動畫
        showLoading();

        // 發送問題到後端 API
        try {
            const response = await fetch('https://c1b5-111-243-149-149.ngrok-free.app/ask', {  // 替換為你的後端API URL
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: userInput }),  // 以JSON格式發送使用者的問題
            });

            const data = await response.json();

            // 隱藏 "加載中" 動畫
            hideLoading();

            if (response.ok) {
                addMessage('bot', data.response);  // 顯示機器人回覆
            } else {
                addMessage('bot', '伺服器回應錯誤：' + data.error);  // 顯示伺服器錯誤訊息
            }
        } catch (error) {
            addMessage('bot', '無法連接到伺服器，請稍後再試。');
            console.error('Error:', error);

            // 隱藏 "加載中" 動畫
            hideLoading();
        }
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
    chatBox.scrollTop = chatBox.scrollHeight;  // 自動滾動到最新訊息
}

// 顯示加載動畫的函式
function showLoading() {
    document.getElementById('loading').style.display = 'block';
}

// 隱藏加載動畫的函式
function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}