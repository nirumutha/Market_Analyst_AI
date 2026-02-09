from langchain_community.utilities import GoogleSerperAPIWrapper
from dotenv import load_dotenv

load_dotenv()

def analyze_market_trends(product_name, config):
    search = GoogleSerperAPIWrapper(gl=config['google_gl'])
    query = f"Market growth trends, demand, and consumer interest for {product_name} in {config['country_full']} 2024 2025"
    return search.run(query)