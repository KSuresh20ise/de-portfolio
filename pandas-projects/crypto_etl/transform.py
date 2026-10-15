import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


def transform(data):

    logger.info("Starting data transformation")

    try:
        df_raw = pd.DataFrame(data)

        logger.info(f"{len(df_raw)} raw records extracted")
        logger.info("Performing data transformation")

        required_columns = [
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
        ]

        missing_columns = set(required_columns) - set(df_raw.columns)

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {missing_columns}"
            )

        df = df_raw[required_columns].copy()

        # Remove duplicate coins
        before = len(df)

        df = df.drop_duplicates(subset=["id"])

        duplicates_removed = before - len(df)

        logger.info(f"Duplicates removed: {duplicates_removed}")

        # Convert numeric columns
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

        for column in numeric_columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

        # Clean text
        df["symbol"] = df["symbol"].str.upper()
        df["name"] = df["name"].str.strip()

        # Rename columns
        df = df.rename(columns={
            "current_price": "price",
            "total_volume": "volume",
            "price_change_percentage_24h": "price_change_pct_24h"
        })

        # Rule-based classification
        df["indicator"] = np.where(
            df["price_change_pct_24h"] > 2,
            "Buy",
            np.where(
                df["price_change_pct_24h"] >= 0,
                "Hold",
                "Sell"
            )
        )

        df["last_updated"] = pd.to_datetime(
            df["last_updated"],
            utc=True
        ).dt.tz_localize(None)
        
        df["ingestion_timestamp"] = pd.Timestamp.now()

        logger.info(
            f"Transformation successful: {len(df)} records"
        )

        return df

    except Exception:
        logger.exception("Data transformation failed")
        return None