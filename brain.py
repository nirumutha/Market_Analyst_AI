import json
import re
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Temperature 0.5 for creativity in strategy, but we force math logic below
llm = ChatOpenAI(model="gpt-4o", temperature=0.5)

def clean_and_parse_json(text):
    try:
        # Try to find JSON inside the text (handling potential markdown wrappers)
        cleaned = text.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned)
    except:
        try:
            # Regex fallback if the AI adds extra text around the JSON
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

def calculate_viability_score(product_name, country_config, market_data, competitor_data, sourcing_data, tax_info):
    currency = country_config['currency_symbol']
    scraped_price = competitor_data.get('average_price', 0)
    is_fallback = "Fallback" in competitor_data.get('source', '')
    confidence_score = 55 if is_fallback else 70
    
    # --- 1. STRICT FINANCIAL CALCULATOR (Python, not AI) ---
    # We calculate everything here to ensure 100% mathematical accuracy.
    
    if scraped_price > 0:
        # Step A: Clean the Price (Force Integer)
        sell_price = int(scraped_price)
        
        # Step B: Get Tax Rate (Handle 18 vs 0.18)
        raw_rate = tax_info.get('rate', 0.18)
        if raw_rate > 1: raw_rate = raw_rate / 100 # Fix for "18" becoming "0.18"
        
        # Step C: Calculate Costs as Integers (No decimals)
        cogs_cost = int(sell_price * 0.35)   # 35% Manufacturing
        ads_cost = int(sell_price * 0.25)    # 25% Marketing/CPA
        logs_cost = int(sell_price * 0.15)   # 15% Logistics
        tax_amt = int(sell_price * raw_rate) # Tax Amount (Correctly calculated now)
        
        # Step D: Calculate Exact Net Profit
        total_expenses = cogs_cost + ads_cost + logs_cost + tax_amt
        net_profit = sell_price - total_expenses
        
        # Step E: Calculate Margin %
        net_margin = int((net_profit / sell_price) * 100)
    else:
        # Safety for zero results
        sell_price = cogs_cost = ads_cost = logs_cost = tax_amt = net_profit = net_margin = 0

    # --- END CALCULATOR ---

    template = """
    You are a Strategic Market Intelligence Engine.
    
    TARGET PRODUCT: "{product_name}"
    TARGET MARKET: {country_full}
    
    HARD DATA (DO NOT CHANGE THESE NUMBERS):
    - Avg Sell Price: {currency}{price}
    - Tax ({tax_pct}%): {currency}{tax_amt}
    - REAL NET PROFIT: {currency}{net_profit} (Margin: {net_margin}%)
    - Competitor Count: {comp_count} items found
    
    CONTEXT:
    - Trends: {trends}
    - Supply Chain: {sourcing}
    
    SCORING RUBRIC (BE STRICT):
    - DEMAND (1-10): 10 = Viral/Explosive trend. 5 = Stable/Flat. 1 = Dead/Declining.
    - COMPETITION (1-10): 10 = Blue Ocean (Zero rivals). 5 = Normal. 1 = Saturated/Bloodbath (>20 rivals).
    - ECONOMICS (1-10): 10 = High Margin (>25%). 5 = Tight Margin (10-15%). 1 = Money Pit (<5%).
    
    MISSION:
    1. Analyze the data using the rubric above.
    2. Write a 'Strategic Thesis'. 
    3. CRITICAL RULE: If you mention price, write "{currency}{price}" (No decimals).
    
    OUTPUT JSON FORMAT:
    {{
        "final_score": <Calculate weighted average>,
        "confidence_score": {confidence_score},
        "verdict_tag": "🟡 ENTER CAUTIOUSLY",
        "strategic_thesis": "Thesis here.",
        "lifecycle_stage": "Growth",
        "volatility": "Medium",
        "financials": {{ 
            "sell_price": {price}, 
            "cogs": {cogs}, 
            "marketing_cpa": {ads},
            "logistics_cost": {logs},
            "tax_rate": {tax_amt},
            "net_margin_pct": {net_margin},
            "net_profit": {net_profit},
            "note": "Net profit is {currency}{net_profit}."
        }},
        "market_entry": {{ "strategy": "D2C/Retail", "reason": "Reason." }},
        "breakdown": {{
            "demand": {{ "total": <Score>, "reason": "Reason.", "signal_1": "Search: High", "signal_2": "Growth: Fast", "signal_3": "Social: Viral" }},
            "competition": {{ "total": <Score>, "reason": "Reason.", "signal_1": "Count: High", "signal_2": "Dominance: Low", "signal_3": "Barrier: Med" }},
            "economics": {{ "total": <Score>, "reason": "Reason.", "signal_1": "Gross: Good", "signal_2": "Net: Tight", "signal_3": "Ads: High" }},
            "culture": {{ "total": <Score>, "reason": "Reason.", "signal_1": "Tech: High", "signal_2": "Trust: Low", "signal_3": "Habit: New" }}
        }},
        "pros": [ "Pro 1", "Pro 2" ],
        "cons": [ "Con 1", "Con 2" ],
        "recommendation": "Final advice."
    }}
    """
    
    comp_count = len(competitor_data.get('products', [])) if competitor_data else 0

    prompt = PromptTemplate(
        input_variables=["country_full", "product_name", "trends", "comp_source", "sourcing", "confidence_score", "price", "currency", "cogs", "ads", "logs", "tax_reason", "tax_amt", "tax_pct", "net_profit", "net_margin", "comp_count"], 
        template=template
    )
    
    final_prompt = prompt.format(
        country_full=country_config['country_full'], 
        product_name=product_name,
        trends=str(market_data)[:600], 
        comp_source=competitor_data.get('source'),
        sourcing=str(sourcing_data)[:600], 
        confidence_score=confidence_score,
        price=sell_price, 
        currency=currency,
        cogs=cogs_cost,
        ads=ads_cost,
        logs=logs_cost,
        tax_reason=tax_info.get('reason'),
        tax_amt=tax_amt,
        tax_pct=int(raw_rate*100),
        net_profit=net_profit,
        net_margin=net_margin,
        comp_count=comp_count
    )
    
    try:
        res = llm.invoke(final_prompt)
        result = clean_and_parse_json(res.content)
        if result:
            # FORCE OVERWRITE: Ensure the Python-calculated math replaces any AI guesses
            fin = result.get('financials', {})
            fin['sell_price'] = sell_price
            fin['cogs'] = cogs_cost
            fin['marketing_cpa'] = ads_cost
            fin['logistics_cost'] = logs_cost
            fin['tax_rate'] = tax_amt
            fin['net_profit'] = net_profit
            fin['net_margin_pct'] = net_margin
            result['financials'] = fin
            return result
        return get_empty_verdict("JSON Error")
    except Exception as e: return get_empty_verdict(str(e))