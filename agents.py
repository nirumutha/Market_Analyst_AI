import os
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_openai import ChatOpenAI
# --- THE FIX IS ON THE NEXT LINE ---
from langchain_core.prompts import PromptTemplate 
from dotenv import load_dotenv

load_dotenv()

def analyze_market_trends(product_name, country_config):
    search = GoogleSerperAPIWrapper()
    query = f"{product_name} market trends consumer interest {country_config['country_full']}"
    return search.run(query)

def lookup_tax_rate(product_name, country_config):
    """
    Research the likely Tax/GST/VAT rate for a specific product category.
    """
    country = country_config['country_full']
    
    # 1. Define Strict Rules (The "Knowledge Base")
    default_rate = 0.20 # UK Standard
    if country == "India": default_rate = 0.18 # India Standard
    
    # 2. Use AI to categorize and refine the rate
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    template = """
    You are a Global Tax Compliance Officer.
    Determine the estimated Indirect Tax Rate (VAT/GST) for: "{product_name}" in {country}.
    
    STRICT RULES (2024/25):
    [INDIA]
    - Standard Electronics (Smart Rings, Earbuds): 18%
    - Luxury Cars/Yachts: 28%
    - Essentials (Food, Unbranded Clothes): 5% or 0%
    - Gold/Jewellery: 3%
    
    [UK]
    - Standard Goods: 20%
    - Children's Clothes / Books: 0%
    - Home Energy: 5%
    
    OUTPUT ONLY A JSON:
    {{ "rate": 0.18, "reason": "Electronics slab in India is 18%" }}
    """
    
    prompt = PromptTemplate(
        input_variables=["product_name", "country"],
        template=template
    )
    
    try:
        res = llm.invoke(prompt.format(product_name=product_name, country=country))
        import json
        return json.loads(res.content.replace("```json","").replace("```",""))
    except:
        return { "rate": default_rate, "reason": "Standard Fallback Rate" }