/**
 * CYCU ChatBot - Main Application Script
 * 中原大學智能問答系統 - 主要應用程式腳本
 */

// 配置
const CONFIG = {
    API_BASE_URL: window.location.origin + '/api/chat',
    MAX_MESSAGE_LENGTH: 1000,
    TYPING_DELAY: 1000,
    AUTO_RESIZE_TEXTAREA: true,
    TOAST_DURATION: 2800
};

// 應用狀態
const state = {
    isLoading: false,
    isDarkTheme: false,
    conversationHistory: [],
    recognition: null
};

// DOM 元素
const elements = {
    chatBox: null,
    userInput: null,
    sendBtn: null,
    voiceBtn: null,
    themeToggle: null,
    resetBtn: null,
    loading: null,
    quickPrompts: null,
    charCounter: null,
    messageCountPill: null,
    emptyState: null,
    toastContainer: null
};

/**
 * 初始化應用程式
 */
function initApp() {
    elements.chatBox = document.getElementById('chat-box');
    elements.userInput = document.getElementById('user-input');
    elements.sendBtn = document.getElementById('send-btn');
    elements.voiceBtn = document.getElementById('voice-btn');
    elements.themeToggle = document.getElementById('theme-toggle');
    elements.resetBtn = document.getElementById('reset-btn');
    elements.loading = document.getElementById('loading');
    elements.quickPrompts = document.getElementById('quick-prompts');
    elements.charCounter = document.getElementById('char-counter');
    elements.messageCountPill = document.getElementById('message-count-pill');
    elements.emptyState = document.getElementById('chat-empty-state');
    elements.toastContainer = document.getElementById('toast-container');

    setupEventListeners();
    loadThemePreference();
    initSpeechRecognition();
    updateCharCounter();
    updateMessageCount();

    setTimeout(() => {
        addMessage('bot', '你好！我是中原大學校園嚮導 🎓\n\n您可以詢問我任何關於中原大學的問題，例如：\n• 學則規定\n• 獎學金申請\n• 課程相關規定\n• 學生事務\n\n請問有什麼我可以幫助您的嗎？');
    }, CONFIG.TYPING_DELAY);
}

/**
 * 設置事件監聽器
 */
function setupEventListeners() {
    elements.sendBtn.addEventListener('click', handleSendMessage);

    elements.userInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            handleSendMessage();
        }
    });

    if (CONFIG.AUTO_RESIZE_TEXTAREA) {
        elements.userInput.addEventListener('input', () => {
            autoResizeTextarea();
            updateCharCounter();
        });
    }

    elements.themeToggle.addEventListener('click', toggleTheme);
    elements.resetBtn.addEventListener('click', resetConversation);
    elements.voiceBtn.addEventListener('click', startVoiceRecognition);

    if (elements.quickPrompts) {
        elements.quickPrompts.addEventListener('click', handlePromptClick);
    }
}

/**
 * 點擊快捷提問
 */
function handlePromptClick(event) {
    const chip = event.target.closest('.prompt-chip');
    if (!chip || state.isLoading) {
        return;
    }

    const prompt = chip.dataset.prompt?.trim();
    if (!prompt) {
        return;
    }

    elements.userInput.value = prompt;
    autoResizeTextarea();
    updateCharCounter();
    handleSendMessage(prompt);
}

/**
 * 處理發送訊息
 */
async function handleSendMessage(messageOverride = null) {
    const message = (messageOverride ?? elements.userInput.value).trim();

    if (!message) {
        showToast('請輸入問題', 'warning');
        return;
    }

    if (message.length > CONFIG.MAX_MESSAGE_LENGTH) {
        showToast(`問題長度不能超過 ${CONFIG.MAX_MESSAGE_LENGTH} 個字元`, 'warning');
        return;
    }

    if (state.isLoading) {
        return;
    }

    elements.userInput.value = '';
    resetTextareaHeight();
    updateCharCounter();

    addMessage('user', message);
    await sendMessageToAPI(message);
}

/**
 * 發送訊息到 API
 */
