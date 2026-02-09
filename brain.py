import json
import re
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Temperature 0.5 allows for dynamic, product-specific creativity
llm = ChatOpenAI(model="gpt-4o", temperature=0.5)

def smart_round(value):
    try:
        val = float(value)
        if val > 1000: return int(round(val / 100) * 100)
        elif val > 100: return int(round(val / 10) * 10)
        return int(val)
    except: return value

def clean_and_parse_json(text):
    try:
        cleaned = text.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned)
    except:
        try:
            match = re.search(r"(\{.*\})", text, re.DOTALL)
            if match: return json.loads(match.group(1))
        except: return None

def get_empty_verdict(error_msg):
    return {
        "final_score": 0, "confidence_score": 0, "verdict_tag": "ERROR",
        "strategic_thesis": "Analysis Failed",
        "lifecycle_stage": "Unknown", "volatility": "Unknown", "financials": {}, 
        "breakdown": {}, "market_entry": {}, "pros": [], "cons": [], "recommendation": error_msg
    }

def get_regional_context(country_code):
    if country_code == "uk":
        return "MARKET CONTEXT: UK (High VAT, Expensive Ads, Mature Tech Adoption)"
    elif country_code == "in":
        return "MARKET CONTEXT: INDIA (Price Sensitive, High Volume Needed, Emerging Tech)"
    return "MARKET CONTEXT: Global Standard"

def calculate_viability_score(product_name, country_config, market_data, competitor_data, sourcing_data):
    currency = country_config['currency_symbol']
    scraped_price = competitor_data.get('average_price', 0)
    is_fallback = "Fallback" in competitor_data.get('source', '')
    confidence_score = 55 if is_fallback else 70
    regional_context = get_regional_context(country_config.get('google_gl', ''))

    template = """
    You are a Strategic Market Intelligence Engine.
    
    TARGET PRODUCT: "{product_name}"
    TARGET MARKET: {country_full}
    {regional_context}
    
    REAL DATA STREAMS:
    - Detected Price: {currency}{scraped_price} (Source: {comp_source})
    - Search Trends: {trends}
    - Supply Chain: {sourcing}
    
    ### MISSION: 
    Generate a highly specific strategic analysis for "{product_name}".
    
    ### DYNAMIC LOGIC RULES (MUST FOLLOW):
    1. **Category Detection:** First, determine if this is Electronics, Fashion, Home, or Consumable.
    2. **Economics:** - If Electronics: Gross Margin is typically 30-40%.
       - If Fashion/Beauty: Gross Margin is typically 65-80%.
       - If Home/Generic: Gross Margin is typically 50%.
       - *DO NOT output generic "82%" for everything.*
    3. **Competition:**
       - Use specific comparisons. If "{product_name}" is a "Gaming Laptop", compare listings to "Office Laptops".
       - If "{product_name}" is "Lipstick", compare to "Skincare".
    
    ### OUTPUT JSON FORMAT:
    {{
        "final_score": 7.5,
        "confidence_score": {confidence_score},
        "verdict_tag": "🟡 ENTER CAUTIOUSLY",
        "strategic_thesis": "Two sentence executive summary specific to {product_name} and its category challenges.",
        "lifecycle_stage": "Growth",
        "volatility": "Medium",
        "financials": {{ 
            "sell_price": {scraped_price}, 
            "cogs": 0, 
            "gross_margin_pct": 0,
            "marketing_cpa": 0,
            "logistics_cost": 0,
            "tax_rate": 0,
            "net_margin_pct": 0,
            "net_profit": 0,
            "note": "Financial note specific to {product_name} economics."
        }},
        "market_entry": {{ "strategy": "D2C/Retail", "reason": "Reason based on product category." }},
        "breakdown": {{
            "demand": {{ 
                "total": 8, 
                "signal_1": "Interest: [Rising/Falling] (from Trends)", 
                "signal_2": "Vol: [Estimate]k/mo", 
                "signal_3": "Adoption: [Early/Mass]", 
                "reason": "Demand analysis for {product_name}." 
            }},
            "competition": {{ 
                "total": 6, 
                "signal_1": "Saturation: [High/Low]", 
                "signal_2": "Rivals: [Fragmented/Monopoly]", 
                "signal_3": "Differentiation: [Easy/Hard]", 
                "reason": "Competition analysis for {product_name}." 
            }},
            "economics": {{ 
                "total": 7, 
                "signal_1": "Gross: [Category Benchmark]%", 
                "signal_2": "Net: [Estimate]%", 
                "signal_3": "Ads: [Cheap/Expensive]", 
                "reason": "Economic analysis for {product_name}." 
            }},
            "culture": {{ 
                "total": 6, 
                "signal_1": "Fit: [Natural/Forced]", 
                "signal_2": "Trust: [Required/Not Needed]", 
                "signal_3": "Barrier: [None/High]", 
                "reason": "Cultural analysis for {product_name}." 
            }}
        }},
        "pros": [
            {{ "title": "Product Strength", "specs": ["Specific Point 1 about {product_name}", "Specific Point 2"] }},
            {{ "title": "Market Opportunity", "specs": ["Specific Point 1", "Specific Point 2"] }}
        ],
        "cons": [
            {{ "title": "Category Risk", "specs": ["Specific Point 1 about {product_name}", "Specific Point 2"] }},
            {{ "title": "Operational Pain", "specs": ["Specific Point 1", "Specific Point 2"] }}
        ],
        "recommendation": "Final strategic advice."
    }}
    """
    
    prompt = PromptTemplate(
        input_variables=["country_full", "product_name", "trends", "regional_context", "comp_source", "sourcing", "confidence_score", "scraped_price", "currency"], 
        template=template
    )
    
    final_prompt = prompt.format(
        country_full=country_config['country_full'], 
        product_name=product_name,
        regional_context=regional_context,
        trends=str(market_data)[:600], 
        comp_source=competitor_data.get('source'),
        sourcing=str(sourcing_data)[:600], 
        confidence_score=confidence_score,
        scraped_price=scraped_price, 
        currency=currency
    )
    
    try:
        res = llm.invoke(final_prompt)
        result = clean_and_parse_json(res.content)
        if result:
            fin = result.get('financials', {})
            # Rounding for clean display
            fin['sell_price'] = smart_round(fin.get('sell_price', 0))
            fin['cogs'] = smart_round(fin.get('cogs', 0))
            fin['marketing_cpa'] = smart_round(fin.get('marketing_cpa', 0))
            fin['logistics_cost'] = smart_round(fin.get('logistics_cost', 0))
            fin['tax_rate'] = smart_round(fin.get('tax_rate', 0))
            fin['net_profit'] = smart_round(fin.get('net_profit', 0))
            result['financials'] = fin
            return result
        return get_empty_verdict("JSON Error")
    except Exception as e: return get_empty_verdict(str(e))