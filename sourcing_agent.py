from langchain_community.utilities import GoogleSerperAPIWrapper
from dotenv import load_dotenv

load_dotenv()

def get_wholesale_cost(product_name, config):
    search = GoogleSerperAPIWrapper(gl=config['google_gl'])
    location_keyword = "IndiaMart" if config['google_gl'] == 'in' else "Alibaba"
    query = f"Wholesale bulk manufacturing cost per unit for {product_name} on {location_keyword}"
    return search.run(query)