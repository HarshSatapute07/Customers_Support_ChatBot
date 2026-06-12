from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq
import os

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Customer Support Assistant",
    page_icon="🎧",
    layout="centered"
)

# Check API Key
if not os.getenv("GROQ_API_KEY"):
    st.error("GROQ_API_KEY not found in .env file")
    st.stop()

# Initialize LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.2
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": """
Hello! 👋

Welcome to Customer Support Assistant.

I can help you with:
• Product Information
• Product Features
• Product Pricing
• Product Availability
• Product Warranty
• Product Returns and Refunds
• Product Usage and Troubleshooting

How may I assist you today?
"""
        }
    ]


# SIDEBAR
st.sidebar.title("📋 Chat Options")

# Show Chat History
if st.sidebar.checkbox("Show Chat History"):

    st.sidebar.subheader("Conversation History")

    for msg in st.session_state.messages:

        if msg["role"] == "user":
            st.sidebar.markdown(
                f"🧑 **User:** {msg['content']}"
            )

# Clear History Button
if st.sidebar.button("🗑️ Clear Chat History"):

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": """
Hello! 👋

Welcome to Customer Support Assistant.

How may I assist you today?
"""
        }
    ]

    st.rerun()


# MAIN PAGE
st.title("🎧 Customer Support Assistant")

st.caption(
    "Helping customers with products, pricing, refunds, warranties and troubleshooting."
)

# Display chat messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
user_prompt = st.chat_input(
    "Describe your issue or ask a product-related question..."
)

if user_prompt:

    # Show User Message
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Save User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    try:

        # Generate Response
        response = llm.invoke(
            [
                {
                    "role": "system",
                    "content": """
You are a Customer Product Support Assistant.

Your job is ONLY to answer questions related to:

- Products
- Product Features
- Product Pricing
- Product Availability
- Product Warranty
- Product Returns and Refunds
- Product Usage
- Product Troubleshooting

If the user asks anything unrelated to products
(such as coding, programming, politics, sports,
movies, education, science, entertainment, etc.)
reply exactly:

Sorry, I can only assist with product-related customer support questions.

Do not answer non-product questions.
"""
                },
                *st.session_state.messages
            ]
        )

        assistant_response = response.content

        # Show Assistant Response
        with st.chat_message("assistant"):
            st.markdown(assistant_response)

        # Save Assistant Response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": assistant_response
            }
        )

    except Exception as e:
        st.error(f"Error: {str(e)}")