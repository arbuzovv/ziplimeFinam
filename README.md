# Ziplime Adapter for Finam 🔌

Адаптер для интеграции брокера Финам с бэктестинг-фреймворком [ziplime](https://github.com/limex-com/ziplime).

Позволяет:
- Получать и сохранять справочник инструментов
- Загружать исторические данные в локальный бандл
- Запускать торговые алгоритмы на исторических данных

---

## Установка

```bash
pip install ziplime
```

## Быстрый старт

#### 1. Получение справочника инструментов

См. пример: [ingest_assets.py](https://github.com/arbuzovv/ziplimeFinam/blob/main/ingest_assets.py)
```bash
from ziplime.core.ingest_data import get_asset_service, ingest_assets
from ziplime.data.data_sources.grpc.grpc_asset_data_source import GrpcAssetDataSource

import os
os.environ['GRPC_TOKEN'] = 'ВАШ_API_TOKEN'
os.environ['GRPC_SERVER_URL'] = 'api.finam.ru:443'

asset_data_source = GrpcAssetDataSource.from_env()
asset_service = get_asset_service(clear_asset_db=True)
ingest_assets(asset_service=asset_service, asset_data_source=asset_data_source)
```

#### 2. Загрузка исторических данных в бандл


См. пример: [ingest_market_data.py](https://github.com/arbuzovv/ziplimeFinam/blob/main/ingest_market_data.py)
```bash
import datetime
import pytz
from ziplime.core.ingest_data import get_asset_service, ingest_market_data
from ziplime.data.data_sources.grpc.grpc_data_source import GrpcDataSource

import os
os.environ['GRPC_TOKEN'] = 'ВАШ_API_TOKEN'
os.environ['GRPC_SERVER_URL'] = 'api.finam.ru:443'


asset_service = get_asset_service(clear_asset_db=False)
symbols = ["SBER@MISX"]
start_date = datetime.datetime(2025, 1, 1, tzinfo=pytz.timezone("America/New_York"))
end_date = datetime.datetime(2025, 9, 18, tzinfo=pytz.timezone("America/New_York"))
market_data_bundle_source = GrpcDataSource.from_env()
market_data_bundle_source.get_token()
ingest_market_data(
        start_date=start_date,
        end_date=end_date,
        symbols=symbols,
        trading_calendar="NYSE",
        bundle_name="grpc_daily_data",
        data_bundle_source=market_data_bundle_source,
        data_frequency=datetime.timedelta(days=1),
        asset_service=asset_service
    )
```

#### 3. Запуск торгового алгоритма

См. пример: [run_backtest.py](https://github.com/arbuzovv/ziplimeFinam/blob/main/run_backtest.py)
```bash
import asyncio
import datetime
import polars as pl
import structlog
import pytz
from ziplime.core.ingest_data import get_asset_service
from ziplime.core.run_simulation import run_simulation
from ziplime.data.services.bundle_service import BundleService
from ziplime.data.services.file_system_bundle_registry import FileSystemBundleRegistry
from pathlib import Path

async def _run_simulation():
    bundle_storage_path = str(Path(Path.home(), ".ziplime", "data"))
    bundle_registry = FileSystemBundleRegistry(base_data_path=bundle_storage_path)
    bundle_service = BundleService(bundle_registry=bundle_registry)
    asset_service = get_asset_service(clear_asset_db=False)
    symbols = ["SBER@XNYM"]
    ny = pytz.timezone("America/New_York")
    start_date = ny.localize(datetime.datetime(2025, 9, 1))
    end_date = ny.localize(datetime.datetime(2025, 9, 17))
    aggregations = [
        pl.col("open").first(),
        pl.col("high").max(),
        pl.col("low").min(),
        pl.col("close").last(),
        pl.col("volume").sum(),
        pl.col("symbol").last()
    ]
    market_data_bundle = await bundle_service.load_bundle(
        bundle_name="grpc_daily_data",
        bundle_version=None,
        frequency=datetime.timedelta(days=1),
        start_date=start_date,
        end_date=end_date + datetime.timedelta(days=1),
        symbols=symbols,
        aggregations=aggregations
    )
    res, errors = await run_simulation(
        start_date=start_date,
        end_date=end_date,
        trading_calendar='NYSE',
        algorithm_file='/path/to/your/algo.py',
        total_cash=100000.0,
        market_data_source=market_data_bundle,
        custom_data_sources=[],
        config_file='/path/to/your/algo.json',
        emission_rate=datetime.timedelta(days=1),
        benchmark_asset_symbol="SBER",
        benchmark_returns=None,
        stop_on_error=False,
        asset_service=asset_service
    )
    if errors:
        print(errors)
    print(res.head(n=10).to_markdown())
```
#### 4. Примеры алгоритмов в папке алго

Обычно указываются 2 файла:

- [algo.py](https://github.com/arbuzovv/ziplimeFinam/blob/main/algo/algo.py) - сам код торгового алгоритма

- [algo.json](https://github.com/arbuzovv/ziplimeFinam/blob/main/algo/algo.json) - конфиг, когда необходимо управлять алгоритмом более гибко


### Требования

Python 3.9+

Доступ к API Finam (GRPC_TOKEN)

ziplime
