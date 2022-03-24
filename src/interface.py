# ===================================
# Productivity CLI, Python, 2022
# ===============To-do===============
# Feature -> Reference older elements 
# when naming elements.
# Feature -> Implement time-based DNS 
#            website blocks
# # Bug     -> Find out whats making NULL
# content appear in self.target_file
# ^ Has somethind todo with multithreading
# and 'r+' file mode.
# ===================================
'''The producitvity user command-line interface (CLI)
that lets the user manage, delete and create their
routines and communicate with the program internals.'''
# ============Credentials============
__author__ = 'xyLotus'
# ==============Imports==============
from routine import Routine
from utils import *
import regex
import os


def format_routine(r_id: int, entry: str):
    '''Returns standard routine str-format.
    Without /-seperators, from the file.'''
    entry_elems = entry.split('//////')
    
    clr_id = clr_green('#' + str(r_id))
    clr_title = clr_bwhite(entry_elems[1])
    clr_desc = clr_gray(entry_elems[2].removesuffix('\n'))
    
    res = f'{clr_id} {entry_elems[0]} - {clr_title}: {clr_desc}'
    
    return res

class CMDInterface:
    '''Class that stores all the CLI commands, called via reflection in main.
    Note: arg_buffer is a parameter for unused arguments. Prevents irrelevant backend errors.
    Note: r_ => Abbreviation for routine. - r_ID => Routine ID (Chronological Index)'''
    def __init__(self, target_file: str):
        self.target_file = target_file

        try:
            self.file_handle = open(self.target_file, 'r+', buffering=1)
        except FileNotFoundError:
            print(f'{clr_red("File-Error")}: File has not been found, terminating.')

    def __del__(self):
        # No clue if I have to do this, because I am not using
        # a context manager, yet I will just do so. 
        self.file_handle.close()

    def _readfilelines(self) -> list:
        '''Readlines for self.file_handle with automatic
        seek(0) for reusability and safety.'''
        # No clue if seek() is still needed if
        # instantiating the value or readlines
        # to a variable, but whatever.
        self.file_handle.seek(0)
        res = self.file_handle.readlines()

        return res

    def _id_is_valid(self, _id: int) -> bool:
        '''Checks if ID is in range of the entry count range.'''
        return 0 < int(_id) <= len(self._readfilelines())

    def h(self):
        pass

    def new(self, routine: Routine|str = '', dev_input=0):
        '''Creates new routine with Routine class.
        :dev_input: if True, checks `routine` type,
                    else, auto-converts string CLI-input.'''
        # non-CLI input instance type check
        if not isinstance(routine, Routine) and dev_input:
            print(f'{clr_red("Error")}: Param "routine" is not of type Routine().')
            return
        else: # CLI-input => type is str => auto-convert
            print('$-> Routine Information: ')
            routine = Routine(
                time = time_input_stream(),
                title = input('$title... '),
                desc = input('$desc... ')
            )

        self.file_handle.write(str(routine) + '\n')
        self.ls()

    def clear(self, *arg_buffer):
        '''Clear CLI output.'''
        os.system("cls")
        print('$?')
    
    # Abbreviation \sa self.clear()
    def cls(self, *arg_buffer):
        '''Clear CLI output.'''
        self.clear()

    def get(self, r_query: str):
        '''Searches for routine by title or time.'''
        r_query = r_query[0]
        routines = self._readfilelines()

        # check whether the search query is time [idx: 0] or title [idx: 1]
        time_regex = r"^(?:[01]?\d|2[0-3])(?::[0-5]\d){1,2}$" 
        if regex.match(time_regex, str(r_query)):
            query_index = 0
        else:
            query_index = 1

        results_found = False
        for i, val in enumerate(routines):
            entry_items = val.split('//////')
            if r_query == entry_items[query_index]:
                print(format_routine(i, val))
                results_found = True

        if not results_found:
            print(clr_red(f'Didn\'t find any results for query \'{r_query}\''))

    def getid(self, r_id: int):
        '''Searches for routine by ID; non-0-indexed.'''
        
        r_id = int(r_id[0])
        
        # Check ID validity
        lines = self._readfilelines()
        if self._id_is_valid(r_id):
            print(format_routine(r_id, lines[r_id-1]))
        else:
            print(f'{clr_red("ID-Error")}: Routine with ID {r_id} is non-existent.')
            return
        

    def edit(self, r_id: str):
        '''Edit a specific part of the entry with the given ID.'''  
        r_id = int(r_id[0])

        current_file_content = self._readfilelines()
        
        # Check ID validity
        if not self._id_is_valid(r_id):
            print(f'{clr_red("Index-Error")}: Routine with ID {r_id} is non-existent.')
            return
        
        clr_timeinp = clr_bwhite('Time (1)')
        clr_titleinp = clr_bwhite('Title (2)')
        clr_descinp = clr_bwhite('Desc. (3)') 
        print(f'What do you want to edit, {clr_timeinp}, {clr_titleinp} or {clr_descinp}?')
        edit_elem_index = int(input('$element... '))

        if edit_elem_index == 1:
            new_elem = time_input_stream()
        elif edit_elem_index == 2:
            new_elem = input('$title... ')
        elif edit_elem_index == 3:
            new_elem = input('$desc... ')

        # Replace elements in entry, then entry in file        
        entry_elems = current_file_content[r_id-1].split('//////')
        entry_elems[edit_elem_index-1] = new_elem
        edited_entry = Routine(
            entry_elems[0], 
            entry_elems[1],
            entry_elems[2]
        )

        current_file_content[r_id-1] = str(edited_entry)

        # clear file and then write new, edited contents to file
        open(self.target_file, 'w').close() # write mode clears file
        for line in current_file_content:
            self.file_handle.write(line)
        
    def delete(self, r_id: str):
        '''Deletes the routine with the given ID.'''
        r_id = int(r_id[0])
        
        # Remove specific routine / entry [local instance]
        current_file_content = self._readfilelines()
        if not self._id_is_valid(r_id):
            print(f'{clr_red("Index-Error")}: Routine with ID {r_id} is non-existent.')
            return

        confirmation_txt = f'$... Delete entry with ID {clr_bwhite(r_id)}? (y/n)'
        confirmation = input(confirmation_txt).replace(' ', '')
        while 1: # Loop until input is valid
            if confirmation.lower() == 'n':
                return
            elif confirmation.lower() == 'y':
                break
            else:
                print('Invalid Input, valid input is \'y\' or \'n\'')
                confirmation = input(confirmation_txt)

        current_file_content.pop(r_id-1)

        # Clear file
        open(self.target_file, 'w').close()

        # Write to file with updated contents
        for line in current_file_content:
            self.file_handle.write(line)
        
        print(clr_bwhite('[Post-Exec]'))
        self.ls()

    def ls(self):
        '''Lists all routines with all of their info.'''
        routines = self._readfilelines()
        print(clr_bwhite('[Routines]'))
        if len(routines) == 0:
            print('...')
            return

        for i, val in enumerate(routines):
            print(format_routine(i+1, val))


