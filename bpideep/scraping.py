"""Library used to scraped data via webscraper and PhantomBuster. Webscraper is a brower 
extension that automates scraping. To use webscraper with scripts generated by functions 
in this module, click on 'create news site map', then 'import site map' and paste the script.
Warning: if the html structure of targeted pages changes, these scripts may need to be tailored"""

import pandas as pd

#List of elements to scrape on company people page: employee profile link, title, name
#Output: table with for each individual: company name, company id, employee profile link, title, name


class str2(str):
    def __repr__(self):
        # remove the outer two characters, single quotes, and replace them with double quotes.
        # Used to generate scraping url with double quotes compatible with webscraper
        return ''.join(('"', super().__repr__()[1:-1], '"'))


"""WARNING: before scraping, verify the number of employees of target companies. Scraping
a 2000 employee company will take more than 30min"""

def make_scripts_company_people():
    """This function generates scraping scripts to be used on webscraper, to scrape people 
    names, titles and profile_urls for a given company. 
    X should be a dataframe with urls in a column 'linkedin_url', as per data provided by
    dearlroom. Scraping takes about 1min per company"""
    X = pd.read_csv('../bpideep/rawdata/data2020-12-03.csv')
    company_count = X.shape[0]
    batches = int(company_count/100)
    urls = X[['linkedin_url']]
    for i in range(0, batches+1):
        name = f"script_batch_{i}"
        batch = []
        for j in range (i*100, (i+1)*100):
            if j > company_count-1:
                break
            else:
                url= f'{urls.iloc[j,0]}/people'
                #str2 is used to replace single quotes by double quotes (webscraper compatibility)
                company = str2(url)
                batch.append(company)
        #the script below was written to scrape people names, titles and profile_urls for a given company, via webscraper       
        script= f'{{"_id":"scraping","startUrl":{batch},"selectors":[\
                    {{"id":"container","type":"SelectorElementScroll","parentSelectors":["_root"],"selector":"div.org-people-profile-card__profile-info","multiple":true,"delay":"1234"}},\
                        {{"id":"name","type":"SelectorText","parentSelectors":["container"],"selector":"div.org-people-profile-card__profile-title","multiple":false,"regex":"","delay":0}},\
                        {{"id":"title","type":"SelectorText","parentSelectors":["container"],"selector":"div.lt-line-clamp--multi-line","multiple":false,"regex":"","delay":0}},\
                        {{"id":"profile","type":"SelectorLink","parentSelectors":["container"],"selector":"a.link-without-visited-state","multiple":false,"delay":0}}]}}'
        script.replace("\\", "")
        # The function outputs a string for each batch as a text file
        path = '../bpideep/scraping_data/scraping_scripts/'
        with open(path + f"{name}.txt", "w") as text_file:
            text_file.write(script)
        # Another output is the printed scripts, from which you can copy/paste in webscraper.
        print(name)
        print(script)
    return None


def make_scripts_description(X):
    """This function generates scraping scripts to be used on webscraper, to scrape the 
    description field of companies.
    The loaded data should be a csv with urls in a column 'linkedin_url', as per data provided by
    dearlroom. Scraping takes about 1min per company"""
    X = pd.read_csv('../../full_data.csv')
    company_count = X.shape[0]
    batches = int(company_count/100)
    urls = X[['linkedin_url']]
    for i in range(0, batches+1):
        name = f"script_description_{i}"
        batch = []
        for j in range (i*100, (i+1)*100):
            if j > count-1:
                break
            else:
                #str2 is used to replace single quotes by double quotes (webscraper compatibility)
                company = str2(urls.iloc[j,0])
                batch.append(company)
        #the script below was written to scrape the description for a given company, via webscraper     
        script= f'{{"_id":"linkedin","startUrl":{batch},"selectors":[\
                    {{"id":"container","type":"SelectorElementScroll","parentSelectors":["_root"],"selector":"div.org-people-profile-card__profile-info","multiple":true,"delay":"1234"}},\
                        {{"id":"name","type":"SelectorText","parentSelectors":["container"],"selector":"div.org-people-profile-card__profile-title","multiple":false,"regex":"","delay":0}},\
                        {{"id":"title","type":"SelectorText","parentSelectors":["container"],"selector":"div.lt-line-clamp--multi-line","multiple":false,"regex":"","delay":0}},\
                        {{"id":"profile","type":"SelectorLink","parentSelectors":["container"],"selector":"a.link-without-visited-state","multiple":false,"delay":0}}]}}'
        script.replace("\\", "")
        # The function outputs a string for each batch as a text file
        with open(f"{name}.txt", "w") as text_file:
            text_file.write(script)
        # Another output is the printed scripts, from which you can copy/paste in webscraper.
        print(name)
        print(script)
    return None