import os
import json
from Naked.toolshed.shell import muterun_js

__DIRNAME__ = os.path.dirname(os.path.abspath(__file__))

"""
Fnguide는 동시 접속이 불가능!

절대로 비동기/병렬로 데이터 요청 보내지말고 한번에 한개의 요청만 보내기 주의
"""

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