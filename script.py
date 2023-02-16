import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import threading


list_discription = []
list_title_jobs = []
list_company_location = []
list_company_name = []
list_link_job = []
list_li = []

# Define a function that will run the Selenium driver in a thread
def run_driver(sittt):
    global driver
    driver = webdriver.Chrome()
    driver.get(sittt)


# Define a function that will get the page source of the website

def display_data():
    global list_discription, list_title_jobs, list_company_location, list_company_name, list_link_job, list_li
    for i in range(len(list_title_jobs)):
        st.markdown(f"""
                <a href="{list_link_job[i]}" class="my-2 card p-4 bg-white border rounded-lg stretched-link">
                  <div class="d-flex align-items-center">
                      <div class="mx-1 ">
                          <img src="https://raw.githubusercontent.com/lhoussaine-HSSINI/Stage/8935dbf0ed54c4ea517deecd02ba8e981de7e0bb/job-seeker.png" alt="aa" width="65" class="rounded-3">  
                      </div>
                      <div class="mx-1">
                          <div class="font-weight-bold leading-tight font-display">{list_title_jobs[i]}</div>
                          <div class="text-muted font-medium text-sm my-1">{list_company_name[i]}</div>
                          <div class="text-muted font-medium text-sm">{list_company_location[i]}</div>
                      </div>
                  </div>
            </a>
            """, unsafe_allow_html=True)


def stocke_data(list_li_1):
    global list_discription,list_title_jobs,list_company_location,list_company_name,list_link_job, list_li
    for i in range(len(list_li_1)):
        title=list_li_1[i].find_element(by=By.CSS_SELECTOR, value="div[class='css-1m4cuuf e37uo190']").text
        list_title_jobs.append(title)
        comany_location=list_li_1[i].find_element(by=By.CSS_SELECTOR, value="div[class='companyLocation']").text
        list_company_location.append(comany_location)
        try:
            company_name =list_li_1[i].find_element(by=By.CSS_SELECTOR, value="span[class='companyName']").text
        except:
            company_name=None
        list_company_name.append(company_name)
        link_job =list_li_1[i].find_element(by=By.CSS_SELECTOR, value="div[class='css-1m4cuuf e37uo190']").find_element(by=By.TAG_NAME, value='a').get_attribute("href")
        list_link_job.append(link_job)

        print(list_title_jobs)

def get_page_source():
    global driver, page_source,list_li, page_total_of_search
    page_total = driver.find_element(by=By.CLASS_NAME, value="jobsearch-JobCountAndSortPane-jobCount").text
    page_total_of_search = int([int(s) for s in re.findall(r'-?\d+\.?\d*', page_total)][-1]) // 15 + 1
    list_li = driver.find_elements(by=By.CSS_SELECTOR, value="div[class='slider_container css-g7s71f eu4oa1w0']")
    stocke_data(list_li)
    page_source = driver.page_source





# Define the Streamlit app
def app():
    global list_li
    sittt=st.text_input("give me site")
    num_times = st.number_input("Enter the number of times to retrieve the page source:", value=1, step=1)
    if st.button("submit"):
        # Start the Selenium driver in a separate thread
        driver_thread = threading.Thread(target=run_driver(sittt))
        driver_thread.start()

        # Wait for the driver to start up
        driver_thread.join()

        # Get the page source using Selenium in a separate thread
        for i in range(num_times):
            page_source_thread = threading.Thread(target=get_page_source)
            page_source_thread.start()

            # Wait for the page source to be retrieved
            page_source_thread.join()

            display_data()
            # # Display the page source in Streamlit
            # st.code(page_source)


# Run the Streamlit app
if __name__ == "__main__":
    app()
