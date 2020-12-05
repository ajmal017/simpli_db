import typing

class TaskContext:
    """
    Global State Context for Tasks

    각 task에 정의되어 있는 middleware step functions에서 globally access할 수 있는 state context
    """
    def __init__(self, task: typing.Callable = None, ctx: dict = {}, stop_step: int or str = None, skip_steps: list = [], production: bool = True,
                 get_history: bool = True, silence_error: bool = False, **kwargs):
        """
        :param task: TaskContext를 사용할 최상위 함수
        :param ctx: investment universe와 같은 함수마다 꼭 필요한 global state 값
        :param stop_step: 몇번째 혹은 무슨 함수에서 task를 중지시킬지 (None이면 도중 stop X)
        :param skip_steps: 리스트 형식으로 몇번째 혹은 무슨 함수를 실행시키지 않을지
        :param production: True면 stop_step, skip_steps, get_history, silence_error를 모두 무시하고 필요한 step만 실행
        :param get_history: 각 step별 리턴값을 history로 모아서 리턴할지 말지
        :param silence_error: error가 발생해도 history에 traceback msg만 남기고 넘길지 raise error할지
        :param kwargs:
        """
        self.task = task
        self.ctx = ctx
        self.stop_step = stop_step
        self.skip_steps = skip_steps
        self.production = production
        self.get_history = get_history
        self.silence_error = silence_error
        self.kwargs = kwargs
        self.history = []

    @property
    def keys(self):
        return list(self.__dict__.keys())

    @property
    def dict(self):
        return self.__dict__

    def add_history(self, taskname: str, status: str, duration: float, input_values: list, output_values: list):
        self.history.append({
            'name': taskname,
            'status': status,
            'duration': duration,
            'input': input_values,
            'output': output_values
        })