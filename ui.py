import streamlit as st 
from agno.agent import Agent 
from agno.tools.youtube import YouTubeTools
from agno.models.groq import Groq 
from dotenv import load_dotenv 
# adding the database 
from agno.db.sqlite import SqliteDb

load_dotenv()

db=SqliteDb(db_file="agno.db")
def yt_agent():
    return Agent(   
        name="Youtube Vedio analyzer",
        db=db,
        add_history_to_context=True,
        model=Groq(id="openai/gpt-oss-120b"),
        tools=[YouTubeTools()],
        markdown=True,
        add_datetime_to_context=True,
        instructions = ["give a good format ans and analyze the entire data of that vedio"]

    )

st.set_page_config(
    page_title="Youtube Vidio Analyzer",
    layout="centered"
)
st.title("🎥 AI Youtube Vedio Analyzer")

# cache - fast acess,temparary storage =>most feq accessed 
@st.cache_resource
def get_agent():
    return yt_agent()

agent=get_agent()

vedio_url = st.text_input("Enter Youtube Video Link",placeholder="https://youtu.be/example")
btn=st.button("analyze vedio",type="primary")

if vedio_url and btn:
    with st.spinner("Analyzing vedio..."):
        response=agent.run(
            f"Analyze this video: {vedio_url}"
        )
    st.markdown("Report the vedio")
    st.markdown(response.content)