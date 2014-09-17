from questions.models import AnswerChoice
from operator import itemgetter
from itertools import groupby, product
import random

from exams.models import ExamAnswerChoice
from questions.handling import handle_ordering, output_question



CORRECT = AnswerChoice.CORRECT
TOP3 = AnswerChoice.TOP3
TOP4 = AnswerChoice.TOP4
DISTRACT = AnswerChoice.DISTRACT
wanted_choicetypes = {CORRECT,DISTRACT,TOP3,TOP4}

sorting = {
    CORRECT : 0,
    TOP3 : 1,
    TOP4 : 2,
    DISTRACT : 3
}
    
    


def get_possible_correct_placement(choices):
    RANDOM = AnswerChoice.RANDOM
    LAST = AnswerChoice.LAST

    if set([c['pin'] for c in choices]) == {RANDOM}:
        return range(len(choices))
    correct_pin = [c['pin'] for c in choices if c['correct']][0]
    if correct_pin == LAST:
        return [len(choices) - 1]
    if correct_pin != RANDOM:
        # since 'last' would have already returned, 
        # this is a string continaing a single digit
        return [ int(correct_pin) ]
    # Now, correct_pin == random, but some distractors are pinned
    open_positions = list(range(len(choices)))
    pins_used = [c['pin'] for c in choices if c['pin'] != RANDOM]
    if LAST in pins_used:
        pins_used.remove(LAST)
        pins_used.append(len(choices) - 1)
    for pin in pins_used:
        open_positions.remove(int(pin))
    return open_positions


def get_form_number(style, num):
    if style == 'number':
        return str(num+1)
    elif style == 'letter':
        letters = 'ABCDEFGHJKLMNPQRSTUVWXYZ'
        return letters[num]
    else:
        raise ValueError("form_number_style must be letter or number")

def create_answer_choices(questions, max_choices=99):
    prev1, prev2 = -1, -2
    for q in questions:
        choices = output_question(
            q.question, q.vardict, set_choice_position=False)['choices']
        choices = [c for c in choices if c['type'] <= wanted_choicetypes]
        for choice in choices:
            choice['temp_order'] = min([sorting[t] for t in choice['type']])
        choices.sort(key=itemgetter('temp_order'))
        all_choices = choices[:max_choices]
        poss_correct_places = get_possible_correct_placement(all_choices[q])
        if (prev1 == prev2) and (len(poss_correct_places) != 1):
            try:
                poss_correct_places.remove(prev1)
            except ValueError:
                pass
        correct_position = random.choice(poss_correct_places)
        choices = handle_ordering(
                all_choices, correct_position=correct_position
        )
        for choice in choices:
            answer_choice = ExamAnswerChoice(
                exam_question = q,
                position = choice['position'],
                choice_text = choice['text'],
                correct = choice['correct'],
            )
            if 'comment' in choice:
                answer_choice.comment = choice['comment']
            answer_choice.save()
                
    







        