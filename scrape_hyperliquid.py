#!/usr/bin/env python3
"""
Simple script to scrape Hyperliquid data from DeFiLlama
"""

import subprocess
import sys
import os

def scrape_hyperliquid():
    """Scrape Hyperliquid data and store in database"""
    try:
        print("Scraping Hyperliquid data from DeFiLlama...")
        
        # Run the spider
        result = subprocess.run([
            'scrapy', 'crawl', 'defillama_spider', '-a', 'protocol=hyperliquid'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Successfully scraped Hyperliquid data")
            print("Data has been stored in the database")
        else:
            print("Error scraping data:")
            print(result.stderr)
            
    except Exception as e:
        print(f"Error running scraper: {e}")

def show_latest_data():
    """Show only the latest Hyperliquid data in database"""
    try:
        print("\nLatest Hyperliquid data:")
        print("=" * 50)
        
        result = subprocess.run([
            'python', 'query_database.py'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(result.stdout)
        else:
            print("Error querying database:")
            print(result.stderr)
            
    except Exception as e:
        print(f"Error querying database: {e}")

if __name__ == "__main__":
    print("Hyperliquid Data Scraper")
    print("=" * 30)
    
    # Scrape new data
    scrape_hyperliquid()
    
    # Show latest database contents
    show_latest_data() 