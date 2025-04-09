from shared.environment import ensure_environment_initialized

ensure_environment_initialized()

import streamlit as st
from shared import logging

import utils.streamlit.streamlit_launcher as sl


logger = logging.get_app_logger()


def streamlit_main():
    logger.info("Running main()")

    st.set_page_config(
        page_title="LLM Playground",  # Sets the browser tab title
        page_icon=":wrench:",  # You can use an emoji OR a URL to an image
    )

    st.markdown("### Language Model Playground :hammer_and_wrench:")


def initializer():
    logger.info("Running initializer()")


if __name__ == "__main__":
    logger.info("Starting Streamlit Server")
    sl.launch_streamlit(streamlit_main, initializer)
