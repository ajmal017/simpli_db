from tasks.app import app
from core.runner import task_runner
from steps.data import get_data, concat
from datasource.nasdaq import make_nasdaq_listings

@app.task(name='simpli.collect_data')
@task_runner
def collect_data(ctx={}, stop_step=None, skip_steps=[], production=True, get_history=True, silence_error=False,
                 tickers: list = []) -> int:
    return [get_data, concat]

@app.task(name='simpli.update_stock_listings')
@task_runner
def update_stock_listings(ctx={}, stop_step=None, skip_steps=[], production=True, get_history=True, silence_error=False):
    return [
        make_nasdaq_listings
    ]