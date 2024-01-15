# This is a code done by follow the course: Web Scraping with Python from freecodecamp
# The link: https://www.youtube.com/watch?v=XVv6mJpFOb0

import requests
from bs4 import BeautifulSoup
import time

unfamiliar_skills = list()
# print('Put a skill that your are not familiar with:')
unfamiliar_skill = ''
while unfamiliar_skill != 'x':
    print('Put a skill that your are not familiar with, (x) for exit:')
    unfamiliar_skill = input('>')
    if unfamiliar_skill != 'x':
        unfamiliar_skills.append(unfamiliar_skill.lower())
        print(f'Unfamiliar skills for now is {[x for x in unfamiliar_skills]}')

print(f'Filtering out {[x for x in unfamiliar_skills]}')


def find_jobs():
    response = requests.get(
        'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=Python&txtLocation=')

    if response.status_code == 200:
        html_text = response.text
        soup = BeautifulSoup(html_text, 'lxml') #lxml is a parser
        jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

        for index, job in enumerate(jobs):
            # Get how long the job post posted then filter it
            days_ago = job.find('span', class_='sim-posted').text.strip()
            if days_ago == 'Posted few days ago':
                company_name = job.find(
                    'h3', class_='joblist-comp-name').text.strip()
                skills = job.find(
                    'span', class_='srp-skills').text.strip().replace('  ,  ', ', ')
                more_info = job.header.h2.a['href']
                braked = False
                # To remove any unfamiliar skill from the list of skills in the job
                for unfamiliar_skill in unfamiliar_skills:
                    if unfamiliar_skill in skills:
                        braked = True
                        break
                if not braked:
                    with open(f'posts/{index}.text','w') as f:
                        
                        f.write(f'''
Company Name: {company_name},
skills: {skills},
More info: {more_info}
##############################################''')
                        print(f'File {index} saved.')
    else:
        print('Oops, something went wrong with the request.')


if __name__ == '__main__':
    while True:
        find_jobs()
        time_wait = 1
        print(f'Waiting {time_wait} minutes ...')
        time.sleep(time_wait * 60)