async function sendMessageToAPI(question) {
    try {
        setLoading(true);
        addTypingIndicator();

        const response = await fetch(`${CONFIG.API_BASE_URL}/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question })
        });

        const data = await response.json();

        if (response.ok && data.status === 'success') {
            addMessage('bot', data.response);

            state.conversationHistory.push({
                question,
                answer: data.response,
                timestamp: new Date()
            });
        } else {
            throw new Error(data.error || '未知錯誤');
        }
    } catch (error) {
        console.error('API Error:', error);
        addMessage('bot', '抱歉，無法連接到伺服器。請稍後再試。');
        showToast('連接失敗，請檢查網路連線', 'error');
    } finally {
        removeTypingIndicator();
        setLoading(false);
    }
}

/**
 * 新增訊息到聊天框
 */
function addMessage(sender, message) {
    hideEmptyState();

    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', `${sender}-message`);

    const avatar = document.createElement('div');
    avatar.classList.add('message-avatar');
    avatar.innerHTML = sender === 'bot'
        ? '<i class="fas fa-robot"></i>'
        : '<i class="fas fa-user"></i>';

    const messageBubble = document.createElement('div');
    messageBubble.classList.add('message-bubble');

    const messageContent = document.createElement('div');
    messageContent.classList.add('message-content');
    messageContent.innerHTML = escapeHtml(message).replace(/\n/g, '<br>');

    const meta = document.createElement('div');
    meta.classList.add('message-meta');

    const timestamp = document.createElement('div');
    timestamp.classList.add('message-timestamp');
    timestamp.textContent = formatTime(new Date());
    meta.appendChild(timestamp);

    if (sender === 'bot') {
        const copyBtn = document.createElement('button');
        copyBtn.classList.add('message-copy-btn');
        copyBtn.type = 'button';
        copyBtn.innerHTML = '<i class="fas fa-copy"></i> 複製';
        copyBtn.addEventListener('click', () => copyMessage(message, copyBtn));
        meta.appendChild(copyBtn);
    }

    messageBubble.appendChild(messageContent);
    messageBubble.appendChild(meta);

    if (sender === 'user') {
        messageDiv.appendChild(messageBubble);
        messageDiv.appendChild(avatar);
    } else {
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageBubble);
    }

    elements.chatBox.appendChild(messageDiv);
    updateMessageCount();
    scrollToBottom();
}

/**
 * 複製訊息內容
 */
async function copyMessage(message, button) {
    try {
        if (navigator.clipboard?.writeText) {
            await navigator.clipboard.writeText(message);
        } else {
            const temp = document.createElement('textarea');
            temp.value = message;
            document.body.appendChild(temp);
            temp.select();
            document.execCommand('copy');
            document.body.removeChild(temp);
        }

        button.innerHTML = '<i class="fas fa-check"></i> 已複製';
        showToast('已複製回答內容', 'success');

        setTimeout(() => {
            button.innerHTML = '<i class="fas fa-copy"></i> 複製';
        }, 1200);
    } catch (error) {
        console.error('複製失敗:', error);
        showToast('複製失敗，請手動選取文字', 'error');
    }
}

/**
 * 設置載入狀態
 */
function setLoading(isLoading) {
    state.isLoading = isLoading;
    elements.loading.style.display = isLoading ? 'flex' : 'none';
    elements.sendBtn.disabled = isLoading;
    elements.voiceBtn.disabled = isLoading;

    document.querySelectorAll('.prompt-chip').forEach((chip) => {
        chip.disabled = isLoading;
    });
}

/**
 * 新增 typing 指示訊息
 */
function addTypingIndicator() {
    if (document.getElementById('typing-indicator')) {
        return;
    }

    const typingMessage = document.createElement('div');
    typingMessage.id = 'typing-indicator';
    typingMessage.classList.add('message', 'bot-message', 'typing-message');

    const avatar = document.createElement('div');
    avatar.classList.add('message-avatar');
    avatar.innerHTML = '<i class="fas fa-robot"></i>';

    const bubble = document.createElement('div');
    bubble.classList.add('message-bubble');

    const content = document.createElement('div');
    content.classList.add('message-content');
    content.innerHTML = `
        <span class="typing-bubble">
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
        </span>
    `;

    bubble.appendChild(content);
    typingMessage.appendChild(avatar);
    typingMessage.appendChild(bubble);

    elements.chatBox.appendChild(typingMessage);
    scrollToBottom();
}

/**
 * 移除 typing 指示訊息
 */
function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

/**
 * 重置對話
 */
async function resetConversation() {
    if (!confirm('確定要清除所有對話記錄嗎？')) {
        return;
    }

    try {
        await fetch(`${CONFIG.API_BASE_URL}/reset`, {
            method: 'POST'
        });

        elements.chatBox.innerHTML = '';
        state.conversationHistory = [];
        updateMessageCount();
        showEmptyState();

        addMessage('bot', '對話已重置。請問有什麼我可以幫助您的嗎？');
        showToast('對話已重置', 'success');
    } catch (error) {
        console.error('Reset Error:', error);
        showToast('重置失敗', 'error');
    }
}

/**
 * 切換主題
 */
function toggleTheme() {
    state.isDarkTheme = !state.isDarkTheme;
    document.body.classList.toggle('dark-theme', state.isDarkTheme);

    const icon = elements.themeToggle.querySelector('i');
    icon.className = state.isDarkTheme ? 'fas fa-sun' : 'fas fa-moon';

    localStorage.setItem('darkTheme', state.isDarkTheme);
}

/**
 * 載入主題偏好設置
 */
function loadThemePreference() {
    const savedTheme = localStorage.getItem('darkTheme');
    if (savedTheme === 'true') {
        state.isDarkTheme = true;
        document.body.classList.add('dark-theme');
        elements.themeToggle.querySelector('i').className = 'fas fa-sun';
    }
}

/**
 * 初始化語音識別
 */
function initSpeechRecognition() {
    if (!('webkitSpeechRecognition' in window)) {
        elements.voiceBtn.disabled = true;
        elements.voiceBtn.title = '目前瀏覽器不支援語音輸入';
        return;
    }

    state.recognition = new webkitSpeechRecognition();
    state.recognition.continuous = false;
    state.recognition.interimResults = false;
    state.recognition.lang = 'zh-TW';

    state.recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        elements.userInput.value = transcript;
        autoResizeTextarea();
        updateCharCounter();
        showToast('語音轉文字完成', 'success');
    };

    state.recognition.onerror = (event) => {
        console.error('語音識別錯誤:', event.error);
        showToast('語音識別失敗，請重試', 'error');
        resetVoiceButton();
    };

    state.recognition.onend = () => {
        resetVoiceButton();
    };
}

/**
 * 開始語音識別
 */
function startVoiceRecognition() {
    if (!state.recognition || state.isLoading) {
        return;
    }

    try {
        state.recognition.start();
        elements.voiceBtn.innerHTML = '<i class="fas fa-microphone-slash"></i>';
        elements.voiceBtn.classList.add('recording');
    } catch (error) {
        console.error('無法啟動語音識別:', error);
        showToast('無法啟動語音輸入', 'error');
    }
}

/**
 * 重置語音按鈕
 */
function resetVoiceButton() {
    elements.voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
    elements.voiceBtn.classList.remove('recording');
}

/**
 * 自動調整輸入框高度
 */
function autoResizeTextarea() {
    const textarea = elements.userInput;
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
}

/**
 * 重置輸入框高度
 */
function resetTextareaHeight() {
    elements.userInput.style.height = 'auto';
}

/**
 * 更新輸入字數計數
 */
function updateCharCounter() {
    if (!elements.charCounter) {
        return;
    }

    const length = elements.userInput.value.length;
    elements.charCounter.textContent = `${length}/${CONFIG.MAX_MESSAGE_LENGTH}`;
    elements.charCounter.classList.remove('warn', 'danger');

    if (length >= CONFIG.MAX_MESSAGE_LENGTH * 0.8) {
        elements.charCounter.classList.add('warn');
    }

    if (length >= CONFIG.MAX_MESSAGE_LENGTH) {
        elements.charCounter.classList.remove('warn');
        elements.charCounter.classList.add('danger');
    }
}

/**
 * 更新訊息數量徽章
 */
function updateMessageCount() {
    if (!elements.messageCountPill || !elements.chatBox) {
        return;
    }

    const messageCount = elements.chatBox.querySelectorAll('.message:not(.typing-message)').length;
    elements.messageCountPill.innerHTML = `<i class="fas fa-comments"></i> ${messageCount} 則訊息`;
}

/**
 * 滾動到底部
 */
function scrollToBottom() {
    elements.chatBox.scrollTop = elements.chatBox.scrollHeight;
}

/**
 * 格式化時間
 */
function formatTime(date) {
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
}

/**
 * 顯示空狀態
 */
function showEmptyState() {
    if (elements.emptyState) {
        elements.emptyState.style.display = 'block';
    }
}

/**
 * 隱藏空狀態
 */
function hideEmptyState() {
    if (elements.emptyState) {
        elements.emptyState.style.display = 'none';
    }
}

/**
 * 顯示提示訊息
 */
function showToast(message, type = 'info') {
    if (!elements.toastContainer) {
        console.log(`[${type.toUpperCase()}] ${message}`);
        return;
    }

    const iconMap = {
        info: 'fa-circle-info',
        success: 'fa-circle-check',
        warning: 'fa-triangle-exclamation',
        error: 'fa-circle-xmark'
    };

    const toast = document.createElement('div');
    toast.classList.add('toast-item', type);

    const icon = document.createElement('i');
    icon.classList.add('fas', iconMap[type] || iconMap.info);

    const text = document.createElement('span');
    text.textContent = message;

    toast.appendChild(icon);
    toast.appendChild(text);
    elements.toastContainer.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, CONFIG.TOAST_DURATION);
}

/**
 * 避免訊息內容被當作 HTML 注入
 */
function escapeHtml(text) {
    return text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

// 當頁面載入完成時初始化應用程式
document.addEventListener('DOMContentLoaded', initApp);