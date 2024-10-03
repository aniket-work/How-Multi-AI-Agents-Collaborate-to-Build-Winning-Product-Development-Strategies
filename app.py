import streamlit as st
from dotenv import load_dotenv
from graph_builder import build_graph
from ui_handler import handle_ui
import constants

load_dotenv()

st.set_page_config(page_title=constants.PAGE_TITLE, layout="wide")
st.title(constants.APP_TITLE)

query = st.text_input(constants.QUERY_PROMPT)

if st.button(constants.RUN_BUTTON):
    handle_ui(query)