import os
from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import linkedin_url_lookup

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

def ice_break_with(name):

    print(f"Conda environment: {os.getenv('CONDA_DEFAULT_ENV')}")

    summary_template = """
    given the information {information} about a person I want you to create:
    1. A short summary
    2. Two interesting facts about them
    3. Which companies they have worked at
    """
    
    summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_template)
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    
    chain = LLMChain(llm=llm, prompt=summary_prompt_template)
    
    linkedin_url = linkedin_url_lookup(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_url, mock=True)
    
    res = chain.invoke(input={"information": linkedin_data})
    
    print(res["text"])
    
if __name__ == "__main__":
    print("Ice Break with")
    ice_break_with("Siddharth Maity Raptive")