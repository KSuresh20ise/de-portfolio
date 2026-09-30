from config import *
from extract import extract
from transform import transform
from logger import logger

def main():

    logger.info("=================== ETL Pipeline Started ==================")

    # Extract
    data = extract(URL)

    if data is None:
        logger.error("ETL Stopped: extraction failed")
        return

    # Transform

    df = transform(data)

    if df is None:
        logger.error("ETL stopped: transformation failed")
        return
    print(df)

    logger.info("========== ETL Pipeline Completed ==========")
    
if __name__ == "__main__":
    main()