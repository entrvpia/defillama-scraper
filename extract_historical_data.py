#!/usr/bin/env python3
"""
Historical Data Extraction Script for DefiLlama Metrics Database

This script extracts all historical data from the SQLite database and creates
a pandas DataFrame for analysis. It provides both the raw data and some
basic analytics.

Author: ML Assistant
Date: 2025
"""

import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime
import os

def connect_to_database(db_path='defillama_data.db'):
    """
    Step 1: Establish connection to the SQLite database
    
    This function creates a connection to the SQLite database file.
    The database contains historical metrics for DeFi protocols.
    
    Args:
        db_path (str): Path to the SQLite database file
        
    Returns:
        sqlite3.Connection: Database connection object
    """
    try:
        # Check if database file exists
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file '{db_path}' not found")
        
        # Create connection
        conn = sqlite3.connect(db_path)
        print(f"✅ Successfully connected to database: {db_path}")
        return conn
    
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        return None

def get_database_info(conn):
    """
    Step 2: Get basic information about the database
    
    This function queries the database to understand:
    - Total number of records
    - Available tickers/protocols
    - Date range of data
    - Table structure
    
    Args:
        conn (sqlite3.Connection): Database connection
        
    Returns:
        dict: Dictionary containing database statistics
    """
    try:
        cursor = conn.cursor()
        
        # Get total record count
        cursor.execute("SELECT COUNT(*) FROM defillama_metrics")
        total_records = cursor.fetchone()[0]
        
        # Get unique tickers
        cursor.execute("SELECT DISTINCT ticker FROM defillama_metrics")
        tickers = [row[0] for row in cursor.fetchall()]
        
        # Get date range
        cursor.execute("""
            SELECT 
                MIN(timestamp) as earliest_date,
                MAX(timestamp) as latest_date
            FROM defillama_metrics
        """)
        date_range = cursor.fetchone()
        
        # Get table schema
        cursor.execute("PRAGMA table_info(defillama_metrics)")
        columns = cursor.fetchall()
        
        info = {
            'total_records': total_records,
            'tickers': tickers,
            'earliest_date': date_range[0],
            'latest_date': date_range[1],
            'columns': [col[1] for col in columns]  # Column names
        }
        
        print("📊 Database Information:")
        print(f"   • Total records: {info['total_records']}")
        print(f"   • Tickers: {', '.join(info['tickers'])}")
        print(f"   • Date range: {info['earliest_date']} to {info['latest_date']}")
        print(f"   • Columns: {', '.join(info['columns'])}")
        
        return info
        
    except Exception as e:
        print(f"❌ Error getting database info: {e}")
        return None

def extract_all_data(conn):
    """
    Step 3: Extract all historical data from the database
    
    This function creates a pandas DataFrame containing all historical
    metrics data. The data includes:
    - Timestamp of each measurement
    - Ticker/protocol name
    - Price (if available)
    - Market cap
    - Annualized revenue
    - P/E ratio
    
    Args:
        conn (sqlite3.Connection): Database connection
        
    Returns:
        pandas.DataFrame: Complete historical dataset
    """
    try:
        # Query all data ordered by timestamp (newest first)
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
        
        # Read data into pandas DataFrame
        df = pd.read_sql_query(query, conn)
        
        # Convert timestamp to datetime for better analysis
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        print(f"✅ Successfully extracted {len(df)} records")
        print(f"   • Data shape: {df.shape}")
        print(f"   • Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error extracting data: {e}")
        return None

def analyze_data(df):
    """
    Step 4: Perform basic analysis on the extracted data
    
    This function provides insights into the data including:
    - Summary statistics
    - Data quality checks
    - Time series analysis
    - Missing value analysis
    
    Args:
        df (pandas.DataFrame): Historical data DataFrame
    """
    print("\n📈 Data Analysis:")
    print("=" * 50)
    
    # Basic info
    print(f"Dataset shape: {df.shape}")
    print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
    
    # Missing values
    print("\n🔍 Missing Values Analysis:")
    missing_data = df.isnull().sum()
    for column, missing_count in missing_data.items():
        percentage = (missing_count / len(df)) * 100
        print(f"   • {column}: {missing_count} missing ({percentage:.1f}%)")
    
    # Summary statistics for numeric columns
    print("\n📊 Summary Statistics:")
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    if len(numeric_columns) > 0:
        print(df[numeric_columns].describe())
    
    # Time series insights
    print("\n⏰ Time Series Analysis:")
    print(f"   • Time span: {(df['timestamp'].max() - df['timestamp'].min()).total_seconds() / 3600:.1f} hours")
    print(f"   • Records per ticker:")
    ticker_counts = df['ticker'].value_counts()
    for ticker, count in ticker_counts.items():
        print(f"     - {ticker}: {count} records")

