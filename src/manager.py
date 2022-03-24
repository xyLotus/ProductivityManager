# ===================================
# Productivity Notifier, Python, 2022
# ===================================
'''Productivity managing interals,
responsible for handling user-entries;
mainly ran in the background.'''
# ============Credentials============
__author__ = 'xyLotus'
# ==============Imports==============
from win10toast import ToastNotifier
from datetime import datetime
from routine import Routine
import time 
import sys
import os


class EntryManager:
    '''Manages all of the entries in the given
    target file, is responsible for notifying you
    when a routine takes place, as well as DNS-block
    websites when a block takes places.'''
    def __init__(self, target_file: str):
        self.target_file = target_file
        self.notifier = ToastNotifier()

        if not os.path.exists(self.target_file):
            print(f'File-Error: File \'{target_file}\' is non-existent.')
            exit(1)

        self._fetch_routines()

        # If file is empty, close process.
        if len(self.wrapped_entries) == 0:
            print('No entries found, terminating.')
            exit(0)

        # For faster routine time lookup.
        self.routine_times = {}
        self._update_routine_times()
        print(self.routine_takes_place())

    def update(self):
        '''Updates self.wrapped_entries|self.routines with current
        new content. Also adds new routine timings to self.routine_times.'''
        self._fetch_routines()
        self._update_routine_times()

    def _fetch_routines(self):
        '''Accesses current instance of self.wrapped_entries
        and unwraps them. Terminates program on ValueError.'''
        with open(self.target_file, 'r') as f:
            self.wrapped_entries = f.readlines()
            
        wrapped_routines = []
        for i in self.wrapped_entries:
            wrapped_routines.append(i.removesuffix('\n'))
        
        # Create list of Routine instance, from wrapped raw entries.
        try:
            self.routines = [Routine.from_wrapped(i) for i in wrapped_routines]
        except ValueError:
            print(f'Val-Error: Found entry with invalid format, terminating.')
            exit(1)

    def _update_routine_times(self):
        '''Updates self.routine_times, creates new key for each new time.'''
        for r in self.routines:
            if not r.time in self.routine_times:
                self.routine_times[r.time] = []
            self.routine_times[r.time].append(r)

    def routine_takes_place(self) -> bool:
        '''Returns true if the current time is 
        existent as a key in self.routine_times.'''
        return time.strftime('%H:%M') in self.routine_times

    def notify(self, routine: Routine):
        '''Notify the user with routine information displayed.'''
        self.notifier.show_toast(
            title=routine.title,
            msg=routine.desc,
            duration=10
        )

    # TODO => Implement website blocks        
    def time_block_website(website: str, time_start: str, time_end: str):
        '''Block the given website for the given period of time.'''
        pass


def main():
    if sys.platform == 'win32':
        os.system('title ProductivityManager')

    target_file = 'default.txt'
    entry_manager = EntryManager('default.txt')

    while True:
        entry_manager.update()

        # Can't guarantee subsecond precision;
        # Calling functions takes milliseconds, etc.
        # This may only occur on program start-up.
        print(f'{time.strftime("%H:%M")} - {entry_manager.routine_takes_place()}')
        if entry_manager.routine_takes_place():
            for r in entry_manager.routine_times[time.strftime('%H:%M')]:
                entry_manager.notify(r)
                print(f'Routine Notified: {r}')

        pause_time = 60 - (datetime.now().second-1) 
        time.sleep(pause_time)
    
if __name__ == '__main__':
    main()