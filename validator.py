from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import json

load_dotenv()

def get_market_guardrails(product_name, country_config):
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    currency = country_config.get('currency_symbol', '$')
    country = country_config.get('country_full', 'Unknown')

    template = """
    You are a Market Calibration Engine.
    
    Product: "{product_name}"
    Target Market: {country}
    Currency: {currency}
    
    TASK: Determine the REALISTIC price range for one unit of this product in {currency}.
    Exclude cheap accessories.
    
    EXAMPLES:
    - Smart Ring (India/₹) -> min: 3000, max: 35000
    - Smart Ring (UK/£) -> min: 40, max: 400
    
    OUTPUT JSON ONLY:
    {{
        "min_price": 50,
        "max_price": 400
    }}
    """
    
    prompt = PromptTemplate(input_variables=["product_name", "country", "currency"], template=template)
    
    try:
        res = llm.invoke(prompt.format(product_name=product_name, country=country, currency=currency))
        return json.loads(res.content.replace("```json", "").replace("```", "").strip())
    except:
        return {"min_price": 10, "max_price": 1000000}