def create_analysis_dataframe(df):
    """
    Step 5: Create enhanced DataFrame with additional analysis columns
    
    This function adds useful derived columns for analysis:
    - Time-based features
    - Change calculations
    - Rolling statistics
    
    Args:
        df (pandas.DataFrame): Original historical data
        
    Returns:
        pandas.DataFrame: Enhanced DataFrame with analysis columns
    """
    # Create a copy to avoid modifying original
    analysis_df = df.copy()
    
    # Sort by ticker and timestamp for proper calculations
    analysis_df = analysis_df.sort_values(['ticker', 'timestamp'])
    
    # Add time-based features
    analysis_df['date'] = analysis_df['timestamp'].dt.date
    analysis_df['hour'] = analysis_df['timestamp'].dt.hour
    analysis_df['minute'] = analysis_df['timestamp'].dt.minute
    
    # Calculate changes (for numeric columns)
    numeric_columns = ['market_cap', 'annualized_revenue', 'pe_ratio']
    
    for column in numeric_columns:
        if column in analysis_df.columns:
            # Calculate absolute change
            analysis_df[f'{column}_change'] = analysis_df.groupby('ticker')[column].diff()
            
            # Calculate percentage change
            analysis_df[f'{column}_pct_change'] = analysis_df.groupby('ticker')[column].pct_change() * 100
    
    print("✅ Enhanced DataFrame created with analysis columns")
    print(f"   • Original columns: {list(df.columns)}")
    print(f"   • New columns: {[col for col in analysis_df.columns if col not in df.columns]}")
    
    return analysis_df

def save_dataframe(df, filename='historical_data.csv'):
    """
    Step 6: Save the DataFrame to CSV for external analysis
    
    Args:
        df (pandas.DataFrame): DataFrame to save
        filename (str): Output filename
    """
    try:
        df.to_csv(filename, index=False)
        print(f"✅ DataFrame saved to: {filename}")
        print(f"   • File size: {os.path.getsize(filename) / 1024:.2f} KB")
    except Exception as e:
        print(f"❌ Error saving DataFrame: {e}")

def main():
    """
    Main function that orchestrates the entire data extraction process
    """
    print("🚀 DefiLlama Historical Data Extraction")
    print("=" * 50)
    
    # Step 1: Connect to database
    conn = connect_to_database()
    if conn is None:
        return
    
    try:
        # Step 2: Get database information
        db_info = get_database_info(conn)
        if db_info is None:
            return
        
        # Step 3: Extract all data
        df = extract_all_data(conn)
        if df is None:
            return
        
        # Step 4: Analyze the data
        analyze_data(df)
        
        # Step 5: Create enhanced analysis DataFrame
        analysis_df = create_analysis_dataframe(df)
        
        # Step 6: Save to CSV
        save_dataframe(analysis_df)
        
        # Return the DataFrames for further use
        print("\n🎉 Data extraction complete!")
        print("You can now use 'df' for raw data and 'analysis_df' for enhanced analysis")
        
        return df, analysis_df
        
    finally:
        conn.close()
        print("🔌 Database connection closed")

if __name__ == "__main__":
    # Execute the main function and get the DataFrames
    raw_df, analysis_df = main()
    
    # Make DataFrames available for interactive use
    if raw_df is not None and analysis_df is not None:
        print("\n📋 DataFrames available:")
        print("   • raw_df: Original historical data")
        print("   • analysis_df: Enhanced data with analysis columns")
        
        # Show sample of the data
        print("\n📄 Sample of raw data:")
        print(raw_df.head())
        
        print("\n📄 Sample of analysis data:")
        print(analysis_df.head()) 