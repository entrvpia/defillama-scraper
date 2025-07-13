#!/usr/bin/env python3
"""
Simple DataFrame Loader for DefiLlama Historical Data

This script provides easy access to the historical data as pandas DataFrames
for analysis and exploration.
"""

import sqlite3
import pandas as pd
import os

def load_historical_data(db_path='defillama_data.db'):
    """
    Load all historical data from the SQLite database into a pandas DataFrame
    
    Args:
        db_path (str): Path to the SQLite database file
        
    Returns:
        pandas.DataFrame: Complete historical dataset
    """
    try:
        # Check if database exists
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file '{db_path}' not found")
        
        # Connect to database
        conn = sqlite3.connect(db_path)
        
        # Query all data
        query = """
        SELECT 
            id,
            timestamp,
            ticker,
            price,
            market_cap,
            annualized_revenue,
            pe_ratio
        FROM defillama_metrics 
        ORDER BY timestamp DESC
        """
        
        # Load into DataFrame
        df = pd.read_sql_query(query, conn)
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        conn.close()
        
        print(f"✅ Loaded {len(df)} records from database")
        print(f"📊 Data shape: {df.shape}")
        print(f"📅 Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None

def get_latest_data(df, ticker=None):
    """
    Get the latest data for a specific ticker or all tickers
    
    Args:
        df (pandas.DataFrame): Historical data DataFrame
        ticker (str, optional): Specific ticker to filter
        
    Returns:
        pandas.DataFrame: Latest data
    """
    if ticker:
        latest = df[df['ticker'] == ticker].iloc[0] if len(df[df['ticker'] == ticker]) > 0 else None
        return latest
    else:
        return df.groupby('ticker').first().reset_index()

def get_data_summary(df):
    """
    Get a summary of the data
    
    Args:
        df (pandas.DataFrame): Historical data DataFrame
        
    Returns:
        dict: Summary statistics
    """
    summary = {
        'total_records': len(df),
        'tickers': df['ticker'].unique().tolist(),
        'date_range': {
            'start': df['timestamp'].min(),
            'end': df['timestamp'].max()
        },
        'columns': list(df.columns),
        'missing_values': df.isnull().sum().to_dict()
    }
    
    return summary

# Load the data when this module is imported
print("🔄 Loading DefiLlama historical data...")
historical_df = load_historical_data()

if historical_df is not None:
    print("✅ Data loaded successfully!")
    print("📋 Available functions:")
    print("   • historical_df: Complete historical dataset")
    print("   • get_latest_data(df, ticker): Get latest data for a ticker")
    print("   • get_data_summary(df): Get data summary")
    
    # Show quick summary
    summary = get_data_summary(historical_df)
    print(f"\n📊 Quick Summary:")
    print(f"   • Total records: {summary['total_records']}")
    print(f"   • Tickers: {', '.join(summary['tickers'])}")
    print(f"   • Date range: {summary['date_range']['start']} to {summary['date_range']['end']}")
    
    # Show sample data
    print(f"\n📄 Sample data:")
    print(historical_df.head())
else:
    print("❌ Failed to load data") 