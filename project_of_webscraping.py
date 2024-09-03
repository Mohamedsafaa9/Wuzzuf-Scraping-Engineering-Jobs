
!pip install selenium pyvirtualdisplay
!apt-get update

! pip3 install  pyvirtualdisplay selenium webdriver_manager  > /dev/null

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
import pandas as pd
import time

disp = Display(visible=0, size=(800, 600))
disp.start()

driver = webdriver.Firefox()
driver.get("https://wuzzuf.net/")

wait = WebDriverWait(driver, 10)
search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='q']")))
search_box.send_keys("engineering")
search_box.send_keys(Keys.RETURN)
time.sleep(5)

job_titles_list = []
company_names_list = []
locations_list = []
dates_posted_list = []
count = 0

while True:
    time.sleep(5)

    # Get job data
    job_titles = driver.find_elements(By.CSS_SELECTOR, "h2.css-m604qf")
    company_names = driver.find_elements(By.CSS_SELECTOR, "a.css-17s97q8")
    locations = driver.find_elements(By.CSS_SELECTOR, "span.css-5wys0k")
    post_dates = driver.find_elements(By.CSS_SELECTOR, "div.css-do6t5g")

    for job, company, location, date in zip(job_titles, company_names, locations, post_dates):
        job_titles_list.append(job.text)
        company_names_list.append(company.text)
        locations_list.append(location.text)
        dates_posted_list.append(date.text)



    try:
        next_page = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-b80bsd")))
        next_page.click()
        count += 1
        print(count)
        if count ==  30:
            break
    except Exception as e:
        print("Pagination issue:", e)
        break

# Create a DataFrame and save to CSV
jobs_df = pd.DataFrame({
    'Job Title': job_titles_list,
    'Company Name': company_names_list,
    'Location': locations_list,
    'Date Posted': dates_posted_list
})

jobs_df.to_csv("wuzzuf_engineering _jobs.csv", index=False)

# Close the WebDriver
driver.quit()
disp.stop()

