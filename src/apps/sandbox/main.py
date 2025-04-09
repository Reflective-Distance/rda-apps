from shared.environment import ensure_environment_initialized

ensure_environment_initialized()

import streamlit as st
import utils.streamlit.streamlit_launcher as sl

from shared import logging

logger = logging.get_app_logger()


def streamlit_main():
    logger.info("Running main()")

    st.set_page_config(
        layout="wide",  # Can be "centered" or "wide"
        page_title="NW Sandbox",  # Sets the browser tab title
        page_icon=":building_construction:",  # You can use an emoji OR a URL to an image
    )

    st.markdown("### Noteworthy Sandbox :building_construction:")


def initializer():
    logger.info("Running initializer()")


if __name__ == "__main__":
    logger.info("Starting Streamlit Server")
    sl.launch_streamlit(streamlit_main, initializer)
