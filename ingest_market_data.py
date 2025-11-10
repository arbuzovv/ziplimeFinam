import asyncio
import datetime
import logging
import os
import pathlib

import pytz

from ziplime.core.ingest_data import get_asset_service, ingest_market_data
from ziplime.data.data_sources.grpc.grpc_data_source import GrpcDataSource
from ziplime.data.data_sources.limex_hub_asset_data_source import LimexHubAssetDataSource
from ziplime.utils.logging_utils import configure_logging

import os
os.environ['GRPC_TOKEN'] = 'your_finam_trade_api_token'
os.environ['GRPC_SERVER_URL'] = 'api.finam.ru:443'


async def _ingest_data_grpc():
    asset_service = get_asset_service(
        clear_asset_db=False
    )

    symbols = ["SBER@MISX"]

    start_date = datetime.datetime(year=2025, month=1, day=1, tzinfo=pytz.timezone("America/New_York"))
    end_date = datetime.datetime(year=2025, month=9, day=18, tzinfo=pytz.timezone("America/New_York"))
    market_data_bundle_source = GrpcDataSource.from_env()
    await market_data_bundle_source.get_token()

    await ingest_market_data(
        start_date=start_date,
        end_date=end_date,
        symbols=symbols,
        trading_calendar="NYSE",
        bundle_name="grpc_daily_data",
        data_bundle_source=market_data_bundle_source,
        data_frequency=datetime.timedelta(days=1),
        asset_service=asset_service
    )


if __name__ == "__main__":
    configure_logging(level=logging.INFO, file_name="mylog.log")
    asyncio.run(_ingest_data_grpc())