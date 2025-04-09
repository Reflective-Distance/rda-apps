import inspect
import os
import threading
from streamlit import config as st_config
from streamlit.web.bootstrap import run as st_run

DEFAULT_PORT = os.environ.get("PORT", 8501)
HEADLESS = True


def launch_streamlit(
    main_callback,
    initializer_callback=None,
    port=DEFAULT_PORT,
    headless=HEADLESS,
    config_options={},
):
    # This launch allows streamlit to be started via the python main or via streamlit run
    # and allows the user to pass in a callback to initialize the app

    if _launched_from_python_main():
        # The server was called from the python main
        # Initialize if the callback is defined
        # and run the server

        if initializer_callback:
            initializer_callback()

        _set_initialized()

        main_callback_filename = inspect.getsourcefile(main_callback)

        # Set the port
        st_config.set_option("server.port", port)

        # Set the headless flag
        st_config.set_option("server.headless", headless)

        # Set the config options
        for key, value in config_options.items():
            st_config.set_option(key, value)

        # Start the Streamlit server (blocking)
        st_run(main_callback_filename, args=[], flag_options=[], is_hello=False)

    else:
        # The server was called by streamlit run
        # The server is already running, so no need to launch

        # Call the initializer callback if it is not initialized
        # The first time the server is called, the initialzied flag is False

        if not _initialized():
            if initializer_callback:
                initializer_callback()

            _set_initialized()

        # Call the main callback
        main_callback()


def _launched_from_python_main():
    return threading.current_thread() is threading.main_thread()


def _initialized():
    # Use and environment variable so that you can change the UI code
    # and see the changes without restarting the server
    # Local variables would be wiped out when the server is restarted
    # Good for development

    return os.environ.get("STREAMLIT_INITIALIZED", "0") == "1"


def _set_initialized(flag=True):
    os.environ["STREAMLIT_INITIALIZED"] = "1" if flag else "0"
