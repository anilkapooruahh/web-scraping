from bs4 import BeautifulSoup
import requests
import time

# HELPER FUNCTIONS
def is_valid_job(text, skills):
    """(str, str list)-> bool
    Gets a job description and checks if the given skills are present in the description"""

    return any([skill in text for skill in skills])


# Input from user
country_code_dict = {"ca" : "Canada", "in" : "India"}    
COUNTRY_CODE = input("Enter the country code {Canada = ca, India = in}\n" )
JOB = input("Enter a job you would like to search for\n").replace(" ", "%20")
LOCATION = input(f"Enter the location you would like to search in {country_code_dict[COUNTRY_CODE]}\n")
AMOUNT = int(input("How many results do you want?\n"))
SKILLS = []
while True:
    skill = input("Enter a relevant skill that you have. Type done if you're finished\n")
    if skill == "done": 
        break
    SKILLS.append(skill.lower())

jobs = 0
filtered_jobs = 0
# main loop

while filtered_jobs < AMOUNT:
    html_text = requests.get(f'https://{COUNTRY_CODE}.indeed.com/jobs?q={JOB}&sort=date&start={jobs}&l={LOCATION}').text
    soup = BeautifulSoup(html_text, features="lxml")


# Collect the links to the individual job postings
    job_links = soup.find_all('a', class_ ="tapItem")
  
    
    for job in job_links:
        # Source code has relative url so need to format again

        url = f"https://{COUNTRY_CODE}.indeed.com{job['href']}"
        
        job_text = requests.get(url).text
        job_soup = BeautifulSoup(job_text, features="lxml")
        job_info = job_soup.find('div', class_ = "jobsearch-DesktopStickyContainer")
        job_name = job_info.find("h1", class_ = "jobsearch-JobInfoHeader-title" )
        job_company_name = job_info.find("div", class_ = "jobsearch-InlineCompanyRating")
        
        # Checking if span.text has a dollar sign in it. Can be replaced by a list of currency symbols and helper func
        job_salary = job_info.find("div", id = "salaryInfoAndJobType")
        salary = "none provided"
        if job_salary is not None and '$' in job_salary.span.text:
            salary = job_salary.span.text

        # Job description and skills
        job_desc = job_soup.find("div", id = "jobDescriptionText")
        job_skills = "\n".join([ f"{skill.text}" for skill in job_desc.find_all("li") ])
        
        
        if is_valid_job(job_skills.lower(),SKILLS):
            filtered_jobs += 1
        # Refactor into function
            with open(f"{JOB}.txt", "a") as file:
                file.write("Job Profile\n")
                file.write(f"Job posting at {url}\n")
                file.write(f"Title: {job_name.text}")
                file.write('\n')
                file.write(f"Company: {job_company_name.text}\n")
                file.write(f"Salary: {salary}\n\n")
        print(jobs, filtered_jobs)       

#  print([f"{COUNTRY_CODE}.indeed.com{a['href']}" for a in job_links])
    jobs += len(job_links)
    time.sleep(10)

print(jobs)
print(SKILLS) 


# def data(job):
    
#     result = ""
#     company = job.find('div', class_ ="heading6 company_location tapItem-gutter companyInfo")
#     salary  = job.find('div', class_ = 'salary-snippet')
#     skills  = job.find('li')
#     if company is not None:
#         result += f"company: {company.text}\n"
    
#     if salary is not None:
#         result += f"salary: {salary.text}\n"
#     if skills is not None:
#         result += f"skills: {skills.text}\n"
#     result += "\n"

#     with open("results.txt", "a") as file:
#         file.write(result)

# for job in jobs:
#     data(job)





