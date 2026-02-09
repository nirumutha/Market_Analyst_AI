def get_country_config(country):
    if country == "INDIA":
        return {
            "country_full": "India",
            "currency_symbol": "₹",
            "google_gl": "in",
            "tld": "in"
        }
    elif country == "UK":
        return {
            "country_full": "United Kingdom",
            "currency_symbol": "£",
            # Google expects 'uk', we handle Amazon 'GB' mapping in scraper.py
            "google_gl": "uk", 
            "tld": "co.uk"
        }
    return None