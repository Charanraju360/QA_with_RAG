/* ============================================
   RAG Assistant - Frontend JavaScript
   Handles file upload and Q&A functionality
   ============================================ */

/* ============================================
   Configuration
   ============================================ */
const API_BASE_URL = 'http://localhost:8000/api';

/* ============================================
   DOM Elements
   ============================================ */
const fileInput = document.getElementById('fileInput');
const fileName = document.getElementById('fileName');
const uploadBtn = document.getElementById('uploadBtn');
const uploadStatus = document.getElementById('uploadStatus');
const uploadSection = document.getElementById('uploadSection');
const chatSection = document.getElementById('chatSection');
const chatMessages = document.getElementById('chatMessages');
const questionInput = document.getElementById('questionInput');
const askBtn = document.getElementById('askBtn');
const newDocBtn = document.getElementById('newDocBtn');

/* ============================================
   Application State
   ============================================ */
let isProcessing = false;

/* ============================================
   File Upload Handlers
   ============================================ */

// Handle file selection
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    
    if (file) {
        fileName.textContent = file.name;
        uploadBtn.disabled = false;
        uploadStatus.style.display = 'none';
    } else {
        fileName.textContent = 'No file selected';
        uploadBtn.disabled = true;
    }
});

// Handle document upload
uploadBtn.addEventListener('click', async () => {
    const file = fileInput.files[0];
    
    if (!file) {
        showStatus('Please select a file first', 'error');
        return;
    }

    // Validate file type
    const validExtensions = ['.pdf', '.docx', '.txt'];
    const fileExtension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
    
    if (!validExtensions.includes(fileExtension)) {
        showStatus('Invalid file type. Please upload PDF, DOCX, or TXT files only.', 'error');
        return;
    }

    try {
        isProcessing = true;
        uploadBtn.disabled = true;
        
        // Show loading state
        const btnText = uploadBtn.querySelector('.btn-text');
        const btnLoader = uploadBtn.querySelector('.btn-loader');
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline-block';
        
        showStatus('Processing document...', 'info');

        // Create FormData and upload
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        // Handle errors
        if (data.error) {
            showStatus(`Error: ${data.error}`, 'error');
            btnText.style.display = 'inline';
            btnLoader.style.display = 'none';
            uploadBtn.disabled = false;
            return;
        }

        // Success - show message
        showStatus(`✓ Document processed successfully! ${data.chunks} chunks created.`, 'success');
        
        // Switch to chat view after delay
        setTimeout(() => {
            uploadSection.style.display = 'none';
            chatSection.style.display = 'block';
            questionInput.focus();
        }, 1500);

    } catch (error) {
        console.error('Upload error:', error);
        showStatus('Failed to upload document. Please ensure the backend server is running at http://localhost:8000', 'error');
        
        // Reset button state
        const btnText = uploadBtn.querySelector('.btn-text');
        const btnLoader = uploadBtn.querySelector('.btn-loader');
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
        uploadBtn.disabled = false;
    } finally {
        isProcessing = false;
    }
});

/* ============================================
   Chat Handlers
   ============================================ */

// Ask question function
async function askQuestion() {
    const question = questionInput.value.trim();
    
    if (!question) {
        return;
    }
    
    // Disable input during processing
    questionInput.disabled = true;
    askBtn.disabled = true;
    
    // Add user message to chat
    addMessage(question, 'user');
    
    // Clear input field
    questionInput.value = '';
    
    // Show loading indicator
    const loadingId = addLoadingMessage();
    
    try {
        // Send question to backend
        const response = await fetch(`${API_BASE_URL}/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question })
        });
        
        const data = await response.json();
        
        // Remove loading indicator
        removeLoadingMessage(loadingId);
        
        // Display response
        if (data.error) {
            addMessage(`Error: ${data.error}`, 'assistant');
        } else {
            addMessage(data.answer, 'assistant');
        }
        
    } catch (error) {
        console.error('Ask error:', error);
        removeLoadingMessage(loadingId);
        addMessage('Failed to get answer. Please ensure the backend server is running at http://localhost:8000', 'assistant');
    } finally {
        // Re-enable input
        questionInput.disabled = false;
        askBtn.disabled = false;
        questionInput.focus();
    }
}

// Send button click
askBtn.addEventListener('click', askQuestion);

// Enter key to send
questionInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        askQuestion();
    }
});

// New document button
newDocBtn.addEventListener('click', () => {
    // Reset upload section
    fileInput.value = '';
    fileName.textContent = 'No file selected';
    uploadBtn.disabled = true;
    uploadStatus.style.display = 'none';
    
    // Clear chat messages
    chatMessages.innerHTML = `
        <div class="welcome-message">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L2 7V17L12 22L22 17V7L12 2Z" fill="none" stroke="#ffd700" stroke-width="2"/>
                <circle cx="12" cy="12" r="3" fill="#1a1a1a"/>
            </svg>
            <p>Document processed successfully. Ask me anything!</p>
        </div>
    `;
    
    // Switch back to upload view
    chatSection.style.display = 'none';
    uploadSection.style.display = 'flex';
});

/* ============================================
   Helper Functions
   ============================================ */

// Show status message
function showStatus(message, type) {
    uploadStatus.textContent = message;
    uploadStatus.className = `status-message ${type}`;
    uploadStatus.style.display = 'block';
}

// Add message to chat
function addMessage(content, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message message-${type}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const p = document.createElement('p');
    p.textContent = content;
    
    contentDiv.appendChild(p);
    messageDiv.appendChild(contentDiv);
    
    // Remove welcome message if present
    const welcomeMsg = chatMessages.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.remove();
    }
    
    chatMessages.appendChild(messageDiv);
    
    // Auto-scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Add loading indicator
function addLoadingMessage() {
    const loadingDiv = document.createElement('div');
    const loadingId = 'loading-' + Date.now();
    loadingDiv.id = loadingId;
    loadingDiv.className = 'message message-assistant';
    
    loadingDiv.innerHTML = `
        <div class="message-loading">
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
        </div>
    `;
    
    chatMessages.appendChild(loadingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return loadingId;
}

// Remove loading indicator
function removeLoadingMessage(loadingId) {
    const loadingDiv = document.getElementById(loadingId);
    if (loadingDiv) {
        loadingDiv.remove();
    }
}

/* ============================================
   Initialization
   ============================================ */
console.log('✓ RAG Assistant Frontend Loaded');
console.log('✓ API Base URL:', API_BASE_URL);
console.log('✓ Ready to process documents');