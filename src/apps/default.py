from shared.environment import ensure_environment_initialized

ensure_environment_initialized()

import streamlit as st
import utils.streamlit.streamlit_launcher as sl

from shared import logging

logger = logging.get_app_logger()


def streamlit_main():
    logger.info("Running main()")

    st.set_page_config(
        layout="centered",  # Can be "centered" or "wide"
        page_title="Mono Repo",  # Sets the browser tab title
        page_icon="🤦‍♂️", 
    )

    st.markdown("### Hello :wave:")
    st.markdown("#### You forgot to override the CMD instruction when starting the Docker container.")
    
    


def initializer():
    logger.info("Running initializer()")


if __name__ == "__main__":
    logger.info("Starting Streamlit Server")
    sl.launch_streamlit(streamlit_main, initializer)
