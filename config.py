from check_api_version import get_latest_api_version

base_url = f'YOUR SHOPIFY URL'
API_KEY = "API KEY"
API_PASSWORD = "API PASSWORD"

stable_base_url = get_latest_api_version(base_url, API_KEY, API_PASSWORD)


