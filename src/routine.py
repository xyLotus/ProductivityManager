from utils import time_input_stream


class Routine:
    '''Stores all time, name-ID and description of a routine.'''
    def __init__(self, time: str, title: str, desc: str):
        time_input_stream(time)

        self.time = time
        self.title = title
        self.desc = desc

    time: str # Format => (16:30 | 16:00 | 16)
    title: str
    desc: str
    
    def __repr__(self):
        return f'Routine({self.time}, {self.title}, {self.desc})'

    def __str__(self):
        return self.wrap()

    def wrap(self):
        return f'{self.time}//////{self.title}//////{self.desc}'

    @staticmethod
    def unwrap(r_wrapped: str) -> list:
        '''Returns a list with the length of 3,
        index 0: time
        index 1: title
        index 2: desc.'''
        r = r_wrapped.split('//////')
        if len(r) != 3:
            raise ValueError
        
        return r

    @staticmethod
    def from_wrapped(r_wrapped: str):
        '''Returns a instance of the routine class,
        with input of the wrapped routine fromat.'''
        r_unwrapped = Routine.unwrap(r_wrapped)
        return Routine(
            time=r_unwrapped[0],
            title=r_unwrapped[1],
            desc=r_unwrapped[2]
        )
