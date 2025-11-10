import asyncio
import logging

from ziplime.core.ingest_data import get_asset_service, ingest_assets
from ziplime.data.data_sources.grpc.grpc_asset_data_source import GrpcAssetDataSource
from ziplime.utils.logging_utils import configure_logging

import os
os.environ['GRPC_TOKEN'] = 'your_finam_trade_api_token'
os.environ['GRPC_SERVER_URL'] = 'api.finam.ru:443'



async def ingest_assets_data_grpc():
    asset_data_source = GrpcAssetDataSource.from_env()
    asset_service = get_asset_service(
        clear_asset_db=True,
    )
    await ingest_assets(asset_service=asset_service, asset_data_source=asset_data_source)


if __name__ == "__main__":    
    asyncio.run(ingest_assets_data_grpc())
    
    
    
    