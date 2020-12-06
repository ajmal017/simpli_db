from tasks.app import app
from core.runner import task_runner
from datasource import get_listings
from steps import print_listings

@app.task(name='simpli.make_supported_code_list')
@task_runner
def make_supported_code_list(ctx={}, stop_step=None, skip_steps=[], production=True, get_history=True, silence_error=False):
    return [
        get_listings,
        print_listings
    ]