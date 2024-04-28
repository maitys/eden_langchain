import sys,os
sys.path.insert(0, os.getcwd())
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from dotenv import load_dotenv
from ice_breaker.tools.tools import get_profile_url_tavily

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

def linkedin_url_lookup(name):
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    
    template = """
    given the full name {name_of_person} I want you to get it me a link to their Linkedin profile page.
    Your answer should only contain a valid URL.
    """
    
    prompt_template = PromptTemplate(template=template, input_variables=["name_of_person"])

    tools_for_agent = [Tool(name="Crawl Google for linkedin profile page",
                            func=get_profile_url_tavily,
                            description = "useful for when you need to get the linkedin page url")]
    
    react_prompt = hub.pull("hwchase17/react")
    
    agent = create_react_agent(llm=llm, prompt=react_prompt, tools=tools_for_agent)
    
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)
    
    result = agent_executor.invoke({"input": prompt_template.format_prompt(name_of_person=name)})
    
    linkedin_profile_url = result["output"]
    
    return linkedin_profile_url
        
if __name__ == "__main__":
    linkedin_url = linkedin_url_lookup("Siddharth Maity")
    print("*"*100)
    print(linkedin_url)
    
                            
    