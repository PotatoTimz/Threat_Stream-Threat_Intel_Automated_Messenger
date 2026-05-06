import json
from openai import OpenAI
from dotenv import dotenv_values

# Create OPENAI instance
config = dotenv_values(".env")
OPENAI_API_KEY = config["OPENAI_API_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)

def basic_analyze_article(url):
    prompt = f"""
        You are going to analyze a news report to get relevant information.

        News Article URL:
        {url}
        
        Your task is to provide the following bits of information. Respond ONLY with a valid JSON object using the following schema:
        - title: article title
        - summary: a high level summary of the entire article. Limit this to one paragraph.
        - tags: a list of affect parties and technologies. Limit to the 15 most important tags. 
        - date: the date that the article was published
        - source: What news website did this article come from
        
        JSON Schema:
        {{
            "title" : "string",
            "summary" : "string",
            "tags" : "list",
            "date" : "string",
            "cves" : "list",
            "source": "string",
            "link" : "string"
        }}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini-search-preview",
        messages=[{"role": "user", "content": prompt}]
    )
    message_content = response.choices[0].message.content
    
    try:
        message_content = message_content[7:-4]
        # print(message_content)
        article_info = json.loads(message_content)
        print(article_info)
    except json.JSONDecodeError:
        print("Failed to parse JSON. Raw output:")
        # print(message_content)
    else:
        article_info["link"] = url
        return article_info
    
    return message_content

def exensive_analyze_article(url):
    prompt = f"""
        You are going to analyze a news report to get relevant information.

        News Article URL:
        {url}

        Your task is to provide the following bits of information. Respond ONLY with a valid JSON object using the following schema:
        - title: article title
        - summary: a high level summary of the entire article. Limit this to one paragraph.
        - tags: a list of affect parties and technologies. Limit to the 15 most important tags. 
        - tech_stack: a list of technologies relevant to this article.
        - company_correlation_rating: rate the relevancy of this article from a scale of 0-100 based on its relevancy to Loblaws Companies Limited
        - company_correlation_reasoning: give a few bullet point reasoning as to why you gave it its correlation score
        - severity_rating: rate the the severity of this issue from a scale of 0-100
        - severity_correlation_reasoning: give a few bullet point reasoning as to why you gave it its severity correlation score
        - source: what news website did this article come from
        
        JSON Schema:
        {{
            "title" : "string",
            "summary" : "string",
            "tags" : "list",
            "tech_stack" : "list",
            "company_correlation_rating" : "0-100"
            "company_correlation_reasoning" : "string",
            "severity_rating" : "0-100",
            "severity_correlation_reasoning" : "string",
            "source" : "string",
        }}
    """
    
    response = client.chat.completions.create(
            model="gpt-4o-mini-search-preview",
            messages=[{"role": "user", "content": prompt}]
        )
    message_content = response.choices[0].message.content
    
    try:
        message_content = message_content[7:-4]
        # print(message_content)
        article_info = json.loads(message_content)
    except json.JSONDecodeError:
        print("Failed to parse JSON. Raw output:")
        # print(message_content)
    else:
        article_info["link"] = url
        return article_info
    
    return ""