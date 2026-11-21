# Lab 3: Chatbot page
# TODO: Rename this file to fit your page. Keep the number at the front.
#
# A chatbot built with Pydantic AI (see the Pydantic AI pages on Canvas).
# It should:
#   - use a Pydantic AI Agent with instructions that fit your project's theme (no tools yet)
#   - use Streamlit's chat elements: st.chat_message and st.chat_input
#   - remember the conversation (message_history, saved in st.session_state)
#   - use try/except so an error shows a message instead of crashing the page
#   - stay on theme, without using any API or external data
#
# Your Gemini API key goes in .streamlit/secrets.toml as GOOGLE_API_KEY.

import streamlit as st
from pydantic_ai import Agent

st.set_page_config(page_title="HR Buddy", page_icon="👨‍🔬")

research_agent = Agent(
    "google:gemini-3.5-flash-lite",
    instructions="""
    You are Health Research Buddy, nicknamed HR Buddy, a friendly assistant for undergraduate
    students interested in biomedical research and pre-med.

    Help users understand topics such as neuroscience, genetics,
    cancer biology, immunology, and biomedical engineering.

    Explain scientific concepts in an approachable way.
    Give advice about undergraduate research and medical careers.

    Keep responses relatively short, clear, and conversational.

    Do not claim to have access to NIH project data, current
    research openings, specific funding amounts, or external
    databases. You cannot search for actual research labs.

    Stay focused on biomedical research, science, and pre-med topics.
    """
)
st.header("🔬HR Buddy🔬", divider="violet")
st.write("Your AI assistant for exploring biomedical research!")
st.badge("Pre-Med", color="blue")
st.badge("Biomedical Research", color="green")

if "message_history" not in st.session_state:
    st.session_state.message_history = []
if "agent_history" not in st.session_state:
    st.session_state.agent_history = []

for message in st.session_state.message_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Ask me about biomedical research opportunities...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.message_history.append({"role": "user", "content": user_input})
    try:
        result = research_agent.run_sync(
            user_input,
            message_history=st.session_state.agent_history
        )
        response = result.output
        with st.chat_message("assistant"):
            st.write(response)
        st.session_state.message_history.append({
            "role": "assistant",
            "content": response
        })
        st.session_state.agent_history = result.all_messages()
    except Exception as error:
        st.error("Sorry, something went wrong! Please try again!")
        st.write(str(error))

if st.button("Clear Chat"):
    st.session_state.message_history=[]
    st.session_state.agent_history = []
    st.rerun()

