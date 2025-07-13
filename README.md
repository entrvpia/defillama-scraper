# DeFiLlama Scraper

A Python-based web scraper for collecting DeFi (Decentralized Finance) data from DeFiLlama. This project uses Scrapy framework to extract historical and real-time data from various DeFi protocols.

## 🚀 Features

- **Real-time Data Collection**: Scrapes current DeFi protocol data
- **Historical Data Extraction**: Collects historical TVL (Total Value Locked) data
- **Database Storage**: Stores data in SQLite database for analysis
- **Data Analysis Tools**: Includes utilities for querying and analyzing collected data
- **HyperLiquid Integration**: Specialized scraper for HyperLiquid protocol

## 📋 Prerequisites

- Python 3.9+
- pip (Python package installer)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd defillama-scraper
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 📁 Project Structure

```
defillama-scraper/
├── defillama/                 # Scrapy spider project
│   ├── spiders/
│   │   └── defillama_spider.py
│   ├── items.py
│   └── pipelines.py
├── extract_historical_data.py # Historical data extraction
├── load_dataframe.py         # Data loading utilities
├── query_database.py         # Database query tools
├── scrape_hyperliquid.py    # HyperLiquid specific scraper
├── df_database.py           # Database operations
├── scrapy.cfg              # Scrapy configuration
└── README.md               # This file
```

## 🎯 Usage

### 1. Basic Scraping

Run the main DeFiLlama spider:
```bash
cd defillama
scrapy crawl defillama_spider
```

### 2. Historical Data Extraction

Extract historical TVL data:
```bash
python extract_historical_data.py
```

### 3. HyperLiquid Data

Scrape HyperLiquid specific data:
```bash
python scrape_hyperliquid.py
```

### 4. Database Queries

Query the collected data:
```bash
python query_database.py
```

## 📊 Data Analysis

The project includes several analysis tools:

- **Data Loading**: `load_dataframe.py` - Load data into pandas DataFrames
- **Database Queries**: `query_database.py` - Query stored data
- **Historical Analysis**: Extract and analyze historical trends

## 🗄️ Database

Data is stored in a local SQLite database (`defillama_data.db`). The database contains:

- Protocol information
- TVL (Total Value Locked) data
- Historical trends
- Timestamp information

## 🔧 Configuration

### Scrapy Settings

Edit `defillama/settings.py` to configure:
- Request delays
- User agents
- Pipeline settings
- Database connections

### Database Configuration

Database settings are in `df_database.py`:
- Database path
- Table schemas
- Connection parameters

## 📈 Data Output

The scraper collects various DeFi metrics:

- **TVL (Total Value Locked)**: Total value locked in protocols
- **Protocol Information**: Names, categories, chains
- **Historical Data**: Time-series data for trend analysis
- **Market Data**: Price and volume information

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Important Notes

- **Rate Limiting**: Respect DeFiLlama's rate limits
- **Data Usage**: Use data responsibly and in accordance with DeFiLlama's terms
- **Database**: The database file is excluded from version control for privacy

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Make sure virtual environment is activated
2. **Database Errors**: Check if database file exists and has proper permissions
3. **Scraping Errors**: Verify internet connection and DeFiLlama availability

### Debug Mode

Enable debug logging:
```bash
scrapy crawl defillama_spider -L DEBUG
```

## 📞 Support

For issues and questions:
- Create an issue in the repository
- Check the documentation in the code comments
- Review the analysis guides in the project

## 🔄 Updates

This scraper is designed to work with DeFiLlama's current structure. If DeFiLlama changes their website structure, the spiders may need updates.

---

**Note**: This project is for educational and research purposes. Always respect the terms of service of the websites you scrape. 