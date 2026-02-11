import os
import requests
import json
import statistics
from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

def filter_junk_products(products, guardrails):
    min_p = guardrails.get('min_price', 0)
    max_p = guardrails.get('max_price', float('inf'))
    
    valid_products = []
    if min_p <= 0: min_p = 1
    
    print(f"🛡️ Validator: Filtering items outside {min_p} - {max_p}...")
    
    for p in products:
        price = p['price']
        if price >= (min_p * 0.8) and price <= (max_p * 1.5):
            valid_products.append(p)
            
    return valid_products

def get_price_data(product_name, country_config, guardrails):
    country_code = country_config['google_gl']
    raw_products = []
    source = "Amazon"
    
    amazon_country = "GB" if country_code.lower() in ["uk", "gb"] else "IN"
    
    try:
        print(f"🛍️ Amazon Scraper: Searching for '{product_name}' in {amazon_country}...")
        
        run_input = { 
            "searchQueries": [product_name], 
            "countryCode": amazon_country, 
            "maxItems": 10 
        }
        
        run = client.actor("apify/amazon-search-scraper").call(run_input=run_input)
        dataset = client.dataset(run["defaultDatasetId"]).list_items().items
        
        for item in dataset:
            price = item.get('price')
            if not price and 'pricing' in item:
                price = item['pricing'].get('realPrice')
            
            if price and isinstance(price, (int, float)) and price > 0:
                raw_products.append({ "title": item.get('title', 'Unknown'), "price": price })
        
        print(f"✅ Amazon found {len(raw_products)} items.")
                
    except Exception as e:
        print(f"⚠️ Amazon Scrape Skipped: {e}")

    if len(raw_products) < 3:
        source = "Google Shopping"
        print("🔄 Switching to Google Shopping...")
        try:
            url = "https://google.serper.dev/shopping"
            gl_code = "gb" if country_code.lower() == "uk" else country_code
            
            payload = json.dumps({ "q": product_name, "gl": gl_code, "num": 20 })
            headers = { 'X-API-KEY': os.getenv("SERPER_API_KEY"), 'Content-Type': 'application/json' }
            
            response = requests.post(url, headers=headers, data=payload)
            res = response.json()
            
            if "shopping" in res:
                for item in res["shopping"]:
                    currency = country_config['currency_symbol']
                    p_str = item.get('price', '').replace(currency, '').replace(',', '').strip()
                    try:
                        price_val = float(p_str)
                        raw_products.append({ "title": item.get('title'), "price": price_val })
                    except: continue
        except Exception as e:
            print(f"⚠️ Google Scrape Failed: {e}")

    clean_products = filter_junk_products(raw_products, guardrails)
    
    if not clean_products:
        source = "Market Estimate (Validator Fallback)"
        est_price = (guardrails['min_price'] + guardrails['max_price']) / 2
        clean_products.append({ "title": "Market Average Estimate", "price": est_price })

    avg_price = statistics.mean([p['price'] for p in clean_products])
    
    return { "source": source, "average_price": avg_price, "products": clean_products }