import streamlit as st
import asyncio
import time
import os
import tempfile

from agent import run_agent, get_thread_messages

from database import (
    get_user_sidebar_history,
    create_new_sidebar_thread,
    update_thread_title,
    get_or_create_user,
)

from rag.run_ingestion import ingest_document

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ShopAI",
    page_icon="✦",
    layout="wide"
)


# =========================================================
# USER
# =========================================================

if "user_id" not in st.session_state:

    username = st.sidebar.text_input(
        "Username",
        placeholder="Enter your username"
    )

    if not username:
        st.info(
            "Please enter your username to continue."
        )
        st.stop()

    st.session_state.user_id = asyncio.run(
        get_or_create_user(
            username=username
        )
    )

    st.session_state.username = username

USER_ID = st.session_state.user_id
USERNAME = st.session_state.username


# =========================================================
# DATABASE HELPERS
# =========================================================

def load_threads():
    """
    Load all chat threads belonging to the current user.
    """

    return asyncio.run(
        get_user_sidebar_history(USER_ID)
    )


def create_thread(title="New Chat"):
    """
    Create a real thread in the database.
    """

    return asyncio.run(
        create_new_sidebar_thread(
            user_id=USER_ID,
            title=title
        )
    )


# =========================================================
# SESSION STATE
# =========================================================

if "thread_id" not in st.session_state:

    threads = load_threads()

    if threads:

        st.session_state.thread_id = (
            threads[0]["thread_id"]
        )

    else:

        st.session_state.thread_id = create_thread()


if "messages" not in st.session_state:

    st.session_state.messages = []


