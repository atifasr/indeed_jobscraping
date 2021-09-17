
import requests
from bs4 import BeautifulSoup
from requests.api import request

#for setting connection and getting soup obj
def get_content(page_no=0):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
    }
    url = f"https://in.indeed.com/jobs?q=work+from+home&start=10"

    resp = requests.get(url,headers=headers)
    print(resp.status_code)
    soup = BeautifulSoup(resp.content, 'html.parser')
    
    return soup

# indeed job descriptions using links 

def get_job_detail(job_link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
    }
    url = f"https://in.indeed.com{job_link}"
    resp = requests.get(url,headers=headers)
    resp = BeautifulSoup(resp.content,"html.parser")
    job = resp.find("div",class_ = "jobsearch-JobComponent")
    job_body = job.find("div",class_ = "jobsearch-jobDescriptionText")
    job_description = job_body.find_all("p")
    for value in job_description:
        print(value.get_text())

    



#getting job links
def get_links(content):
    job_links = content.find_all("a",class_ = "tapItem")
    job_link_list = []
    for links in job_links:
        job_link_list.append(links['href']) 
    get_job_detail(job_link_list[0])
    
    


#getting job data dictionary

def get_data(soup):
    content = soup.find_all("table",class_ = "jobCard_mainContent")
    job_details_list = []

    for val in content:
        result_content  = val.find_all("td",class_ = "resultContent")
        job_descrip = val.find_all("table",class_ = "jobCardShelfContainer")
        for result in result_content:
            job_title = result.find("h2",class_= "jobTitle").get_text()
            company_name = result.find("span",class_ = "companyName").get_text()
            company_location = result.find("div",class_ = "companyLocation").get_text()
            job_detail ={
                'job_title':job_title,
                'company_name':company_name,
                'company_location':company_location,  
            }
            try:
                salary = result.find("span", class_ = "salary-snippet").get_text()
                job_detail['salary'] = salary
            except Exception as e:
                salary = 0
            
            job_details_list.append(job_detail)

    print(job_details_list)




content  = get_content()
get_links(content)
#get_data(content)

