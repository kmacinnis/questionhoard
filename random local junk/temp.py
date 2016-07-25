from sympy import flatten
import random
from operator import itemgetter

CORRECT = ''
RANDOM = 'random'
LAST = 'last'
A = '0'
B = '1'
C = '2'
D = '3'
E = '4'



dicts = [
    {'color':'red', 'thing':'apple'},
    {'color':'red', 'thing':'wagon'},
    {'color':'red', 'thing':'ruby'},
    {'color':'blue', 'thing':'sky'},
    {'color':'blue', 'thing':'ribbon'},
    {'color':'yellow','thing':'lemon'},
]

def condense_list_of_dicts(dicts,key):
    if not all([key in d for d in dicts]):
        raise ValueError('{key} not in every dict in list'.format(key=key))
    
    keyvals = set([d[key] for d in dicts])
    result = []
    for val in keyvals:
        temp_dict = {key: val}
        matching_dicts = [d for d in dicts if d[key] == val]
        all_keys = set(flatten([list(d.keys()) for d in matching_dicts]))
        for k in all_keys:
            if k != key:
                temp_dict[k] = [d[k] for d in matching_dicts]
        result.append(temp_dict)
    return result



cl = [
    dict(text='pinned first', pin='0',choice_type=None),
    dict(text='pinned last', pin='last',choice_type=None),
    dict(text='random1',choice_type=None,pin=RANDOM),
    dict(text='random2',choice_type=None,pin=RANDOM),
    
]



def handle_ordering(choice_list, correct_position=None):
    # correct_answer = [c for c in choice_list if c['choice_type']==CORRECT][0]
    open_positions = list(range(len(choice_list)))
    print(open_positions)
    if correct_position != None:
        correct_answer['position'] = int(correct_position)
        open_positions.remove(int(correct_position))
    pinned_choices = [c for c in choice_list if c['pin'] != RANDOM]
    for choice in pinned_choices:
        if choice['pin'] == LAST:
            choice['position'] = len(choice_list) - 1
        else:
            choice['position'] = int(choice['pin'])
        print(choice['position'])
        open_positions.remove(choice['position'])
    randomized_choices = [c for c in choice_list if c['pin'] == RANDOM]
    random.shuffle(open_positions)
    for pos, choice in zip(open_positions,randomized_choices):
        choice['position'] = pos
    return sorted(choice_list, key=itemgetter('position'))

print(handle_ordering(cl))
    
    