# 🚀 Crypto ETL Pipeline

A production-style **Python ETL pipeline** that extracts cryptocurrency
market data from the CoinGecko API, transforms and validates the data
using Pandas, and loads the cleaned dataset into a MySQL database.

The project demonstrates core **Data Engineering concepts** such as API
ingestion, data cleaning, validation, deduplication, environment-based
configuration, database loading, logging, error handling, and modular
ETL design.

------------------------------------------------------------------------

## 📌 Project Overview

This project follows a simple and maintainable ETL architecture:

``` text
                 CoinGecko API
                       │
                       ▼
                ┌─────────────┐
                │   EXTRACT   │
                │  requests   │
                └──────┬──────┘
                       │
                       ▼
                ┌─────────────┐
                │  TRANSFORM  │
                │   Pandas    │
                │  NumPy      │
                └──────┬──────┘
                       │
                       ▼
                ┌─────────────┐
                │    LOAD     │
                │ SQLAlchemy  │
                │    MySQL    │
                └──────┬──────┘
                       │
                       ▼
                 MySQL Database
```

The pipeline can be executed from a single entry point:

``` bash
python main.py
```

------------------------------------------------------------------------

## ✨ Features

-   🔌 Extracts cryptocurrency market data from CoinGecko API
-   🔐 Stores API keys and database credentials in `.env`
-   🧹 Cleans and standardizes raw API data
-   🔢 Converts numeric fields to appropriate data types
-   ♻️ Removes duplicate cryptocurrency records
-   🔍 Validates required columns during transformation
-   📊 Uses Pandas DataFrames for data processing
-   🗄️ Loads transformed data into MySQL
-   🔄 Uses SQLAlchemy for database connectivity
-   📝 Implements application-level logging
-   🚨 Handles API, transformation, and database failures
-   ⏱️ Uses HTTP request timeouts to avoid indefinitely waiting for an
    API
-   🧩 Separates Extract, Transform, Load responsibilities into modules
-   🔁 Returns success/failure status from the loading stage
-   🔒 Keeps secrets out of source code

------------------------------------------------------------------------

## 🛠️ Tech Stack

  Technology                   Purpose
  ---------------------------- --------------------------------------
  **Python**                   Core programming language
  **Requests**                 API communication
  **Pandas**                   Data transformation
  **NumPy**                    Derived-column logic
  **python-dotenv**            Environment variable management
  **SQLAlchemy**               Database connection and transactions
  **MySQL**                    Data storage
  **mysql-connector-python**   MySQL database driver
  **Logging**                  Pipeline monitoring and debugging
  **Git/GitHub**               Version control

------------------------------------------------------------------------

## 📂 Project Structure

``` text
crypto_etl/
│
├── .env                    # Local secrets/configuration (not committed)
├── .gitignore              # Git exclusions
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
│
├── config.py               # Environment variables and API configuration
├── extract.py              # API extraction
├── transform.py            # Data cleaning and transformation
├── load.py                 # MySQL loading
├── logger.py               # Logging configuration
├── main.py                 # ETL pipeline entry point
│
├── crypto_etl.ipynb        # Development/experimentation notebook
│
└── logs/
    └── etl.log            # Runtime logs (normally ignored by Git)
```

------------------------------------------------------------------------

## 🔄 ETL Workflow

### 1. Extract

`extract.py` sends a request to the CoinGecko API using configured
headers and query parameters.

The extraction layer:

-   Sends the API request
-   Records the HTTP status code
-   Uses a request timeout
-   Validates the HTTP response
-   Converts the JSON response into Python data
-   Logs failures with a traceback
-   Returns `None` when extraction fails

Example:

``` python
response = requests.get(
    url,
    headers=headers,
    params=params,
    timeout=30
)

response.raise_for_status()
data = response.json()
```

------------------------------------------------------------------------

### 2. Transform

`transform.py` converts the raw API response into a structured Pandas
DataFrame.

The transformation process includes:

