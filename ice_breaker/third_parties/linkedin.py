import os
import requests
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["PROXYCURL_API_KEY"] = os.getenv("PROXYCURL_API_KEY")

def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """
    scrapes a linkedin profile and returns the text
    """
    
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/maitys/f76b2ecf798087b0abf8c6fea9f68b19/raw/6beeda020d0aa690f2c0873a35ba3a50bed8202f/siddharth-maity-linkedin-json"
        response = requests.get(linkedin_profile_url, timeout=10)
        
    else:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header_dic = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
        response = requests.get(api_endpoint, params={"url": linkedin_profile_url}, headers=header_dic, timeout=10)
        
    data = response.json()
    ## remove empty values ##
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")
            
    return data
    
if __name__ == "__main__":
    print(scrape_linkedin_profile(linkedin_profile_url="x", mock=True))
    
    