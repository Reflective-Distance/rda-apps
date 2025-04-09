import threading
import streamlit as st
import streamlit_launcher as sl
import datetime


def main():
    print("Running main()")
    
    st.write("Welcome!")
    btn_click = st.button("Press me")

    if btn_click:
        st.write(f"Button Clicked at {datetime.datetime.now()}")


def initializer():
    print("Running initializer()")


if __name__ == "__main__":
    name = threading.current_thread().name
    id = threading.current_thread().ident
    print(f"Starting Streamlit Server on [{name}] ID: [{id}]");
    
    sl.launch_streamlit(main, initializer)