1.  Selecting required columns
2.  Validating required columns
3.  Removing duplicate cryptocurrencies using `id`
4.  Converting numeric fields using `pd.to_numeric()`
5.  Standardizing symbols to uppercase
6.  Removing unnecessary whitespace
7.  Renaming columns
8.  Creating a derived indicator column
9.  Logging transformation results

Example transformations:

``` text
current_price
      ↓
price

total_volume
      ↓
volume

price_change_percentage_24h
      ↓
price_change_pct_24h
```

The project also demonstrates rule-based classification:

``` text
price_change_pct_24h > 2%   → Buy
0% to 2%                    → Hold
price_change_pct_24h < 0%   → Sell
```

> The indicator is included as a demonstration of derived business
> logic. It is not intended to constitute financial advice or a trading
> recommendation.

------------------------------------------------------------------------

### 3. Load

`load.py` receives the transformed DataFrame and loads it into MySQL.

The loading stage:

-   Creates a SQLAlchemy engine
-   Establishes a database connection
-   Uses a transaction
-   Writes the DataFrame to MySQL
-   Appends records to the target table
-   Logs the number of records loaded
-   Returns `True` on success and `False` on failure

Example:

``` python
with engine.begin() as con:
    df.to_sql(
        "crypto_data",
        con=con,
        if_exists="append",
        index=False
    )
```
------------------------------------------------------------------------

## 🧠 Data Transformation

The pipeline works with fields such as:

``` text
id
symbol
name
price
market_cap
market_cap_rank
volume
high_24h
low_24h
price_change_24h
price_change_pct_24h
circulating_supply
last_updated
indicator
```

### Data quality operations

  Operation                    Purpose
  ---------------------------- -----------------------------------------
  Required-column validation   Detect API schema changes
  Duplicate removal            Prevent duplicate coin records
  Numeric conversion           Ensure correct database/data types
  `errors="coerce"`            Convert invalid numeric values to `NaN`
  Uppercase symbols            Standardize text
  `strip()`                    Remove unwanted whitespace
  Column renaming              Create consistent target-column names

------------------------------------------------------------------------

## 📝 Logging

The project uses Python's logging module to track pipeline execution.

Example:

``` text
2026-10-01 13:42:42,201 | INFO | load | Data loading started
2026-10-01 13:42:42,388 | INFO | load | Database connection successful
2026-10-01 13:42:42,388 | INFO | load | 250 records loaded into database successfully
2026-10-01 13:42:42,388 | INFO | logger | ========== ETL Pipeline Completed ==========
```

Logs are written to:

``` text
logs/etl.log
```

The pipeline uses `logger.exception()` when failures occur so that
useful traceback information is available for debugging.

------------------------------------------------------------------------

## 🔐 Configuration & Security

Sensitive credentials are stored in `.env` instead of being hard-coded.

Example:

``` env
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_database
API_KEY=your_api_key
```

The database password is URL-encoded before being placed in the
SQLAlchemy connection URL:

``` python
PASSWORD = quote_plus(DB_PASSWORD)
```

For example:

``` text
Raw password:
Sur@#234

URL-encoded:
Sur%40%23234
```

### Important

Never commit `.env` to GitHub.

Recommended `.gitignore`:

``` gitignore
.env
logs/
__pycache__/
*.pyc
```

A safe approach is to provide an example configuration file such as:

``` text
.env.example
```

containing placeholder values:

``` env
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_database
API_KEY=your_api_key
```

------------------------------------------------------------------------

## ⚙️ Installation

### 1. Clone the repository

``` bash
git clone <your-repository-url>
cd crypto_etl
```

### 2. Create a virtual environment

Windows:

``` powershell
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

``` bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

``` env
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_database
API_KEY=your_coingecko_api_key
```

### 5. Create the MySQL database

Example:

``` sql
CREATE DATABASE crypto_db;
```

The table can be created by the loading process when using Pandas
`to_sql()`.

------------------------------------------------------------------------

## ▶️ Running the Pipeline

Run:

``` bash
python main.py
```

Expected flow:

