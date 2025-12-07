class ThinkerWorkshop {
    constructor() {
        this.dialoguePanel = document.getElementById('dialogue-panel');
        this.archivePanel = document.getElementById('archive-panel');
        this.messageContainer = document.getElementById('messages');
        this.sourcesDisplay = document.getElementById('sources-display');
        this.userInput = document.getElementById('user-input');
        this.sendButton = document.getElementById('submit-btn');
        this.uploadButton = document.getElementById('upload-btn');
        this.fileInput = document.getElementById('file-input');
        this.userStatus = document.getElementById('user-status');
        this.providerSelect = document.getElementById('provider-select');
        this.modelSelect = document.getElementById('model-select');
        this.enhancedModeToggle = document.getElementById('enhanced-mode-toggle');
        this.answerLengthSlider = document.getElementById('answer-length');
        this.answerLengthValue = document.getElementById('answer-length-value');
        this.quoteCountSlider = document.getElementById('quote-count');
        this.quoteCountValue = document.getElementById('quote-count-value');
        this.fontSizeSlider = document.getElementById('font-size-slider');
        this.fontSizeValue = document.getElementById('font-size-value');
        this.knowledgePanel = document.getElementById('knowledge-panel');
        this.avatarButtons = document.querySelectorAll('.avatar-btn');
        
        this.databases = [];
        this.providers = [];
        this.selectedDatabase = 'freud';
        this.currentEventSource = null;
        this.currentSources = [];
        this.knowledgeQuotes = [];
        this.knowledgeFacts = [];
        this.bottomPositions = [];
        this.currentQuoteIndex = 0;
        this.quoteRotationInterval = null;
        this.factRotationInterval = null;
        
        this.thinkerConfig = {
            freud: { name: 'Freud', emoji: '👴', color: 'freud' },
            kuczynski: { name: 'ZHI', emoji: '🤓', color: 'kuczynski' },
            jung: { name: 'Jung', emoji: '🧔', color: 'jung' }
        };
        
        this.workLinks = {
            'ZHI': { title: 'Conceptual Atomism' },
            'EP': { title: 'Essays in Philosophy' },
            'CFACT': { title: 'Curious Facts' },
            'ANALPHIL': { title: 'Analytic Philosophy' },
            'CATOM': { title: 'Conception and Causation' },
            'KMETA': { title: 'Metaphysics & Epistemology' },
            'KEPIST': { title: 'Theoretical Knowledge' },
            'OCD': { title: 'OCD and Philosophy' },
            'DOCD': { title: 'Dialogue on OCD' },
            'ATTACH': { title: 'Attachment Theory' },
            'CHOMSKY': { title: "Chomsky's Contributions" },
            'KANT': { title: 'Kant and Hume on Induction' },
            'INTENS': { title: 'Intensionality and Modality' },
            'LOGIC': { title: 'Logic and Set Theory' },
            'MORAL': { title: 'Moral Structure of Legal Obligation' },
            'FREUD': { title: 'Works of Freud' },
            'JUNG': { title: 'Works of Jung' }
        };
        
        this.readerModal = null;
        this.createReaderModal();
        
        this.setupEventListeners();
        this.loadDatabases();
        this.loadProviders();
        this.checkSession();
        this.showWelcomeMessage();
        this.loadSavedFontSize();
    }
    
    setupEventListeners() {
        this.sendButton.addEventListener('click', () => this.sendMessage());
        
        this.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        this.userInput.addEventListener('input', () => {
            this.autoExpandTextarea();
        });
        
        this.uploadButton.addEventListener('click', () => {
            this.fileInput.click();
        });
        
        this.fileInput.addEventListener('change', (e) => {
            if (e.target.files[0]) {
                this.handleFileUpload(e.target.files[0]);
            }
        });
        
        this.avatarButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                this.selectThinker(btn.dataset.db);
            });
        });
        
        this.providerSelect.addEventListener('change', () => {
            this.updateModelDropdown();
        });
        
        this.answerLengthSlider.addEventListener('input', () => {
            this.answerLengthValue.textContent = this.answerLengthSlider.value;
        });
        
        this.quoteCountSlider.addEventListener('input', () => {
            this.quoteCountValue.textContent = this.quoteCountSlider.value;
        });
        
        this.fontSizeSlider.addEventListener('input', () => {
            const size = this.fontSizeSlider.value;
            this.fontSizeValue.textContent = size + '%';
            this.applyFontSize(size);
        });
        
        document.getElementById('download-chat-btn').addEventListener('click', () => {
            this.downloadCompleteChat('md');
        });
        
        document.getElementById('clear-chat-btn').addEventListener('click', () => {
            this.clearChat();
        });
        
        document.getElementById('close-knowledge-panel').addEventListener('click', () => {
            this.hideKnowledgePanel();
        });
        
        this.archiveFontSize = 100;
        document.getElementById('archive-font-down').addEventListener('click', () => {
            this.adjustArchiveFontSize(-10);
        });
        document.getElementById('archive-font-up').addEventListener('click', () => {
            this.adjustArchiveFontSize(10);
        });
        this.loadArchiveFontSize();
    }
    
    hideKnowledgePanel() {
        this.knowledgePanel.style.display = 'none';
        if (this.quoteRotationInterval) {
            clearInterval(this.quoteRotationInterval);
            this.quoteRotationInterval = null;
        }
        if (this.factRotationInterval) {
            clearInterval(this.factRotationInterval);
            this.factRotationInterval = null;
        }
    }
    
    adjustArchiveFontSize(delta) {
        this.archiveFontSize = Math.max(50, Math.min(150, this.archiveFontSize + delta));
        document.getElementById('archive-font-size').textContent = this.archiveFontSize + '%';
        this.applyArchiveFontSize();
        localStorage.setItem('freudgpt-archive-font-size', this.archiveFontSize);
    }
    
    applyArchiveFontSize() {
        const scale = this.archiveFontSize / 100;
        const baseFontSize = 0.7 * scale;
        document.querySelectorAll('.quote-text').forEach(el => {
            el.style.fontSize = baseFontSize + 'em';
        });
        document.querySelectorAll('.source-text').forEach(el => {
            el.style.fontSize = (0.75 * scale) + 'em';
        });
    }
    
    loadArchiveFontSize() {
        const saved = localStorage.getItem('freudgpt-archive-font-size');
        if (saved) {
            this.archiveFontSize = parseInt(saved);
            document.getElementById('archive-font-size').textContent = this.archiveFontSize + '%';
            this.applyArchiveFontSize();
        }
    }
    
    selectThinker(database) {
        this.selectedDatabase = database;
        this.avatarButtons.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.db === database);
        });
    }
    
    applyFontSize(sizePercent) {
        const scale = sizePercent / 100;
        const dialogueFontSize = (0.85 * scale) + 'em';
        const archiveFontSize = (0.75 * scale) + 'em';
        const archiveIdSize = (0.65 * scale) + 'em';
        
        document.querySelectorAll('.message-text').forEach(el => {
            el.style.fontSize = dialogueFontSize;
        });
        
        document.querySelectorAll('.source-text').forEach(el => {
            el.style.fontSize = archiveFontSize;
        });
        
        document.querySelectorAll('.source-id').forEach(el => {
            el.style.fontSize = archiveIdSize;
        });
        
        localStorage.setItem('freudgpt-font-size', sizePercent);
    }
    
    loadSavedFontSize() {
        const saved = localStorage.getItem('freudgpt-font-size');
        const fontSize = saved || '130';
        this.fontSizeSlider.value = fontSize;
        this.fontSizeValue.textContent = fontSize + '%';
        this.applyFontSize(fontSize);
    }
    
    async loadDatabases() {
        try {
            const response = await fetch('/api/databases');
            const data = await response.json();
            this.databases = data.databases;
            this.updateAvatarCounts();
            this.updateFooterStats();
        } catch (error) {
            console.error('Failed to load databases:', error);
        }
    }
    
    updateAvatarCounts() {
        this.databases.forEach(db => {
            const countEl = document.getElementById(`${db.id === 'kuczynski' ? 'zhi' : db.id}-count`);
            if (countEl) {
                countEl.textContent = db.count.toLocaleString();
            }
        });
    }
    
    updateFooterStats() {
        const totalPositions = this.databases.reduce((sum, db) => sum + db.count, 0);
        document.getElementById('footer-stats').textContent = 
            `Powered by ${totalPositions.toLocaleString()} philosophical positions from Freud, ZHI & Jung`;
    }
    
    async loadProviders() {
        try {
            const response = await fetch('/api/providers');
            const data = await response.json();
            this.providers = data.providers;
            this.updateProviderDropdown();
        } catch (error) {
            console.error('Failed to load providers:', error);
            this.providerSelect.innerHTML = '<option value="">No providers available</option>';
        }
    }
    
    updateProviderDropdown() {
        if (this.providers.length === 0) {
            this.providerSelect.innerHTML = '<option value="">No providers configured</option>';
            return;
        }
        
        this.providerSelect.innerHTML = this.providers.map(p => 
            `<option value="${p.id}" ${p.default ? 'selected' : ''}>${p.name}</option>`
        ).join('');
        
        this.updateModelDropdown();
    }
    
    updateModelDropdown() {
        const selectedProvider = this.providers.find(p => p.id === this.providerSelect.value);
        if (!selectedProvider) {
            this.modelSelect.innerHTML = '<option value="">Default</option>';
            return;
        }
        
        this.modelSelect.innerHTML = '<option value="">Default</option>' + 
            selectedProvider.models.map(m => 
                `<option value="${m}">${m}</option>`
            ).join('');
    }
    
    autoExpandTextarea() {
        this.userInput.style.height = 'auto';
        const newHeight = Math.min(this.userInput.scrollHeight, 200);
        this.userInput.style.height = newHeight + 'px';
    }
    
    async checkSession() {
        try {
            const response = await fetch('/api/check-session');
            const data = await response.json();
            if (data.logged_in) {
                this.updateUserStatus(data.username);
            } else {
                this.updateUserStatus(null);
            }
        } catch (error) {
            console.error('Session check failed:', error);
        }
    }
    
    updateUserStatus(username) {
        if (username) {
            this.userStatus.innerHTML = `
                <span>Welcome, ${username}</span>
                <button class="btn-link" onclick="workshop.logout()">Logout</button>
            `;
        } else {
            this.userStatus.innerHTML = `
                <button class="btn-link" onclick="workshop.showLoginModal()">Login</button>
            `;
        }
    }
    
    showLoginModal() {
        const modal = document.getElementById('login-modal');
        const usernameInput = document.getElementById('username-input');
        const submitBtn = document.getElementById('login-submit-btn');
        const cancelBtn = document.getElementById('login-cancel-btn');
        
        modal.style.display = 'flex';
        usernameInput.value = '';
        usernameInput.focus();
        
        const handleSubmit = async () => {
            const username = usernameInput.value.trim();
            if (username) {
                try {
                    const response = await fetch('/api/login', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({username})
                    });
                    if (response.ok) {
                        modal.style.display = 'none';
                        this.updateUserStatus(username);
                    }
                } catch (error) {
                    console.error('Login failed:', error);
                }
            }
        };
        
        submitBtn.onclick = handleSubmit;
        cancelBtn.onclick = () => modal.style.display = 'none';
        usernameInput.onkeypress = (e) => {
            if (e.key === 'Enter') handleSubmit();
        };
    }
    
    async logout() {
        try {
            await fetch('/api/logout', {method: 'POST'});
            this.updateUserStatus(null);
        } catch (error) {
            console.error('Logout failed:', error);
        }
    }
    
    async handleFileUpload(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        this.uploadButton.disabled = true;
        
        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            if (data.text) {
                this.userInput.value = data.text;
                this.autoExpandTextarea();
                this.userInput.focus();
            } else if (data.error) {
                alert('Error: ' + data.error);
            }
        } catch (error) {
            alert('Error uploading file: ' + error.message);
        } finally {
            this.uploadButton.disabled = false;
            this.fileInput.value = '';
        }
    }
    
    showWelcomeMessage() {
        if (this.messageContainer.children.length === 0) {
            const welcomeDiv = document.createElement('div');
            welcomeDiv.className = 'empty-state';
            welcomeDiv.innerHTML = `
                <h2>Welcome to the Workshop</h2>
                <p>Select a thinker below, then pose your question. Watch as their thoughts unfold in The Dialogue while original source texts appear in The Archive.</p>
            `;
            this.messageContainer.appendChild(welcomeDiv);
        }
    }
    
    async fetchKnowledgeContent(database) {
        try {
            const response = await fetch(`/api/random-quotes?database=${database}&count=8`);
            const data = await response.json();
            this.knowledgeQuotes = data.quotes || [];
            this.bottomPositions = data.positions || [];
            this.bottomPositionIndex = 0;
            return true;
        } catch (error) {
            console.error('Failed to fetch knowledge content:', error);
            return false;
        }
    }
    
    showKnowledgePanel(database) {
        if (!this.knowledgePanel) return;
        
        this.knowledgePanel.className = 'knowledge-panel';
        this.knowledgePanel.classList.add(`${database}-theme`);
        
        const config = this.thinkerConfig[database] || this.thinkerConfig.freud;
        
        const headerIcon = this.knowledgePanel.querySelector('.knowledge-icon');
        const headerTitle = this.knowledgePanel.querySelector('.knowledge-title');
        if (headerIcon) headerIcon.textContent = '📚';
        if (headerTitle) headerTitle.textContent = `From ${config.name}'s Archives`;
        
        this.currentQuoteIndex = 0;
        this.updateQuoteDisplay();
        this.updateFactDisplay();
        this.updateProgressDots();
        
        this.knowledgePanel.style.display = 'block';
        
        this.startQuoteRotation();
        this.startFactRotation();
    }
    
    updateQuoteDisplay() {
        const carousel = this.knowledgePanel.querySelector('.quote-carousel');
        if (!carousel || this.knowledgeQuotes.length === 0) return;
        
        const quote = this.knowledgeQuotes[this.currentQuoteIndex];
        
        carousel.innerHTML = `
            <div class="quote-card active">
                <div class="quote-text">${quote.text}</div>
            </div>
        `;
    }
    
    updateFactDisplay() {
        if (!this.bottomPositions || this.bottomPositions.length === 0) return;
        
        this.bottomPositionIndex = (this.bottomPositionIndex || 0) + 1;
        if (this.bottomPositionIndex >= this.bottomPositions.length) {
            this.bottomPositionIndex = 0;
        }
        
        const position = this.bottomPositions[this.bottomPositionIndex];
        
        const factText = this.knowledgePanel.querySelector('.fact-text');
        const factYear = this.knowledgePanel.querySelector('.fact-year');
        
        if (factText) factText.textContent = position.text;
        if (factYear) factYear.style.display = 'none';
    }
    
    updateProgressDots() {
        const dotsContainer = this.knowledgePanel.querySelector('.progress-dots');
        if (!dotsContainer) return;
        
        dotsContainer.innerHTML = this.knowledgeQuotes.map((_, i) => 
            `<div class="progress-dot ${i === this.currentQuoteIndex ? 'active' : ''}"></div>`
        ).join('');
    }
    
    startQuoteRotation() {
        if (this.quoteRotationInterval) clearInterval(this.quoteRotationInterval);
        
        this.quoteRotationInterval = setInterval(async () => {
            if (this.knowledgeQuotes.length > 1) {
                this.currentQuoteIndex++;
                
                if (this.currentQuoteIndex >= this.knowledgeQuotes.length) {
                    const database = this.selectedDatabase || 'freud';
                    await this.fetchMoreQuotes(database);
                }
                
                if (this.currentQuoteIndex < this.knowledgeQuotes.length) {
                    this.updateQuoteDisplay();
                    this.updateProgressDots();
                }
            }
        }, 4000);
    }
    
    async fetchMoreQuotes(database) {
        try {
            const existingIds = this.knowledgeQuotes.map(q => q.id).join(',');
            const response = await fetch(`/api/random-quotes?database=${database}&count=8&exclude=${encodeURIComponent(existingIds)}`);
            const data = await response.json();
            if (data.quotes && data.quotes.length > 0) {
                this.knowledgeQuotes = [...this.knowledgeQuotes, ...data.quotes];
            }
        } catch (error) {
            console.log('Could not fetch more quotes');
        }
    }
    
    startFactRotation() {
        if (this.factRotationInterval) clearInterval(this.factRotationInterval);
        
        this.factRotationInterval = setInterval(() => {
            this.updateFactDisplay();
        }, 1500);
    }
    
    hideKnowledgePanel() {
        if (!this.knowledgePanel) return;
        
        if (this.quoteRotationInterval) {
            clearInterval(this.quoteRotationInterval);
            this.quoteRotationInterval = null;
        }
        if (this.factRotationInterval) {
            clearInterval(this.factRotationInterval);
            this.factRotationInterval = null;
        }
        
        this.knowledgePanel.classList.add('hiding');
        setTimeout(() => {
            this.knowledgePanel.style.display = 'none';
            this.knowledgePanel.classList.remove('hiding');
        }, 300);
    }
    
    displaySources(sources) {
        if (!this.sourcesDisplay) return;
        
        if (!sources || sources.length === 0) {
            this.sourcesDisplay.innerHTML = `
                <div class="archive-placeholder">
                    <div class="placeholder-icon">📖</div>
                    <p>No sources available for this response</p>
                </div>
            `;
            return;
        }
        
        const sourceIcons = ['📜', '📄', '📖', '📝', '🗒️'];
        
        this.sourcesDisplay.innerHTML = sources.map((source, index) => `
            <div class="source-item" data-index="${index}">
                <div class="source-header">
                    <span class="source-icon">${sourceIcons[index % sourceIcons.length]}</span>
                    <span class="source-id">${source.id || `Source ${index + 1}`}</span>
                </div>
                <div class="source-text">${source.text}</div>
            </div>
        `).join('');
        
        this.sourcesDisplay.querySelectorAll('.source-item').forEach(item => {
            item.addEventListener('click', () => {
                document.querySelectorAll('.source-item').forEach(i => i.classList.remove('highlighted'));
                item.classList.add('highlighted');
            });
        });
    }
    
    async sendMessage() {
        const question = this.userInput.value.trim();
        if (!question) return;
        
        const welcomeMsg = this.messageContainer.querySelector('.empty-state');
        if (welcomeMsg) {
            welcomeMsg.remove();
        }
        
        this.addUserMessage(question);
        this.userInput.value = '';
        this.userInput.style.height = 'auto';
        
        this.sendButton.disabled = true;
        this.uploadButton.disabled = true;
        
        const database = this.selectedDatabase;
        
        await this.fetchKnowledgeContent(database);
        this.showKnowledgePanel(database);
        
        this.sourcesDisplay.innerHTML = `
            <div class="archive-placeholder">
                <div class="placeholder-icon" style="animation: pulse-icon 1.5s infinite;">📚</div>
                <p>Searching the archives...</p>
            </div>
        `;
        
        const responseDiv = this.addAssistantMessage(database, '', true);
        const textDiv = responseDiv.querySelector('.message-text');
        const sourcesDiv = responseDiv.querySelector('.message-sources');
        
        textDiv.innerHTML = this.createThinkingAnimation(database);
        let firstToken = true;
        this.currentSources = [];
        
        try {
            const provider = this.providerSelect.value || 'anthropic';
            const model = this.modelSelect.value || '';
            const enhancedMode = this.enhancedModeToggle.checked;
            const answerLength = parseInt(this.answerLengthSlider.value) || 500;
            const quoteCount = parseInt(this.quoteCountSlider.value) || 5;
            
            const response = await fetch('/api/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    question,
                    database,
                    provider,
                    model,
                    enhanced_mode: enhancedMode,
                    answer_length: answerLength,
                    quote_count: quoteCount
                })
            });
            
            if (!response.ok) {
                throw new Error('Failed to get response from server');
            }
            
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';
            
            while (true) {
                const {done, value} = await reader.read();
                if (done) break;
                
                buffer += decoder.decode(value, {stream: true});
                const lines = buffer.split('\n');
                buffer = lines.pop();
                
                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        try {
                            const data = JSON.parse(line.slice(6));
                            
                            if (data.type === 'token') {
                                if (firstToken) {
                                    textDiv.innerHTML = '';
                                    textDiv.classList.add('streaming');
                                    firstToken = false;
                                }
                                textDiv.textContent += data.data;
                                this.scrollToBottom();
                            } else if (data.type === 'sources') {
                                const sourceIds = data.data;
                                const workLinks = this.getWorkLinks(sourceIds, database);
                                sourcesDiv.innerHTML = '📚 Sources: ' + workLinks;
                                
                                if (data.positions) {
                                    this.currentSources = data.positions;
                                    this.displaySources(data.positions);
                                }
                            } else if (data.type === 'done') {
                                textDiv.classList.remove('streaming');
                                this.addDownloadButton(responseDiv, question);
                                this.hideKnowledgePanel();
                            }
                        } catch (e) {
                            console.error('Error parsing SSE data:', e);
                        }
                    }
                }
            }
        } catch (error) {
            textDiv.textContent = 'Error: ' + error.message;
            textDiv.classList.remove('streaming');
            this.hideKnowledgePanel();
        } finally {
            this.sendButton.disabled = false;
            this.uploadButton.disabled = false;
        }
    }
    
    getWorkLinks(sourceIds, database) {
        const seenWorks = new Set();
        const links = [];
        
        for (const id of sourceIds) {
            let workPrefix = id.split('-')[0];
            if (database === 'freud' || database.startsWith('freud')) {
                workPrefix = 'FREUD';
            } else if (database === 'jung') {
                workPrefix = 'JUNG';
            }
            
            if (seenWorks.has(workPrefix)) continue;
            seenWorks.add(workPrefix);
            
            const work = this.workLinks[workPrefix];
            if (work) {
                links.push(`<a href="#" class="source-link" onclick="workshop.openReader('${workPrefix}'); return false;">${work.title}</a>`);
            }
        }
        
        return links.length > 0 ? links.join(', ') : sourceIds.slice(0, 3).join(', ');
    }
    
    createReaderModal() {
        this.readerModal = document.createElement('div');
        this.readerModal.id = 'reader-modal';
        this.readerModal.className = 'reader-modal';
        this.readerModal.innerHTML = `
            <div class="reader-container">
                <div class="reader-header">
                    <h2 class="reader-title">Loading...</h2>
                    <div class="reader-controls">
                        <button class="reader-btn" id="reader-font-decrease">A-</button>
                        <button class="reader-btn" id="reader-font-increase">A+</button>
                        <button class="reader-close" id="reader-close">&times;</button>
                    </div>
                </div>
                <div class="reader-search">
                    <input type="text" id="reader-search-input" placeholder="Search in text...">
                    <button class="reader-btn" id="reader-search-btn">Find</button>
                    <span id="reader-search-count"></span>
                </div>
                <div class="reader-content" id="reader-content">
                    <div class="reader-loading">Loading work...</div>
                </div>
            </div>
        `;
        document.body.appendChild(this.readerModal);
        
        document.getElementById('reader-close').addEventListener('click', () => this.closeReader());
        document.getElementById('reader-font-increase').addEventListener('click', () => this.adjustReaderFont(1.1));
        document.getElementById('reader-font-decrease').addEventListener('click', () => this.adjustReaderFont(0.9));
        document.getElementById('reader-search-btn').addEventListener('click', () => this.searchInReader());
        document.getElementById('reader-search-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.searchInReader();
        });
        
        this.readerModal.addEventListener('click', (e) => {
            if (e.target === this.readerModal) this.closeReader();
        });
        
        this.readerFontSize = 1.1;
    }
    
    async openReader(workId, searchText = null) {
        this.readerModal.style.display = 'flex';
        const content = document.getElementById('reader-content');
        const title = document.getElementById('reader-title');
        
        content.innerHTML = '<div class="reader-loading">Loading work...</div>';
        
        try {
            const response = await fetch(`/api/work/${workId}`);
            const data = await response.json();
            
            if (data.error) {
                content.innerHTML = `<div class="reader-error">Work not available: ${data.error}</div>`;
                return;
            }
            
            document.querySelector('.reader-title').textContent = data.title;
            
            const formattedText = data.text
                .split('\n\n')
                .map(p => `<p>${this.escapeHtml(p)}</p>`)
                .join('');
            
            content.innerHTML = formattedText;
            content.style.fontSize = `${this.readerFontSize}em`;
            
            if (searchText) {
                document.getElementById('reader-search-input').value = searchText;
                this.searchInReader();
            }
        } catch (error) {
            content.innerHTML = `<div class="reader-error">Error loading work: ${error.message}</div>`;
        }
    }
    
    closeReader() {
        this.readerModal.style.display = 'none';
    }
    
    adjustReaderFont(factor) {
        this.readerFontSize *= factor;
        this.readerFontSize = Math.max(0.8, Math.min(2.5, this.readerFontSize));
        document.getElementById('reader-content').style.fontSize = `${this.readerFontSize}em`;
    }
    
    searchInReader() {
        const searchText = document.getElementById('reader-search-input').value.trim();
        if (!searchText) return;
        
        const content = document.getElementById('reader-content');
        const text = content.innerHTML;
        
        const cleanText = text.replace(/<mark[^>]*>(.*?)<\/mark>/gi, '$1');
        
        const regex = new RegExp(`(${searchText.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
        const highlighted = cleanText.replace(regex, '<mark class="search-highlight">$1</mark>');
        
        content.innerHTML = highlighted;
        
        const matches = content.querySelectorAll('.search-highlight');
        document.getElementById('reader-search-count').textContent = `${matches.length} found`;
        
        if (matches.length > 0) {
            matches[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }
    
    createThinkingAnimation(database) {
        const config = this.thinkerConfig[database] || this.thinkerConfig.freud;
        
        // Get position statements for scrolling marquee
        const positions = this.bottomPositions || [];
        const marqueeStatements = positions.slice(0, 20).map(p => 
            `<div class="position-statement">${this.escapeHtml(p.text)}</div>`
        ).join('');
        
        // Duplicate for seamless loop
        const doubledStatements = marqueeStatements + marqueeStatements;
        
        return `
            <div class="thinking-animation">
                <div class="orbit-container">
                    <div class="sun"></div>
                    <div class="orbit-path">
                        <div class="freud-head">${config.emoji}</div>
                    </div>
                </div>
                <div class="thinking-text">${config.name} is contemplating...</div>
                <div class="position-marquee">
                    <div class="position-marquee-content">
                        ${doubledStatements || '<div class="position-statement">Loading philosophical positions...</div>'}
                    </div>
                </div>
            </div>
        `;
    }
    
    addUserMessage(content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message message-user';
        
        messageDiv.innerHTML = `
            <div class="message-bubble">
                <div class="message-text">${this.escapeHtml(content)}</div>
            </div>
        `;
        
        this.messageContainer.appendChild(messageDiv);
        this.scrollToBottom();
        
        return messageDiv;
    }
    
    addAssistantMessage(database, content = '', isStreaming = false) {
        const config = this.thinkerConfig[database] || this.thinkerConfig.freud;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message message-assistant';
        
        messageDiv.innerHTML = `
            <div class="thinker-header">
                <div class="thinker-avatar ${config.color}">${config.emoji}</div>
                <span class="thinker-name">${config.name}</span>
            </div>
            <div class="message-bubble">
                <div class="message-text">${content}</div>
                <div class="message-sources"></div>
            </div>
        `;
        
        this.messageContainer.appendChild(messageDiv);
        this.scrollToBottom();
        
        return messageDiv;
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    addDownloadButton(messageDiv, userQuestion) {
        const bubble = messageDiv.querySelector('.message-bubble');
        const buttonContainer = document.createElement('div');
        buttonContainer.className = 'download-buttons';
        
        const downloadMdBtn = document.createElement('button');
        downloadMdBtn.className = 'download-btn';
        downloadMdBtn.textContent = '💾 Markdown';
        downloadMdBtn.onclick = () => this.downloadExchange(messageDiv, userQuestion, 'md');
        
        const downloadTxtBtn = document.createElement('button');
        downloadTxtBtn.className = 'download-btn';
        downloadTxtBtn.textContent = '💾 Text';
        downloadTxtBtn.onclick = () => this.downloadExchange(messageDiv, userQuestion, 'txt');
        
        buttonContainer.appendChild(downloadMdBtn);
        buttonContainer.appendChild(downloadTxtBtn);
        bubble.appendChild(buttonContainer);
    }
    
    downloadExchange(messageDiv, userQuestion, format = 'md') {
        const assistantText = messageDiv.querySelector('.message-text').textContent;
        const sources = messageDiv.querySelector('.message-sources').textContent;
        const thinkerName = messageDiv.querySelector('.thinker-name')?.textContent || 'Thinker';
        
        const date = new Date().toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        
        let content, mimeType, extension;
        
        if (format === 'txt') {
            content = `CONVERSATION WITH ${thinkerName.toUpperCase()}
Date: ${date}

================================================================================

YOU:
${userQuestion}

--------------------------------------------------------------------------------

${thinkerName.toUpperCase()}:
${assistantText}

--------------------------------------------------------------------------------

${sources}

================================================================================

Generated by FreudGPT - The Thinker's Workshop
`;
            mimeType = 'text/plain';
            extension = 'txt';
        } else {
            content = `# Conversation with ${thinkerName}
Date: ${date}

## Exchange

**You:** ${userQuestion}

**${thinkerName}:** ${assistantText}

**${sources}**

---

*Generated by FreudGPT - The Thinker's Workshop*
`;
            mimeType = 'text/markdown';
            extension = 'md';
        }
        
        const blob = new Blob([content], {type: mimeType});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${thinkerName.toLowerCase()}-conversation-${Date.now()}.${extension}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
    
    scrollToBottom() {
        this.messageContainer.scrollTop = this.messageContainer.scrollHeight;
    }
    
    clearChat() {
        if (this.messageContainer.children.length === 0) {
            return;
        }
        
        const confirmClear = confirm('Clear the entire conversation?');
        if (confirmClear) {
            this.messageContainer.innerHTML = '';
            this.sourcesDisplay.innerHTML = `
                <div class="archive-placeholder">
                    <div class="placeholder-icon">📖</div>
                    <p>Source texts will appear here as the thinker responds...</p>
                    <p class="placeholder-hint">Watch the original passages that inform each answer</p>
                </div>
            `;
            this.showWelcomeMessage();
        }
    }
    
    downloadCompleteChat(format = 'md') {
        const messages = this.messageContainer.querySelectorAll('.message');
        
        if (messages.length === 0 || this.messageContainer.querySelector('.empty-state')) {
            alert('No conversation to download');
            return;
        }
        
        const exchanges = [];
        let currentExchange = null;
        
        messages.forEach(msg => {
            if (msg.classList.contains('message-user')) {
                if (currentExchange) {
                    exchanges.push(currentExchange);
                }
                currentExchange = {
                    question: msg.querySelector('.message-text').textContent,
                    answer: '',
                    sources: '',
                    thinker: ''
                };
            } else if (msg.classList.contains('message-assistant') && currentExchange) {
                currentExchange.answer = msg.querySelector('.message-text').textContent;
                const sourcesElement = msg.querySelector('.message-sources');
                currentExchange.sources = sourcesElement ? sourcesElement.textContent : '';
                currentExchange.thinker = msg.querySelector('.thinker-name')?.textContent || 'Thinker';
            }
        });
        
        if (currentExchange) {
            exchanges.push(currentExchange);
        }
        
        if (exchanges.length === 0) {
            alert('No complete exchanges to download');
            return;
        }
        
        const date = new Date().toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
        
        let content, mimeType, extension;
        
        if (format === 'txt') {
            content = `COMPLETE WORKSHOP SESSION
Date: ${date}
Total Exchanges: ${exchanges.length}

${'='.repeat(80)}

`;
            exchanges.forEach((exchange, index) => {
                content += `EXCHANGE ${index + 1} - with ${exchange.thinker}

YOU:
${exchange.question}

${'-'.repeat(80)}

${exchange.thinker.toUpperCase()}:
${exchange.answer}

${'-'.repeat(80)}

${exchange.sources}

${'='.repeat(80)}

`;
            });
            
            content += `
Generated by FreudGPT - The Thinker's Workshop`;
            
            mimeType = 'text/plain';
            extension = 'txt';
        } else {
            content = `# Complete Workshop Session
Date: ${date}  
Total Exchanges: ${exchanges.length}

---

`;
            exchanges.forEach((exchange, index) => {
                content += `## Exchange ${index + 1} - with ${exchange.thinker}

**You:** ${exchange.question}

**${exchange.thinker}:** ${exchange.answer}

**${exchange.sources}**

---

`;
            });
            
            content += `
*Generated by FreudGPT - The Thinker's Workshop*`;
            
            mimeType = 'text/markdown';
            extension = 'md';
        }
        
        const blob = new Blob([content], {type: mimeType});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `workshop-session-${Date.now()}.${extension}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
}

let workshop;
document.addEventListener('DOMContentLoaded', () => {
    workshop = new ThinkerWorkshop();
});
