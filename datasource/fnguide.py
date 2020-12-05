import os
import json
from Naked.toolshed.shell import muterun_js

__DIRNAME__ = os.path.dirname(os.path.abspath(__file__))

def _run_fnguide_file(file: str):
    filename = os.path.join(__DIRNAME__, 'fnguide', file)
    res = muterun_js(filename)
    if res.exitcode == 0:
        return True, res.stdout.decode('utf-8')
    elif res.exitcode == 1:
        raise Exception(res.stderr.decode('utf-8'))


if __name__ == '__main__':
    status, res = _run_fnguide_file('main.js')
    data = json.loads(res)
    print(data)