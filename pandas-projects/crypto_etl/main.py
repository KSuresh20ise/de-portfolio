from config import URL
from extract import extract
from transform import transform
from load import load
from logger import logger


def main():

    logger.info("=================== ETL Pipeline Started ==================")

    # Extract
    data = extract(URL)

    if data is None:
        logger.error("ETL stopped: extraction failed")
        return

    # Transform
    df = transform(data)

    if df is None:
        logger.error("ETL stopped: transformation failed")
        return

    # Load
    success = load(df)

    if not success:
        logger.error("ETL stopped: loading failed")
        return

    logger.info("=================== ETL Pipeline Completed ==================")


if __name__ == "__main__":
    main()