import datetime
from decimal import Decimal
import numpy as np
import polars as pl
from ziplime.domain.bar_data import BarData
from ziplime.finance.execution import MarketOrder
from ziplime.trading.trading_algorithm import TradingAlgorithm


async def initialize(context):
    context.sber = await context.symbol("SBER")

async def handle_data(context, data):
    print(f"simulating {context.simulation_dt}")
    window = 20
    df_sber = data.history(assets=[context.sber], fields=["close"], bar_count=window)
    print(df_sber)
    await context.order(asset=context.sber, amount=1, style=MarketOrder())
