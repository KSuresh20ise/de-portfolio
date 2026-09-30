import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

def transform(data):

    logger.info("Starting data transformation")

    try:
        df_raw = pd.DataFrame(data)
        logger.info(f"{len(df_raw)} raw records extracted")
        logger.info("Perfroming Data Transformation")

        # Required columns
        df = df_raw[[
            "id",
            "symbol",
            "name",
            "current_price",
            "market_cap",
            "market_cap_rank",
            "total_volume",
            "high_24h",
            "low_24h",
            "price_change_24h",
            "price_change_percentage_24h",
            "circulating_supply",
            "last_updated"
        ]]

        # Remove duplicate coins
        df.drop_duplicates(subset=["id"],inplace=True)

        numeric_columns = [
                "current_price",
                "market_cap",
                "market_cap_rank",
                "total_volume",
                "high_24h",
                "low_24h",
                "price_change_24h",
                "price_change_percentage_24h",
                "circulating_supply"
         ]
        # convert numeric columns
        for column in numeric_columns:
            df[column] = pd.to_numeric(df[column],
                errors="coerce"                      
            )

        # Capitalize symbol
        df["symbol"] = df["symbol"].str.upper()

        # Rename columns
        df.rename(columns={
            "current_price": "price",
            "total_volume": "volume",
            "price_change_percentage_24h": "price_change_pct_24h"
        }, inplace=True)

        # Remove spaces
        df["name"] = df["name"].str.strip()

        # Indicator

        df["indicator"] = np.where(
            df["price_change_pct_24h"]>2,"Buy",
            np.where(
                df["price_change_pct_24h"]>=0,"Hold","Sell"
            )
        )
         
        logger.info(f"Transformation successful: {len(df)} records")

        return df

    except Exception:
        logger.exception("Data transformation failed")
        return None