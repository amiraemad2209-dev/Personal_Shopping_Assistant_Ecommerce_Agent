// =========================================================
// CONFIGURATION
// =========================================================

const API_URL = "http://127.0.0.1:5000/chat";


// =========================================================
// USER & THREAD
// =========================================================

// For now we use a fixed user.
// Later we can connect this to login/authentication.

const userId = "customer_456";

let threadId = createThreadId();


// =========================================================
// DOM ELEMENTS
// =========================================================

const messagesContainer =
    document.getElementById("messages");

const messageInput =
    document.getElementById("messageInput");

const sendButton =
    document.getElementById("sendButton");

const welcome =
    document.getElementById("welcome");

const chatHistory =
    document.getElementById("chatHistory");

const newChatButton =
    document.getElementById("newChatButton");

const headerNewChat =
    document.getElementById("headerNewChat");

const chatSearch =
    document.getElementById("chatSearch");


// =========================================================
// INITIALIZATION
// =========================================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        setupSuggestions();

        setupInput();

        setupNewChatButtons();

        loadChatHistory();

        messageInput.focus();

    }
);


// =========================================================
// CREATE THREAD ID
// =========================================================

function createThreadId() {

    return (
        "thread_" +
        Date.now() +
        "_" +
        Math.random()
            .toString(36)
            .substring(2, 8)
    );
}


// =========================================================
// INPUT SETUP
// =========================================================

function setupInput() {

    messageInput.addEventListener(
        "input",
        autoResize
    );

    messageInput.addEventListener(
        "keydown",
        handleInputKey
    );

    sendButton.addEventListener(
        "click",
        sendMessage
    );
}


function autoResize() {

    messageInput.style.height = "auto";

    messageInput.style.height =
        Math.min(
            messageInput.scrollHeight,
            130
        ) + "px";
}


function handleInputKey(event) {

    if (
        event.key === "Enter" &&
        !event.shiftKey
    ) {

        event.preventDefault();

        sendMessage();

    }

}


// =========================================================
// SUGGESTIONS
// =========================================================

function setupSuggestions() {

    const suggestions =
        document.querySelectorAll(
            ".suggestion-card"
        );

    suggestions.forEach(
        button => {

            button.addEventListener(
                "click",
                () => {

                    const message =
                        button.dataset.message;

                    messageInput.value =
                        message;

                    autoResize();

                    sendMessage();

                }
            );

        }
    );
}


// =========================================================
// SEND MESSAGE
// =========================================================

async function sendMessage() {

    const message =
        messageInput.value.trim();


    if (!message) {
        return;
    }


    hideWelcome();

    addUserMessage(message);

    messageInput.value = "";

    autoResize();

    setLoading(true);

    const typingId =
        showTyping();


    try {

        console.log(
            "Sending message:",
            message
        );

        console.log(
            "User:",
            userId
        );

        console.log(
            "Thread:",
            threadId
        );


        const response =
            await fetch(
                API_URL,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        message: message,
                        user_id: userId,
                        thread_id: threadId
                    })
                }
            );


        const data =
            await response.json();


        console.log(
            "Response status:",
            response.status
        );

        console.log(
            "Response data:",
            data
        );


        removeTyping(
            typingId
        );


        if (!response.ok) {

            console.error(
                "API Error:",
                data
            );


            addAssistantMessage(
                data.details ||
                data.error ||
                "Something went wrong."
            );


            return;
        }


        // =================================================
        // AI RESPONSE
        // =================================================

        console.log(
            "Assistant answer:",
            data.answer
        );


        addAssistantMessage(
            data.answer
        );


        // =================================================
        // DEBUG UI
        // =================================================

        console.log(
            "MESSAGE ADDED TO UI"
        );


        console.log(
            "Messages container:",
            messagesContainer.innerHTML
        );


        // =================================================
        // SAVE CHAT
        // =================================================

        saveCurrentChat(
            message
        );

    }

    catch (error) {

        console.error(
            "Connection Error:",
            error
        );


        removeTyping(
            typingId
        );


        addAssistantMessage(
            "I couldn't connect to the AI assistant. " +
            "Please make sure the Flask server is running."
        );

    }

    finally {

        setLoading(
            false
        );

        messageInput.focus();

    }

}


// =========================================================
// USER MESSAGE
// =========================================================