``` text
ETL Pipeline Started
        ↓
API request
        ↓
Data extracted
        ↓
Data transformed
        ↓
MySQL connection
        ↓
Data loaded
        ↓
ETL Pipeline Completed
```

------------------------------------------------------------------------

## 🗄️ Example MySQL Queries

View the table:

``` sql
DESC crypto_data;
```

View records:

``` sql
SELECT *
FROM crypto_data;
```

Count records:

``` sql
SELECT COUNT(*)
FROM crypto_data;
```

View selected fields:

``` sql
SELECT
    id,
    name,
    price,
    market_cap,
    price_change_pct_24h
FROM crypto_data;
```

------------------------------------------------------------------------

## 🚨 Error Handling

Each ETL stage handles failures independently.

### Extraction failure

``` text
API request fails
       ↓
extract() returns None
       ↓
main() stops the pipeline
```

### Transformation failure

``` text
Transformation error
       ↓
transform() returns None
       ↓
main() stops the pipeline
```

### Loading failure

``` text
Database/load error
       ↓
load() returns False
       ↓
main() stops the pipeline
```

The pipeline only reports:

``` text
ETL Pipeline Completed
```

when all three stages succeed.

------------------------------------------------------------------------

## 🎯 Data Engineering Concepts Demonstrated

This project demonstrates practical knowledge of:

-   ETL architecture
-   REST API ingestion
-   JSON data processing
-   Data validation
-   Data cleaning
-   Data standardization
-   Deduplication
-   Data type conversion
-   Pandas DataFrames
-   SQL databases
-   SQLAlchemy
-   Database transactions
-   Environment variables
-   Secret management
-   Logging
-   Exception handling
-   Modular Python programming
-   Git/GitHub workflow

------------------------------------------------------------------------

## 🚀 Future Improvements

Possible next steps:

-   [ ] Add automated tests with `pytest`
-   [ ] Add retry logic for temporary API failures
-   [ ] Add API pagination
-   [ ] Add data-quality checks
-   [ ] Add database primary keys and indexes
-   [ ] Add an ingestion timestamp
-   [ ] Add incremental loading
-   [ ] Add Docker support
-   [ ] Add scheduled execution
-   [ ] Add Apache Airflow orchestration
-   [ ] Add cloud storage/data warehouse integration
-   [ ] Add a Power BI dashboard
-   [ ] Add CI/CD with GitHub Actions

------------------------------------------------------------------------

## 📈 Future Architecture

The project can eventually evolve from:

``` text
CoinGecko API
      ↓
Python ETL
      ↓
MySQL
```

to:

``` text
                 CoinGecko API
                       ↓
                Python Extraction
                       ↓
                 Data Validation
                       ↓
                  Data Storage
                       ↓
                Transformation
                       ↓
              Data Warehouse
                       ↓
                 Power BI
```

Or, with orchestration:

``` text
             Airflow
                │
        ┌───────┴───────┐
        ▼               ▼
    Extract          Transform
        │               │
        └───────┬───────┘
                ▼
              Load
                │
                ▼
          Data Warehouse
                │
                ▼
            Power BI
```

------------------------------------------------------------------------

## 📚 Learning Goals

This project was built to strengthen practical skills in:

**Python → APIs → Pandas → SQL → MySQL → SQLAlchemy → ETL → Logging →
Data Engineering**

The focus is on understanding how individual components work together to
create a reliable data pipeline rather than simply writing a single
script.

------------------------------------------------------------------------

## 👨‍💻 Author

**Suresh**

Aspiring Data Engineer

Skills demonstrated through this project:

``` text
Python
SQL
Pandas
REST APIs
MySQL
SQLAlchemy
ETL
Data Cleaning
Logging
Git/GitHub
```

------------------------------------------------------------------------

## ⭐ Project Summary

A modular Python ETL pipeline that collects cryptocurrency market data
from the CoinGecko API, performs data-quality and transformation
operations using Pandas, and loads the resulting dataset into MySQL with
structured logging and error handling.

The project provides a foundation that can be extended with testing,
orchestration, incremental processing, cloud services, data warehousing,
and BI tools.
