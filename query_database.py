#!/usr/bin/env python3
"""
Database query utility for defillama_metrics
"""

import sqlite3
import pandas as pd
from datetime import datetime

def query_database():
    """Query and display latest data from the database"""
    try:
        conn = sqlite3.connect('defillama_data.db')
        
        # Query only the latest entry for each ticker
        query = """
        SELECT 
            timestamp,
            ticker,
            price,
            market_cap,
            annualized_revenue,
            pe_ratio
        FROM defillama_metrics 
        WHERE id IN (
            SELECT MAX(id) 
            FROM defillama_metrics 
            GROUP BY ticker
        )
        ORDER BY timestamp DESC
        """
        
        df = pd.read_sql_query(query, conn)
        
        if df.empty:
            print("No data found in database.")
            return
        
        # Format the display
        print("DefiLlama Metrics Database (Latest Entries)")
        print("=" * 80)
        
        for _, row in df.iterrows():
            print(f"Timestamp: {row['timestamp']}")
            print(f"Ticker: {row['ticker']}")
            print(f"Market Cap: ${row['market_cap']:,.0f}" if row['market_cap'] else "Market Cap: N/A")
            print(f"Annual Revenue: ${row['annualized_revenue']:,.0f}" if row['annualized_revenue'] else "Annual Revenue: N/A")
            print(f"P/E Ratio: {row['pe_ratio']}" if row['pe_ratio'] else "P/E Ratio: N/A")
            print("-" * 40)
        
        conn.close()
        
    except Exception as e:
        print(f"Error querying database: {e}")

def get_latest_data(ticker=None):
    """Get the latest data for a specific ticker or all tickers"""
    try:
        conn = sqlite3.connect('defillama_data.db')
        
        if ticker:
            query = """
            SELECT * FROM defillama_metrics 
            WHERE ticker = ? 
            ORDER BY timestamp DESC 
            LIMIT 1
            """
            df = pd.read_sql_query(query, conn, params=(ticker,))
        else:
            query = """
            SELECT ticker, MAX(timestamp) as latest_timestamp
            FROM defillama_metrics 
            GROUP BY ticker
            """
            df = pd.read_sql_query(query, conn)
        
        conn.close()
        return df
        
    except Exception as e:
        print(f"Error getting latest data: {e}")
        return None

if __name__ == "__main__":
    print("DefiLlama Database Query Tool")
    print("=" * 50)
    
    # Show latest data only
    query_database()
    
    # Show available tickers
    print("\nAvailable tickers in database:")
    df_latest = get_latest_data()
    if df_latest is not None and not df_latest.empty:
        for _, row in df_latest.iterrows():
            print(f"  • {row['ticker']} (last updated: {row['latest_timestamp']})") 