import streamlit as st
import uuid
import warnings

from chat import app
from langchain_core.messages import HumanMessage, AIMessage

warnings.simplefilter("ignore")


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------------------------------
# GET ALL THREADS FROM POSTGRESQL
# --------------------------------------------------

def get_all_threads():

    threads = set()

    try:
        checkpoints = app.checkpointer.list(None)

        for checkpoint in checkpoints:
            thread_id = checkpoint.config["configurable"]["thread_id"]
            threads.add(thread_id)

    except Exception as e:
        st.error(f"Could not load conversations: {e}")

    return list(threads)


# --------------------------------------------------
# LOAD CONVERSATION
# --------------------------------------------------

def load_conversation(thread_id):

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    state = app.get_state(config)

    if state and state.values:
        return state.values.get("messages", [])

    return []


# --------------------------------------------------
# RESET / NEW CHAT
# --------------------------------------------------

def new_chat():

    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.messages = []


# --------------------------------------------------
# CURRENT CONFIG
# --------------------------------------------------

def get_config():

    return {
        "configurable": {
            "thread_id": st.session_state.thread_id
        }
    }


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("LANGGRAPH CHATBOT")


if st.sidebar.button(
    "➕ New Chat",
    use_container_width=True
):
    new_chat()
    st.rerun()


st.sidebar.divider()
st.sidebar.header("My Conversations")


# Get conversations directly from PostgreSQL
threads = get_all_threads()

# Remove current thread if it doesn't have messages yet
# because it has not been saved to DB.
threads = [
    thread for thread in threads
    if thread != st.session_state.thread_id
]


# Show newest first
threads.reverse()


for index, thread_id in enumerate(threads, start=1):

    if st.sidebar.button(
        f"Conversation {index}",
        key=f"conversation_{thread_id}",
        use_container_width=True
    ):

        st.session_state.thread_id = thread_id

        messages = load_conversation(thread_id)

        temp_messages = []

        for message in messages:

            if isinstance(message, HumanMessage):

                temp_messages.append({
                    "role": "user",
                    "content": message.content
                })

            elif isinstance(message, AIMessage):

                temp_messages.append({
                    "role": "assistant",
                    "content": message.content
                })

        st.session_state.messages = temp_messages

        st.rerun()


# --------------------------------------------------
# MAIN UI
# --------------------------------------------------

st.title("AI ASSISTANT")


# --------------------------------------------------
# DISPLAY MESSAGES
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

user_input = st.chat_input(
    "Enter your query here..."
)


if user_input:

    # USER MESSAGE
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })


    # ASSISTANT MESSAGE
    with st.chat_message("assistant"):

        response_text = st.write_stream(
            message.content
            for message, metadata in app.stream(
                {
                    "messages": [
                        HumanMessage(
                            content=user_input
                        )
                    ]
                },
                config=get_config(),
                stream_mode="messages"
            )
            if message.content
        )


    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text
    })