function addUserMessage(text) {

    const message =
        document.createElement("div");

    message.className =
        "message user-message";


    const content =
        document.createElement("div");

    content.className =
        "message-content";


    const bubble =
        document.createElement("div");

    bubble.className =
        "bubble";


    bubble.textContent =
        text;


    content.appendChild(
        bubble
    );


    message.appendChild(
        content
    );


    messagesContainer.appendChild(
        message
    );


    scrollToBottom();

}


// =========================================================
// ASSISTANT MESSAGE
// =========================================================

function addAssistantMessage(text) {

    const message =
        document.createElement("div");

    message.className =
        "message assistant-message";


    const avatar =
        document.createElement("div");

    avatar.className =
        "message-avatar";

    avatar.textContent =
        "✦";


    const content =
        document.createElement("div");

    content.className =
        "message-content";


    const sender =
        document.createElement("div");

    sender.className =
        "sender";

    sender.textContent =
        "ShopAI";


    const bubble =
        document.createElement("div");

    bubble.className =
        "bubble";


    bubble.innerHTML =
        formatAssistantText(text);


    content.appendChild(
        sender
    );


    content.appendChild(
        bubble
    );


    message.appendChild(
        avatar
    );


    message.appendChild(
        content
    );


    messagesContainer.appendChild(
        message
    );


    scrollToBottom();

}


// =========================================================
// FORMAT AI RESPONSE
// =========================================================

function formatAssistantText(text) {

    if (!text) {
        return "";
    }


    let formatted =
        escapeHTML(text);


    // Bold
    formatted =
        formatted.replace(
            /\*\*(.*?)\*\*/g,
            "<strong>$1</strong>"
        );


    // Bullet points
    formatted =
        formatted.replace(
            /^\s*[-•]\s+(.*)$/gm,
            "<li>$1</li>"
        );


    // Wrap consecutive list items
    formatted =
        formatted.replace(
            /(<li>.*?<\/li>)+/gs,
            match => {

                return (
                    "<ul>" +
                    match +
                    "</ul>"
                );

            }
        );


    // New lines
    formatted =
        formatted.replace(
            /\n/g,
            "<br>"
        );


    return formatted;

}


// =========================================================
// ESCAPE HTML
// =========================================================

function escapeHTML(text) {

    const div =
        document.createElement(
            "div"
        );


    div.textContent =
        text;


    return div.innerHTML;

}


// =========================================================
// TYPING INDICATOR
// =========================================================

function showTyping() {

    const id =
        "typing_" + Date.now();


    const message =
        document.createElement("div");


    message.className =
        "message assistant-message";


    message.id =
        id;


    message.innerHTML = `

        <div class="message-avatar">
            ✦
        </div>

        <div class="message-content">

            <div class="sender">
                ShopAI
            </div>

            <div class="bubble">

                <div class="typing-bubble">

                    <span class="typing-dot"></span>

                    <span class="typing-dot"></span>

                    <span class="typing-dot"></span>

                </div>

            </div>

        </div>

    `;


    messagesContainer.appendChild(
        message
    );


    scrollToBottom();


    return id;

}


function removeTyping(id) {

    const element =
        document.getElementById(id);


    if (element) {

        element.remove();

    }

}


// =========================================================
// LOADING STATE
// =========================================================

function setLoading(isLoading) {

    sendButton.disabled =
        isLoading;


    messageInput.disabled =
        isLoading;

}


// =========================================================
// HIDE WELCOME
// =========================================================

function hideWelcome() {

    if (welcome) {

        welcome.style.display =
            "none";

    }

}


// =========================================================
// NEW CHAT
// =========================================================

function setupNewChatButtons() {

    newChatButton.addEventListener(
        "click",
        startNewChat
    );


    headerNewChat.addEventListener(
        "click",
        startNewChat
    );

}


