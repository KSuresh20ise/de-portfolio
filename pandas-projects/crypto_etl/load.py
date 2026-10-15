from sqlalchemy import create_engine
from config import DATABASE, USER_NAME, PASSWORD
import logging

logger = logging.getLogger(__name__)

def load(df):

    logger.info("Data loading started")

    try:
        engine = create_engine(
            f"mysql+mysqlconnector://{USER_NAME}:{PASSWORD}@localhost/{DATABASE}"
        )

        with engine.begin() as con:

            logger.info("Database connection successful")

            df.to_sql(
                "crypto_data",
                con=con,
                if_exists="append",
                index=False
            )

            logger.info(
                f"{len(df)} records loaded into database successfully"
            )

        return True

    except Exception:
        logger.exception("Data loading failed")
        return False