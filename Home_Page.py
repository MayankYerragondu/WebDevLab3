import streamlit as st

# Title of App
st.set_page_config()
st.title("Web Development Labs 03 & 04")
st.header("Lab 3: 🧬 Pre-Med Research Lab Finder 🧬")
st.caption("Discover biomedical research happening across universities!")


if "welcome_shown" not in st.session_state:
    st.toast("Welcome to our Research Lab Finder! 👋")
    st.session_state.welcome_shown = True

# Assignment Data
# TODO: Fill out your team number, section, and team members

st.header("CS 1301")
st.subheader("Team 30, Web Development - Section A")
st.subheader("Audrey Zhang, Mayank Yerragondu", divider="green")

# TODO (optional): Add a group photo to the images folder and show it here, for example:
# st.image("images/group_photo.jpg")

#Intro
st.header("Welcome to Our Project!", divider="violet")
st.write("""
Welcome to our Pre-Med Research Lab Finder! This app helps undergraduate
students explore biomedical research opportunities by searching through
NIH-funded research projects.

Whether you're interested in neuroscience, cancer biology, genetics,
or biomedical engineering, you can explore active research projects,
discover faculty researchers, and learn about different universities.

Use the sidebar to navigate between our pages!
         """)
#Each page and its description
st.header("Explore the Website", divider="blue")
st.subheader("📊 1. Data Page 📊")
st.write("""
Explore NIH-funded biomedical research projects from universities
and research institutions. Search by research topic, filter by
university, and learn more about principal investigators, project
abstracts, and funding information.
""")

st.subheader("🤖 2. AI Chatbot 🤖")
st.write("""
Ask questions about biomedical research projects using our AI chatbot!
You can ask questions about neuroscience research at Emory University, find
institutions studying cancer biology, or explore researchers working
in specific fields, in Georgia or anywhere!
""")

#st.subheader("Lab 4 - For Later")
#st.write("Uhh we'll get there")

st.divider()
st.header("✨ Fun Features ✨", divider="rainbow")

st.write("A few extra features to make exploring research more interesting!")

col1, col2 = st.columns(2)

with col1:
    st.info("🧠 Explore Research Areas 🧠")
    st.write("Discover projects in neuroscience, genetics, cancer biology, and more.")

    st.info("🏫 University Explorer 🏫")
    st.write("See what biomedical research is happening at different universities.")

with col2:
    st.info("🔎 Find Researchers 🔎")
    st.write("Discover principal investigators and learn about their research.")

    st.info("💰 Research Funding 💰")
    st.write("Explore NIH funding information associated with different projects.")

# Interactive element
st.header("🔍 What Research Interests You? 🔍 ")

interest = st.selectbox(
    "Choose a research area to explore:",
    ["Neuroscience", "Cancer Biology", "Genetics",
     "Biomedical Engineering", "Immunology"]
)

if st.button("Explore My Interest"):
    st.success(f"Great choice! Get ready to explore {interest} research!")

st.caption("CS 1301 | Fall 2026 | Web Development Labs 03 & 04")