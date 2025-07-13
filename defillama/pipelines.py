import sqlite3
from datetime import datetime

class DefillamaPipeline:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.setup_database()
    
    def setup_database(self):
        """Initialize SQLite database and create table if it doesn't exist"""
        self.conn = sqlite3.connect('defillama_data.db')
        self.cursor = self.conn.cursor()
        
        # Create table with the specified structure
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS defillama_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                ticker TEXT NOT NULL,
                price REAL,
                market_cap REAL,
                annualized_revenue REAL,
                pe_ratio REAL
            )
        ''')
        self.conn.commit()
    
    def process_item(self, item, spider):
        # Store original values for P/E calculation
        original_market_cap = item.get("market_cap")
        original_annual_revenue = item.get("annual_revenue")
        
        # Basic cleaning: remove unwanted characters or format numbers for display
        for field in ["market_cap", "annual_revenue"]:
            if item.get(field) and isinstance(item[field], str):
                item[field] = item[field].replace("$", "").replace(",", "").strip()
        
        # Calculate P/E ratio using original values
        if original_market_cap and original_annual_revenue and original_market_cap != "Not found" and original_annual_revenue != "Not found":
            market_cap_num = self._convert_to_number(original_market_cap.strip())
            annual_revenue_num = self._convert_to_number(original_annual_revenue.strip())
            
            if market_cap_num and annual_revenue_num and annual_revenue_num > 0:
                pe_ratio = market_cap_num / annual_revenue_num
                item["pe_ratio"] = f"{pe_ratio:.2f}"
            else:
                item["pe_ratio"] = "Not calculable"
        else:
            item["pe_ratio"] = "Not calculable"
        
        # Store data in SQLite database
        self.store_in_database(item)
        
        return item
    
    def store_in_database(self, item):
        """Store the scraped data in SQLite database"""
        try:
            # Convert values to numbers for database storage
            market_cap_num = self._convert_to_number(item.get("market_cap", "0"))
            annual_revenue_num = self._convert_to_number(item.get("annual_revenue", "0"))
            pe_ratio_num = float(item.get("pe_ratio", "0")) if item.get("pe_ratio") != "Not calculable" else None
            
            # Insert data into database
            self.cursor.execute('''
                INSERT INTO defillama_metrics 
                (timestamp, ticker, price, market_cap, annualized_revenue, pe_ratio)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now(),
                item.get("protocol", ""),
                None,  # Price not available in current scraping
                market_cap_num,
                annual_revenue_num,
                pe_ratio_num
            ))
            self.conn.commit()
            print(f"Stored data for {item.get('protocol')} in database")
            
        except Exception as e:
            print(f"Error storing data in database: {e}")
    
    def _convert_to_number(self, value_str):
        """Convert string with 'b' or 'm' suffix to number"""
        try:
            # Remove dollar signs and clean the string
            clean_str = value_str.replace('$', '').replace(',', '').strip()
            
            if 'b' in clean_str.lower():
                return float(clean_str.lower().replace('b', '')) * 1_000_000_000
            elif 'm' in clean_str.lower():
                return float(clean_str.lower().replace('m', '')) * 1_000_000
            else:
                return float(clean_str)
        except (ValueError, AttributeError):
            return None
    
    def close_spider(self, spider):
        """Close database connection when spider finishes"""
        if self.conn:
            self.conn.close()
