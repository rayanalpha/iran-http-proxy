import requests
import concurrent.futures
import logging
import time
from typing import List, Optional, Set

# --- Configuration ---
# API URLs provided by the user
API_URLS = [
    "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&country=ir&proxy_format=protocolipport&format=text",
    "https://openproxylist.xyz/http.txt?country=IR&referrer=grok.com"
]

# Stage 1: Check if proxy is generally alive
GLOBAL_CHECK_URL = "http://www.google.com"

# Stage 2: Check if proxy can access the specific target
TARGET_URL = "http://salamat.gov.ir"

# Timeout for network operations
TIMEOUT = 20 

# Number of concurrent threads
MAX_WORKERS = 50

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("ProxyChecker")

class ProxyScraper:
    def __init__(self, api_urls: List[str], timeout: int = 20):
        self.api_urls = api_urls
        self.timeout = timeout

    def fetch_proxies(self) -> List[str]:
        """Fetches the list of proxies from multiple API URLs and deduplicates them."""
        all_proxies: Set[str] = set()
        
        for url in self.api_urls:
            logger.info(f"Connecting to API: {url}")
            try:
                response = requests.get(url, timeout=self.timeout)
                response.raise_for_status()
                
                # Extract proxies line by line
                lines = [line.strip() for line in response.text.splitlines() if line.strip()]
                
                count = 0
                for line in lines:
                    # Normalize proxy format: Ensure it starts with http:// if missing
                    if "://" not in line:
                        proxy = f"http://{line}"
                    else:
                        proxy = line
                        
                    all_proxies.add(proxy)
                    count += 1
                
                logger.info(f"Retrieved {count} proxies from this source.")
                
            except requests.RequestException as e:
                logger.error(f"Error fetching from {url}: {e}")
        
        unique_proxies = list(all_proxies)
        logger.info(f"Total unique proxies collected: {len(unique_proxies)}")
        return unique_proxies

    def check_connectivity(self, proxy: str, url: str) -> bool:
        """
        Checks connectivity to a specific URL using the proxy.
        Returns True if successful, False otherwise.
        """
        proxies_dict = {
            "http": proxy,
            "https": proxy
        }

        try:
            response = requests.get(
                url, 
                proxies=proxies_dict, 
                timeout=self.timeout,
                allow_redirects=True
            )
            
            if response.status_code == 200:
                return True
                
        except Exception:
            pass
            
        return False

    def run(self):
        """Main execution flow."""
        proxies = self.fetch_proxies()
        
        if not proxies:
            logger.warning("No proxies found to check.")
            return

        # --- Phase 1: General Health Check ---
        logger.info("-" * 50)
        logger.info(f"PHASE 1: Checking general health (Google) for {len(proxies)} proxies...")
        logger.info("-" * 50)

        alive_proxies = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_proxy = {executor.submit(self.check_connectivity, p, GLOBAL_CHECK_URL): p for p in proxies}
            
            for future in concurrent.futures.as_completed(future_to_proxy):
                proxy = future_to_proxy[future]
                if future.result():
                    logger.info(f"✔️  ALIVE: {proxy}")
                    alive_proxies.append(proxy)

        logger.info(f"Phase 1 Complete. {len(alive_proxies)} proxies are alive.")
        
        if not alive_proxies:
            logger.warning("No alive proxies found. Exiting.")
            return

        # --- Phase 2: Target Specific Check ---
        logger.info("-" * 50)
        logger.info(f"PHASE 2: Checking access to {TARGET_URL}...")
        logger.info("-" * 50)

        final_working_proxies = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_proxy = {executor.submit(self.check_connectivity, p, TARGET_URL): p for p in alive_proxies}
            
            for future in concurrent.futures.as_completed(future_to_proxy):
                proxy = future_to_proxy[future]
                is_working = future.result()
                
                if is_working:
                    logger.info(f"✅ WORKS ON TARGET: {proxy}")
                    final_working_proxies.append(proxy)
                else:
                    logger.warning(f"❌ FAILED ON TARGET: {proxy} (Alive but blocked/timeout)")

        # --- Summary ---
        logger.info("-" * 50)
        logger.info(f"Final Report: Found {len(final_working_proxies)} proxies that open {TARGET_URL}.")
        
        if final_working_proxies:
            with open("working_proxies.txt", "w") as f:
                for p in final_working_proxies:
                    f.write(p + "\n")
            logger.info("Saved final working proxies to 'working_proxies.txt'.")
        else:
            logger.info("No proxies could open the target site.")

if __name__ == "__main__":
    scraper = ProxyScraper(API_URLS, timeout=TIMEOUT)
    scraper.run()