if "threads" not in st.session_state:

    st.session_state.threads = load_threads()


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* Main background */

    .stApp {
        background-color: #0f1117;
    }


    /* Sidebar */

    section[data-testid="stSidebar"] {
        background-color: #151821;
    }


    /* Title */

    .shop-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 0;
    }


    .shop-subtitle {
        color: #9ca3af;
        margin-bottom: 25px;
    }


    /* Chat title */

    .chat-header {
        font-size: 24px;
        font-weight: 600;
        padding-bottom: 15px;
    }


    /* User info */

    .user-box {
        background-color: #1c202b;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="shop-title">✦ Shop with AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="shop-subtitle">'
        'Your Personal Shopping Assistant'
        '</div>',
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # DOCUMENT UPLOAD
    # -----------------------------------------------------

    st.markdown("### 📚 Knowledge Base")

    uploaded_file = st.file_uploader(
        "Upload a document",
        type=["pdf"]
    )

    if uploaded_file is not None:

        if (
            "uploaded_file_name"
            not in st.session_state
            or
            st.session_state.uploaded_file_name
            != uploaded_file.name
        ):

            temp_dir = tempfile.gettempdir()

            file_path = os.path.join(
                temp_dir,
                uploaded_file.name
            )

            with open(file_path, "wb") as f:
                f.write(
                    uploaded_file.getbuffer()
                )

            with st.spinner(
                "Indexing document..."
            ):

                try:

                    result = ingest_document(
                        file_path
                    )

                    st.session_state.uploaded_file_name = (
                        uploaded_file.name
                    )

                    st.success(
                        "✅ Document indexed successfully!"
                    )

                    st.caption(
                        uploaded_file.name
                    )

                except Exception as e:

                    st.error(
                        f"❌ Error indexing document: {e}"
                    )

        else:

            st.success(
                "✅ Document already indexed"
            )

            st.caption(
                uploaded_file.name
            )

        # -----------------------------------------------------
    # UPLOADED DOCUMENTS
    # -----------------------------------------------------

    if "uploaded_documents" not in st.session_state:

        st.session_state.uploaded_documents = []


    if (
        uploaded_file is not None
        and
        uploaded_file.name
        not in st.session_state.uploaded_documents
    ):

        st.session_state.uploaded_documents.append(
            uploaded_file.name
        )


    if st.session_state.uploaded_documents:

        st.markdown("#### 📄 Uploaded Documents")

        for document in st.session_state.uploaded_documents:

            st.caption(
                f"📄 {document}"
            )


    # -----------------------------------------------------
    # USER
    # -----------------------------------------------------

    # USER
    st.markdown(
        f"""
        <div class="user-box">
        👤 <strong>{USERNAME}</strong>
    </div>
    """,
        unsafe_allow_html=True
    )

    if st.button(
        "🔄 Switch User",
        use_container_width=True
        ):
        st.session_state.clear()
        st.rerun()

    # -----------------------------------------------------
    # NEW CHAT
    # -----------------------------------------------------

    if st.button(
        "＋ New Chat",
        use_container_width=True
    ):

        new_thread_id = create_thread(
            title="New Chat"
        )

        st.session_state.thread_id = new_thread_id
        st.session_state.messages = []

        st.session_state.threads = load_threads()

        st.rerun()

    st.divider()

    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    search = st.text_input(
        "🔎 Search chats",
        placeholder="Search conversations..."
    )

    st.markdown("### Recent Chats")

    # -----------------------------------------------------
    # REFRESH THREADS
    # -----------------------------------------------------

    st.session_state.threads = load_threads()

    # هنا بنعرّف threads قبل ما نستخدمها
    threads = st.session_state.threads

    # -----------------------------------------------------
    # FILTER
    # -----------------------------------------------------

    if search:

        threads = [
            thread
            for thread in threads
            if search.lower()
            in thread["title"].lower()
        ]

    # -----------------------------------------------------
    # DISPLAY THREADS
    # -----------------------------------------------------

    if not threads:

        st.caption(
            "No conversations yet."
        )

    else:

        for thread in threads:

            thread_id = thread["thread_id"]
            title = thread["title"]

            is_active = (
                thread_id ==
                st.session_state.thread_id
            )

            if is_active:

                button_label = "🟢 " + title

            else:

                button_label = "💬 " + title

            if st.button(
                button_label,
                key=f"thread_{thread_id}",
                use_container_width=True
            ):

                st.session_state.thread_id = thread_id

                st.session_state.messages = asyncio.run(
                    get_thread_messages(thread_id)
                )

                st.rerun()


# =========================================================
# MAIN AREA
# =========================================================

st.markdown(
    '<div class="chat-header">Personal Shopping Assistant</div>',
    unsafe_allow_html=True
)


st.caption(
    f"Thread: {st.session_state.thread_id}"
)


st.divider()


# =========================================================
# WELCOME
# =========================================================

if not st.session_state.messages:

    st.markdown(
        """
        ## Welcome to Shop with AI 

        I can help you:

        - 💻 Find products
        - ⚖️ Compare products
        - 🛒 Build shopping plans
        - ⭐ Understand customer reviews
        - 🔎 Search for current information
        """
    )


# =========================================================
# DISPLAY MESSAGES
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# =========================================================
# CHAT INPUT
# =========================================================

user_input = st.chat_input(
    "What are you looking for?"
)


# =========================================================
# PROCESS MESSAGE
# =========================================================

if user_input:

    # -----------------------------------------------------
    # Display user message
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):

        st.markdown(
            user_input
        )


    # -----------------------------------------------------
    # Run Agent
    # -----------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "ShopAI is thinking..."
        ):

            try:

                answer = asyncio.run(
                    run_agent(
                        user_input=user_input,
                        user_id=USER_ID,
                        thread_id=(
                            st.session_state.thread_id
                        )
                    )
                )

                st.markdown(
                    answer
                )


                # -------------------------------------------------
                # Save assistant message to current UI session
                # -------------------------------------------------

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )


                # -------------------------------------------------
                # Create title from first user message
                # -------------------------------------------------

                current_threads = load_threads()

                current_thread = next(
                    (
                        thread
                        for thread in current_threads
                        if thread["thread_id"]
                        == st.session_state.thread_id
                    ),
                    None
                )

                if (
                    current_thread
                    and current_thread["title"] == "New Chat"
                ):

                    words = user_input.strip().split()

                    title = " ".join(words[:2])

                    if len(words) > 2:
                        title += "..."

                    asyncio.run(
                        update_thread_title(
                            thread_id=(
                                st.session_state.thread_id
                            ),
                            title=title
                        )
                    )


                # -------------------------------------------------
                # Refresh sidebar
                # -------------------------------------------------

                st.session_state.threads = (
                    load_threads()
                )


            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )

                print(
                    "Streamlit Error:",
                    e
                )