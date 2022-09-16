import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
from keys import WEB_SCRAPING_API_KEY

def make_indeed_url(search_job, search_location=None, job_age=7):
    '''
    This function takes in 3 search parameters and inserts them into an
    indeed.com url to search for jobs in those parameters
    input:
        search_job (str): job title being searched for
        search_location (str): city, state being searched
        job_age (int): 3 or 7, max age of job posting in days
    output:
        indeed_job_url (str): url to indeed jobs of the given parameters
    '''
    job = search_job.replace(' ', '%20')
    indeed_job_url = f'https://www.indeed.com/jobs?q={job}&fromage={job_age}'
    if search_location:
        location = search_location.replace(',', '%2C').replace(' ', '%20')
        indeed_job_url += f"&l={location}"

    return indeed_job_url


def scrape_job_card(job_meta):
    '''
    This function takes in a job_card_element from indeed.com and extracts the
    job title, company name, company location, and estimated salary
    input: 
        job_card_element, selenium webdriver object (specific to indeed.com)
    output: 
        - job_title, str
        - company_name, str
        - company_location, str
        - estimated_salary, str
    '''
    try:
        job_title = job_meta.find(
            'h2', {'class': 'jobTitle'}).get_text().lstrip('new\n')
    except:
        job_title = 'No job title found'
    try:
        company_name = job_meta.find(
            'span', {'class': 'companyName'}).get_text()
    except:
        company_name = 'No Company Name'
    try:
        company_location = job_meta.find(
            'div', {'class': 'companyLocation'}).get_text()
    except:
        company_location = 'No Location'
    try:
        estimated_salary = job_meta.find(
            'div', {'class': 'metadata salary-snippet-container'}).get_text()
    except:
        estimated_salary = 'No Estimated Salary'
    return job_title, company_name, company_location, estimated_salary


def scrape_job_description(job_desc_href):
    '''
    This function takes in a job_card_element from indeed.com and extracts the
    job description.
    input: 
        job_card_element: selenium webdriver object (specific to indeed.com)
    output: 
        job_desc, str, can be extremely long (avg 3,000-7,000 characters)
    '''
    try:
        page = web_scrape_api_call(job_desc_href)
        soup = BeautifulSoup(page.content, 'html.parser')
        job_desc = soup.find(id='jobDescriptionText')
        job_desc = job_desc.text.replace('\n', ' ').replace('\r', '')
    except:
        job_desc = 'No Job Description'
    return job_desc


def scrape_job_page_meta(job_page_html):
    '''
    This function takes in a html job page and uses beautiful soup to extract each jobs title, company name,
    estimated salary, job description href and then uses that href to open the job description page and
    extract that job description. While its looping through each job on the job page it is storing the 
    information in a pandas dataframe.
    input:
        job_page_html: html response from indeed search request
    output:
        jobs_df: pandas dataframe containing the scraped data from the job search page
    '''
    page_soup = BeautifulSoup(job_page_html.text, 'lxml')
    df_columns = ['job_title', 'company_name',
                  'company_location', 'est_salary', 'job_href', 'job_desc']
    jobs_df = pd.DataFrame(columns=df_columns)
    for job in page_soup.find_all('div', {"id": "mosaic-provider-jobcards"}):
        # Lets find the job title
        for href_post in job.find_all('a', href=True):
            if href_post.find('a', href=True):
                # this is for the url for the job posting
                job_desc_href = 'https://www.indeed.com'+str(href_post['href'])
                job_desc = scrape_job_description(job_desc_href)
                for job_meta in href_post.find_all('div', {"class": "job_seen_beacon"}):
                    job_title, company_name, company_location, estimated_salary = scrape_job_card(
                        job_meta)
                    print(f'{job_title}, {job_desc_href}')
                    job_dict = {'job_title': job_title,
                                'company_name': [company_name],
                                'company_location': [company_location],
                                'est_salary': [estimated_salary],
                                'job_href': [job_desc_href],
                                'job_desc': [job_desc]}
                    j_df = pd.DataFrame.from_dict(job_dict)
                    jobs_df = jobs_df.append(j_df, ignore_index=True)
    return jobs_df


def job_loc_scrape_loop(job_list, loc_list, job_age):
    '''
    This function takes in a list of job titles, locations and age.
    It then loops through each item of both lists, creates a url to call
    and then scrapes the given info from each page.
    At the end of each item in the loop, it saves the job info to a csv.
    '''
    date = dt.datetime.today().strftime('%Y-%m-%d')
    for job in job_list:
        for loc in loc_list:
            print(f'Scraping: {job} {loc}')
            indeed_url = make_indeed_url(job, loc, job_age)
            indeed_response = web_scrape_api_call(indeed_url)
            result_df = scrape_job_page_meta(indeed_response)
            result_df['retrieve_date'] = date
    result_df.to_csv("jobs.csv")
    print("Wrote to CSV")
    return None

def job_loc_scrape_loop_simple(job_list):
    '''
    This function takes in a list of job titles.
    It then loops through job titles, creates a url to call
    and then scrapes the given info from each page.
    At the end of each item in the loop, it saves the job info to a csv.
    '''
    date = dt.datetime.today().strftime('%Y-%m-%d')
    for job in job_list:
        print(f'Scraping: {job}')
        indeed_url = make_indeed_url(job)
        indeed_response = web_scrape_api_call(indeed_url)
        result_df = scrape_job_page_meta(indeed_response)
        result_df['retrieve_date'] = date
    result_df.to_csv("jobs_simple.csv")
    print("Wrote to CSV")
    return None


def web_scrape_api_call(url_to_scrape):
    '''
    sends the url that we would like to scrape to the webscrapingapi
    so that our calls can be ananomyzed. 
    '''
    url = "https://api.webscrapingapi.com/v1"
    params = {
        "api_key": WEB_SCRAPING_API_KEY,
        "url": url_to_scrape
    }
    response = requests.request("GET", url, params=params)
    return response


if __name__ == '__main__':
    job_list = [
        "Scientist",
        "Data Scientist",
        "Software Engineer"
    ]
    # primary_city_state_list = [
    #     "Atlanta, GA",
    #     "Austin, TX",
    #     "Boston, MA",
    #     "Chicago, IL",
    #     "Denver, CO",
    #     "Dallas-Ft. Worth, TX",
    #     "Los Angeles, CA",
    #     "New York City, NY",
    #     "San Francisco, CA",
    #     "Seattle, WA"
    # ]
    # job_loc_scrape_loop(job_list, primary_city_state_list, '7')
    job_loc_scrape_loop_simple(job_list)

