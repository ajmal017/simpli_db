import copy
import typing

from core.context import TaskContext

class TaskTree:
    def __init__(self, tasks_list: list = [], context: TaskContext = None):
        self.tasks_list = tasks_list
        self.context = context
        self.info_dict = None

    @property
    def task_cnt(self):
        return len(self.tasks_list)

    def _func_annotations(self, func):
        ann = copy.deepcopy(func.__annotations__)
        output_ann = ann.pop('return', None)
        output_ann = list(output_ann) if type(output_ann) == tuple else output_ann
        output_ann = [output_ann] if type(output_ann) != list else output_ann
        input_ann = list(ann.values())
        return input_ann, output_ann

    def _func_dimensions(self, input_ann, output_ann):
        input_dim = len(input_ann)
        if type(output_ann) == list:
            output_dim = len(output_ann)
        else:
            output_dim = 1
        return input_dim, output_dim

    def _add_task_info(self, idx: int, task: typing.Callable):
        production = self.context.production
        stop_step = self.context.stop_step
        skip_steps = self.context.skip_steps

        taskname = task.__name__
        step_info = [idx, taskname]
        in_ann, out_ann = self._func_annotations(task)
        in_dim, out_dim = self._func_dimensions(in_ann, out_ann)
        self.info_dict[idx] = {
            'name': taskname,
            'function': task,
            'type': [in_ann, out_ann] if idx != 0 else [in_ann, in_ann], # 첫 step은 parent함수의 인풋을 그대로 첫 번째 함수로 보내주는 역할
            'dimension': [in_dim, out_dim] if idx != 0 else [in_dim, in_dim],
            'skip': True if ((idx in skip_steps) or (taskname in skip_steps)) else False,
            'exit': True if ((stop_step in step_info) and (not production)) else False
        }

    @property
    def info(self):
        if isinstance(self.info_dict, type(None)):
            self.info_dict = {}
            self._add_task_info(0, self.context.task)
            for i in range(len(self.tasks_list)):
                self._add_task_info(i + 1, self.tasks_list[i])
        return self.info_dict

    def traverse_check(self):
        """
        task pipeline에서 step by step input / output의 size와 type이 일치하는지 확인
        context.stop_step과 context.skip_steps를 파악하여 실제로 실행시키는 함수에 대해서만 테스트 진행
        마지막 step의 결과값은 무조건 output 개수가 1개
        """
        info = self.info
        task_started = False
        for idx, _ in enumerate(self.tasks_list):
            on_task = info[idx + 1]['name']
            if (not task_started) and (not info[idx + 1]['skip']):
                task_started = True
            if task_started and (not info[idx + 1]['skip']):
                prev_output_type = info[idx]['type'][1]
                curr_input_type = info[idx + 1]['type'][0]
                prev_output_dimension = info[idx]['dimension'][1]
                curr_input_dimension = info[idx + 1]['dimension'][0]
                if prev_output_type != curr_input_type:
                    raise Exception(f'{on_task}: Input/Output 타입이 다릅니다. (Hint: should be {prev_output_type})')
                if prev_output_dimension != curr_input_dimension:
                    raise Exception(f'{on_task}: Input/Output dimension 사이즈가 다릅니다. (Hint: should be {prev_output_dimension})')
            if info[idx + 1]['exit']:
                break
        return True