# ===================================
# Productivity Project Utils, Python, 2022
# ============Credentials============
__author__ = 'xyLotus'
# ==============Imports==============
import regex


def clr_green(string) -> str:
    '''Colors the given string green, with ANSI-reset-code.'''
    return f'\u001b[32m{string}\u001b[0m'

def clr_red(string) -> str:
    '''Colors the given string red, with ANSI-reset-code.'''
    return f'\u001b[31m{string}\u001b[0m'

def clr_bwhite(string) -> str:
    '''Colors the given string bright white, with ANSI-reset-code.'''
    return f'\u001b[37;1m{string}\u001b[0m'

def clr_gray(string) -> str:
    '''Colors the given string grey, with ANSI-reset-code.'''
    return f'\u001b[1;30m{string}\u001b[0m'

def list_remove_all(src: list, target_elem: object) -> list:
    '''Returns list without the given element if
    existent in given list.
    :src: list that with elements that are to-be-removed.
    :target_elem: element to-be-removed from src list.'''
    while target_elem in src:
        src.remove(target_elem)

    return src

def time_input_stream(time='') -> str:
    '''Checks conformity of time str-input 
    reiterates question if param is unconform.'''
    if len(time) == 0:
        time = input('$time... ')
    
    time_regex = r'^(?:[01]?\d|2[0-3])(?::[0-5]\d){1,2}$'
    while 1:
        if not regex.match(time_regex, time):
            print(f'{clr_red("Format-Error")}: Format is HH:MM')
            time = input('$time... ')
        else: 
            break
    
    return time