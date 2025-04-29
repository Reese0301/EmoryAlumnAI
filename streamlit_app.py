import streamlit as st
import requests
import random

# --- Langflow Flow ID and URL ---
LANGFLOW_URL = "http://127.0.0.1:7860/api/v1/run/74a40bc4-47a7-4ff8-9078-7278879d9e21"

# --- Welcome Message ---
WELCOME_MESSAGE = "Hi there! I am here to help you with patient reports. Simply paste in what you have, no need to format anything --- I will synthesize them."

# --- Thinking animations ---
thinking_messages = [
    "Processing your request...",
    "Analyzing information and generating a response...",
    "Building a thoughtful report...",
    "Calculating Financials...",
    "Synthesizing information..."
]

# --- Initialize chat ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": WELCOME_MESSAGE}]

# --- Main Page Title ---
st.title("AlumnAI: Patient Report Generator")
st.markdown(
    """
    ---
    - 🤖 I am a Chatbot designed to help you update **Patient Reports** using your latest information.
    - 🧾 Simply paste in your outdated report and new data — I'll do the rest!
    - 📤 Make sure to proof read important information such as names and numbers.
    - 🧠 For other features or tasks, refer to sidebar on the left side of the screen.
    ---
    """,
    unsafe_allow_html=True
)


# --- Sidebar Style + Suggestions ---
with st.sidebar:
    st.markdown("## 🧠 About AlumnAI")
    st.markdown("Built by the **BUS399 Mad-Libs Team**")
    
    st.markdown("### 💡 User Guide")
    st.markdown(
        "- Step 1: Gather previous patient report\n"
        "- Step 2: Gather the latest information \n"
        "- Step 3: Copy & Paste the text into the chatbox\n"
        "- Step 4: Proof read AI output and revise"
    )

    #st.markdown("---")
    #st.markdown("📬 [Send Feedback](mailto:your-email@example.com)")

    # Inside your `with st.sidebar:` block, add this:
    st.markdown("### 📝 Writing Assistant")
    st.markdown(
        """
        <style>
        div.stButton > button:first-child {
            background-color: #FF4B4B;
            color: white;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    if st.button("Generate AI Feedback"):
        # Make sure there’s at least one assistant message
        assistant_messages = [m for m in st.session_state.messages if m["role"] == "assistant"]
        if assistant_messages:
            last_output = assistant_messages[-1]["content"]

            # Send to Feedback AI API
            try:
                feedback_response = requests.post(
                    "http://127.0.0.1:7860/api/v1/run/22faa234-90cb-47f2-a62d-ac70607d0b88",
                    headers={"Content-Type": "application/json"},
                    json={
                        "input_value": last_output,
                        "output_type": "chat",
                        "input_type": "chat"
                    }
                )
                feedback_response.raise_for_status()
                feedback_data = feedback_response.json()
                feedback_text = feedback_data["outputs"][0]["outputs"][0]["results"]["message"]["text"]

                # Add feedback as an assistant-style message
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"**AI Feedback:**\n\n{feedback_text}"
                })
                st.rerun()  # Force refresh to show it in chat

            except Exception as e:
                st.error(f"Feedback API Error: {e}")
        else:
            st.warning("No assistant output yet. Generate a report first.")

    # DARK OVERLAY CSS LIKE YOUR FINANCE BOT
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            background-image: url(https://github.com/Reese0301/alumai/blob/main/EmoryUniSideBarImage.jpg?raw=true);
            background-size: cover;
            position: relative;
        }

        [data-testid="stSidebar"]::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);  /* Dark overlay (50% black) */
            z-index: 0;
        }

        [data-testid="stSidebar"] > div:first-child {
            position: relative;
            z-index: 1;
            padding: 20px;
        }

        [data-testid="stSidebar"] * {
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# --- Display all chat messages ---
for msg in st.session_state.messages:
    avatar = "https://github.com/Reese0301/GIS-AI-Agent/blob/main/4322991.png?raw=true" if msg["role"] == "assistant" else "https://github.com/Reese0301/GIS-AI-Agent/blob/main/FoxUser.png?raw=true"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# --- Input from user ---
if prompt := st.chat_input("Ask me anything..."):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="https://github.com/Reese0301/GIS-AI-Agent/blob/main/FoxUser.png?raw=true"):
        st.markdown(prompt)

    thinking = st.empty()
    thinking.markdown(f"💬 {random.choice(thinking_messages)}")

    # Build plain conversation text for Langflow
    full_convo = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])

    try:
        response = requests.post(
            LANGFLOW_URL,
            headers={"Content-Type": "application/json"},
            json={
                "input_value": full_convo,
                "output_type": "chat",
                "input_type": "chat"
            }
        )
        response.raise_for_status()
        data = response.json()
        reply = data["outputs"][0]["outputs"][0]["results"]["message"]["text"]

    except Exception as e:
        reply = f"❌ Error: {e}"

    thinking.empty()

    with st.chat_message("assistant", avatar="https://github.com/Reese0301/GIS-AI-Agent/blob/main/4322991.png?raw=true"):
        st.markdown(reply)


    st.session_state.messages.append({"role": "assistant", "content": reply})