function startNewChat() {

    threadId =
        createThreadId();


    messagesContainer.innerHTML =
        "";


    // Create welcome again

    const welcomeElement =
        document.createElement("div");


    welcomeElement.className =
        "welcome";


    welcomeElement.innerHTML = `

        <div class="welcome-icon">
            ✦
        </div>

        <h2>
            Your Personal Shopping Assistant
        </h2>

        <p>
            Find the right products, compare options,
            understand reviews, and build smart shopping plans.
        </p>

        <div class="suggestion-grid">

            <button
                class="suggestion-card"
                data-message="What laptop do you recommend for me?"
            >

                <div class="suggestion-icon">
                    💻
                </div>

                <div class="suggestion-content">

                    <strong>
                        Recommend a laptop
                    </strong>

                    <span>
                        Find the best laptop for my needs
                    </span>

                </div>

                <span class="arrow">
                    →
                </span>

            </button>


            <button
                class="suggestion-card"
                data-message="Compare two laptops for me"
            >

                <div class="suggestion-icon">
                    ⚖️
                </div>

                <div class="suggestion-content">

                    <strong>
                        Compare products
                    </strong>

                    <span>
                        Compare products and features
                    </span>

                </div>

                <span class="arrow">
                    →
                </span>

            </button>


            <button
                class="suggestion-card"
                data-message="What should I buy for a gaming setup?"
            >

                <div class="suggestion-icon">
                    🛒
                </div>

                <div class="suggestion-content">

                    <strong>
                        Build a shopping plan
                    </strong>

                    <span>
                        Get a complete shopping list
                    </span>

                </div>

                <span class="arrow">
                    →
                </span>

            </button>


            <button
                class="suggestion-card"
                data-message="What do customers say about this product?"
            >

                <div class="suggestion-icon">
                    ⭐
                </div>

                <div class="suggestion-content">

                    <strong>
                        Check reviews
                    </strong>

                    <span>
                        Understand customer opinions
                    </span>

                </div>

                <span class="arrow">
                    →
                </span>

            </button>

        </div>

    `;


    messagesContainer.appendChild(
        welcomeElement
    );


    // Reconnect suggestion buttons

    setupSuggestions();


    messageInput.value =
        "";


    autoResize();


    messageInput.focus();

}


// =========================================================
// SCROLL
// =========================================================

function scrollToBottom() {

    const container =
        document.getElementById(
            "chatContainer"
        );


    setTimeout(
        () => {

            container.scrollTo({

                top:
                    container.scrollHeight,

                behavior:
                    "smooth"

            });

        },
        50
    );

}


// =========================================================
// LOCAL CHAT HISTORY
// =========================================================

function saveCurrentChat(firstMessage) {

    const chats =
        JSON.parse(
            localStorage.getItem(
                "shopai_chats"
            ) || "[]"
        );


    const existing =
        chats.find(
            chat =>
                chat.threadId ===
                threadId
        );


    if (!existing) {

        chats.unshift({

            threadId:
                threadId,

            title:
                firstMessage,

            createdAt:
                new Date().toISOString()

        });

    }


    localStorage.setItem(

        "shopai_chats",

        JSON.stringify(
            chats.slice(0, 20)
        )

    );


    loadChatHistory();

}


// =========================================================
// LOAD CHAT HISTORY
// =========================================================

function loadChatHistory() {

    const chats =
        JSON.parse(
            localStorage.getItem(
                "shopai_chats"
            ) || "[]"
        );


    chatHistory.innerHTML =
        "";


    chats.forEach(
        chat => {

            const item =
                document.createElement(
                    "div"
                );


            item.className =
                "chat-item";


            if (
                chat.threadId ===
                threadId
            ) {

                item.classList.add(
                    "active"
                );

            }


            item.innerHTML = `

                <span class="chat-item-icon">
                    💬
                </span>

                <span class="chat-item-text">
                    ${escapeHTML(chat.title)}
                </span>

            `;


            item.addEventListener(
                "click",
                () => {

                    loadChat(
                        chat.threadId
                    );

                }
            );


            chatHistory.appendChild(
                item
            );

        }
    );

}


// =========================================================
// LOAD CHAT
// =========================================================

function loadChat(id) {

    threadId =
        id;


    messagesContainer.innerHTML =
        "";


    addAssistantMessage(

        "This conversation is connected to thread: " +
        id +
        ". Continue asking me anything."

    );


    loadChatHistory();


    messageInput.focus();

}


// =========================================================
// CHAT SEARCH
// =========================================================

chatSearch.addEventListener(
    "input",
    () => {

        const search =
            chatSearch.value
                .toLowerCase()
                .trim();


        const items =
            document.querySelectorAll(
                ".chat-item"
            );


        items.forEach(
            item => {

                const text =
                    item.textContent
                        .toLowerCase();


                item.style.display =
                    text.includes(search)
                        ? "flex"
                        : "none";

            }
        );

    }
);