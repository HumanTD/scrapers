from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import pprint

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
HEADERS=({ "User-Agent": user_agent, "Content-Encoding": "br", "Cf-Ray": "865efb10dc77f3a5-BOM", "Cookie": "ajs_anonymous_id=63153436-7aaf-4b38-ba88-43580c577f8d; _wellfound=aa63168ca1d3975fa811dd3d4d9d71e5; _gcl_au=1.1.1858267607.1710694766; _hjSession_1444722=eyJpZCI6ImZmMzVjNGI0LTEzOGEtNDVmMy1hMDE4LWViNGJiMjZiZDM4MyIsImMiOjE3MTA2OTQ3NjU1NTcsInMiOjEsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxfQ==; _fbp=fb.1.1710694765588.9572783; _hjSessionUser_1444722=eyJpZCI6ImJjYjBhYjNkLWE1YzgtNTA5ZC05NGNmLWE1Y2I4MGQ4NjJjMCIsImNyZWF0ZWQiOjE3MTA2OTQ3NjU1NTcsImV4aXN0aW5nIjp0cnVlfQ==; _ga=GA1.1.661819419.1710694766; datadome=g_PKAobcHT6hxUQ91f7M0Rgb5v76GTj8s26TQ3AUr0C61YPjD40KiZr7fMC4Ra~B_tCqLAKNBKcZl04Q97d6wHKxJBE4iSo_3eLlFm8ADvQB8cygqD_EpeGR9DP2Ffiy; _ga_705F94181H=GS1.1.1710698960.2.1.1710698997.23.0.0"})

def fetch_jobs(location, role, page):
    jobs = []
    if page == 0:
        URL = f'''https://wellfound.com/location/{location}'''
    else:
        URL = f'''https://wellfound.com/location/{location}?page={page}'''
    print(URL)
    doc = requests.get(URL)
    role=""
    location = "united-states"
    if not doc:
        print("Error fetching URL")
        return None
    soup = BeautifulSoup(doc.content, 'html.parser')

    jobs_dict = {}
    
    job_listings = soup.findAll('div', class_='styles_result__rPRNG')

    # inside the job listings div loop through all the a tags to get job title and link
    for job in job_listings:
        company_name = job.find('h4', class_='styles_name__rSxBl').text
        job_title = job.find('a', class_='styles_jobTitle___jT4l').text
        job_link = job.find('a', class_='styles_jobTitle___jT4l')['href']
        upd_job_link = f'''https://wellfound.com{job_link}'''
        #  in the jobs_dict match the company name to an array of job titles and links

        # print(type('https://wellfound.com'), type(job_link))
        if company_name in jobs_dict:
            jobs_dict[company_name].append({'title': job_title, 'link': upd_job_link})
        else:
            jobs_dict[company_name] = [{'title': job_title, 'link': upd_job_link}]


    pprint.pprint(jobs_dict)
    return jobs_dict

role=""
location = "united-states"
max_pages = 40
i = 0
good_page_count = 0

while i < max_pages:
    if(max_pages > 250):
        break
    jobs = fetch_jobs(location, role, i)
    i += 1
    good_page_count += 1
    if not jobs:
        good_page_count -= 1
        max_pages += 1
    print(f"Page {i} done")

print(f"Good page count: {good_page_count}")