def call_cmd(cmd_interface: CMDInterface, base: str, args=[]):
    '''Calls a command with or without args, checks existence and input of cmd.'''
    if len(base) == 0:
        return

    # Call command/method with error catching and handling
    try:
        if len(args) == 0:
            getattr(cmd_interface, base)()
        else:
            getattr(cmd_interface, base)(args)
    except AttributeError:
       print(f'{clr_red("Error")}: Command "{base}" w/ params {args} not found.')
    except TypeError as e: 
        print(f'{clr_red("Error")}: {e}')
    except KeyboardInterrupt:
        print('\n$!')
        exit(0)
    except Exception as e:
        # You may think "that's bullshit, you should handle errors!"
        # my answer is: no, I'm too lazy. Git gud.
      print(f'{clr_red("Internal-Error")}: ', e)

def main():
    # ? => Start Char
    print("$?")

    os.system("title ProductivityInterface")
    cmd_interface = CMDInterface("default.txt")

    running = 1
    while running:
        # input cmd and check validity
        try:
            cmd = input("$ ").split(' ')
            list_remove_all(cmd, '')
        except KeyboardInterrupt:
            print('\n$!', end='')
            exit(0)

        # Argument handling / cmd splitting
        if len(cmd) > 1:
            cmd_base = cmd[0]
            cmd_args = cmd[1:]
        elif len(cmd) == 1:
            cmd_base = cmd[0]
            cmd_args = []
        
        # Special commands have priority
        if cmd_base == 'break' or cmd_base == 'exit':
            running = 0
        else: 
            # "Safe" cmd call, with less error-catch statements
            call_cmd(cmd_interface, cmd_base, cmd_args) 
        
    # ! => End of program char
    print('$!')


if __name__ == '__main__':
    main()
