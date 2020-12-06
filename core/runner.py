import time
import inspect
import asyncio
import traceback
from functools import wraps

from core.context import TaskContext
from core.tree import TaskTree

def task_runner(func):
    signature = inspect.signature(func)

    @wraps(func)
    def call(*args, **kwargs):
        bound_arguments = signature.bind(*args, **kwargs)
        bound_arguments.apply_defaults()
        kwargs = bound_arguments.arguments
        extra = bound_arguments.kwargs

        tasks_list = func(*args, **kwargs)

        kwargs['task'] = func
        tc = TaskContext(**kwargs, **extra)
        tt = TaskTree(tasks_list, context=tc)

        if tt.traverse_check():
            info = tt.info
            params = {key: val for key, val in kwargs.items() if key not in tc.keys}
            for i in range(len(info.keys())):
                if info[i]['skip'] or (i == 0):
                    continue
                try:
                    start = time.time()
                    if type(params) == dict:
                        res = info[i]['function'](**params, ctx=tc.ctx)
                    elif type(params) == tuple:
                        res = info[i]['function'](*params, ctx=tc.ctx)
                    else:
                        res = info[i]['function'](params, ctx=tc.ctx)
                    if inspect.iscoroutinefunction(info[i]['function']):
                        res = asyncio.run(res)
                    end = time.time()
                    tc.add_history(info[i]['name'], 'SUCCESS', end - start, params, res)
                    params = res
                except Exception as e:
                    tc.add_history(info[i]['name'], 'FAILED', None, params, traceback.format_exc())
                    if (not tc.silence_error) or tc.production:
                        raise e
                if info[i]['exit']:
                    break
        if tc.get_history and (not tc.production):
            return res, tc.history
        else:
            return res
    return call