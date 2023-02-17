import streamlit as st
from selenium import webdriver
import threading


# Define a function that will run the Selenium driver in a thread
def run_driver():
    global driver
    driver = webdriver.Chrome()
    driver.get("https://www.google.com")


# Define a function that will get the page source of the website
def get_page_source():
    global driver, page_source
    page_source = driver.page_source


# Define the Streamlit app
def app():
    num_times = st.number_input("Enter the number of times to retrieve the page source:", value=1, step=1)

    # Start the Selenium driver in a separate thread
    driver_thread = threading.Thread(target=run_driver)
    driver_thread.start()

    # Wait for the driver to start up
    driver_thread.join()

    # Get the page source using Selenium in a separate thread
    for i in range(num_times):
        page_source_thread = threading.Thread(target=get_page_source)
        page_source_thread.start()

        # Wait for the page source to be retrieved
        page_source_thread.join()

        # Display the page source in Streamlit
        st.code(page_source)


# Run the Streamlit app
if __name__ == "__main__":
    app()
