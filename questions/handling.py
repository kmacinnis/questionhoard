from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import random
from itertools import product as iterproduct
from operator import itemgetter

import questions.models
import questions.mathness as mathness
from collections import defaultdict
import re
import keyword
import sympy






safelocals = {}
safeglobals = {key : value for key, value 
                    in mathness.__dict__.items() if key[:2] != '__'}




def crossproduct(*args):
    """Returns the cross product of any number of lists (or other iterables)"""
    return list(iterproduct(*args))


def unfiltered_possibilities(question):
    randvars = question.randvar_set.all()
    varnames = [item.varname for item in randvars]
    possibilities = crossproduct(
        *[eval(item.varposs,safeglobals,safelocals) 
                    for item in randvars]
        )
    return tuple([dict(zip(varnames,t)) for t in possibilities])


def filtered_possibilities(question):
    
    def meets_conditions(valdict, conditions):
        return all([eval(c.condition_text, safeglobals, valdict) 
                        for c in conditions])

    conditions = question.condition_set.all()
    return [p for p in unfiltered_possibilities(question)
                    if meets_conditions(p,conditions)]


def display_dict(d):
    display = ''
    for key in d:
        display += '{key} = {value}; '.format(key=key,value=d[key])
    return display.strip('; ')


def condense_list_of_dicts(dicts,key):
    if not all([key in d for d in dicts]):
        raise ValueError('{key} not in every dict in list'.format(key=key))
    
    keyvals = set([d[key] for d in dicts])
    result = []
    for val in keyvals:
        temp_dict = {}
        temp_dict[key] = val
        matching_dicts = [d for d in dicts if d[key] == val]
        all_keys = set(sympy.flatten([list(d.keys()) for d in matching_dicts]))
        for k in all_keys:
            if k != key:
                temp_dict[k] = set([d[k] for d in matching_dicts])
        result.append(temp_dict)
    return result


def handle_ordering(choice_list, correct_position=None):
    '''
    Takes a list of choice dictionaries, randomly
    sets a position key on each, respecting pinned choices,
    and returns the choice_list sorted by that position.
    
    If passed a value for correct_position, it must be an
    integer less than the length of the choice_list.
    
    '''
    AnswerChoice = questions.models.AnswerChoice
    correct_answer = [c for c in choice_list if c['correct']][0]
    open_positions = list(range(len(choice_list)))
    pinned_choices = [c for c in choice_list 
                            if c['pin'] != AnswerChoice.RANDOM]
    if correct_position is not None:
        if correct_position not in open_positions:
            raise ValueError("correct_position must be an integer less than the length of choice_list")
        correct_answer['position'] = correct_position
        open_positions.remove(correct_position)
        try:
            pinned_choices.remove(correct_answer)
        except ValueError:
            pass
    for choice in pinned_choices:
        if choice['pin'] == AnswerChoice.LAST:
            choice['position'] = len(choice_list) - 1
        else:
            choice['position'] = int(choice['pin'])
        open_positions.remove(choice['position'])
    randomized_choices = [
        choice for choice in choice_list 
        if (choice['pin'] == AnswerChoice.RANDOM) 
        and (choice.get('position','empty') == 'empty')
    ]
    random.shuffle(open_positions)
    for pos, choice in zip(open_positions,randomized_choices):
        choice['position'] = pos
    return sorted(choice_list, key=itemgetter('position'))


def latex(thing):
    # TODO I think we need to make this latexify anything.  For now, it's sympy objects and dictionaries.  Need to at least add lists and tuples.
    if isinstance(thing, sympy.Basic):
        return sympy.latex(thing)
    if isinstance(thing, dict):
        return { key: latex(value) for key, value in thing.items()}
    return thing


def make_inline(latex):
    '''
    Takes a latex string, which may contain display math, and returns it
    with all math expressions as inline math.
    '''
    if not latex:
        return latex
    return latex.replace(r'\[',r'\(').replace(r'\]',r'\)')


def output_question(question, vardict, set_choice_position=True):
    """
    Returns a dictionary 
    question should be a Question object, and 
    vardict should be a dictionary mapping the random variables
    in that question to the values to be used.
    order_choices should be boolean.  If true, the dictionary will 
    include a key 'position', and will be sorted on that key.
    """

    AnswerChoice = questions.models.AnswerChoice
    safelocals = vardict.copy()

    # Bring in the symbolic variables
    separator = re.compile(r'[\,\;\s|]')
    sym_vars = separator.split(question.symbol_vars)
    sym_vars = [v for v in sym_vars if v]
    for v in sym_vars:
        exec('{v} = Symbol("{v}")'.format(v=v), safeglobals, safelocals)

    # Run code to establish all variable values
    exec(question.code, safeglobals, safelocals)
    
    if question.short_version:
        short_version = question.short_version.format(**latex(safelocals))
    else:
        short_version = None
    questiontext = question.question_text.format(**latex(safelocals))
    
    choices = []
    for ans in question.answerchoice_set.all():
        if ans.choice_expr:
            exec('choice_expr = {}'.format(ans.choice_expr),
                    safeglobals,safelocals)
        choice = ans.choice_text.format(**latex(safelocals))
        choices.append({'text':choice,'type':ans.choice_type,'pin':ans.pin})
    choices = condense_list_of_dicts(choices,'text')
    for choice in choices:
        choice['correct'] = (AnswerChoice.CORRECT in choice['type'])
        if choice['correct']:
            answer = choice['text']
        if len(choice['pin']) == 1:
            choice['pin'] = list(choice['pin'])[0]
        else:
            raise NotImplementedError('Pin conflict!!!')
    if set_choice_position:
        choices = handle_ordering(choices)
    output = {
        'questiontext' : questiontext,
        'choices' : choices,
        'locals' : safelocals,
        'Q' : make_inline(short_version),
        'A' : make_inline(answer),
    }
    return output



def preview_question(question):
    try:
        vardicts = question.validation.vardicts
    except ObjectDoesNotExist:
        
        return defaultdict(lambda: 'ERROR! Question has not been validated.')
    
    # For now, preview just takes the first possible option.
    
    return output_question(question, vardicts[0])







def validate_question(question, user):
# TODO: Items with *
    """
    This function validates the question by checking for several conditions.
    If it fails, we return a dictionary of error messages.
    If it succeeds, we return None.
    
    Checks for the following things:
        * Question name should be unique to user
        ✓ all fields that contain code (varposs, condition, code, choice_expr)
          are _probably_ safe to run (no double underscores, no known attacks)
          If not, logs warning in bad_code model.
        ✓ Every varposs returns an iterable when eval'ed
        ✓ Conditions should evaluate to a boolean
        ✓ Code runs without errors
        ✓ Symbolic variables can all be symbol()ed
        ✓ Any random or symbolic variables are actually used in 
          either the question_code or the question_text. 
        ✓ There is exactly one answer choice with choice_type == AnswerChoice.CORRECT
        ✓ At most 3 answer choices have choice_type == TOP3
        ✓ At most 4 answer choices have choice_type == TOP3 or TOP4
        * Check for conflicting AnswerChoice pin values
          (including no LAST and E in TOP4 and no LAST and D in TOP3)
        * Strings that get .format() replacements use {{ }} properly
        * Strings that get .format() replacements check for {0} and warn.
        * Give warning to user when different AnswerChoices return the
          same value for some particular vardict
    
    """




    def code_probably_safe(code=None, question=None,
                        user=None, field_name=None, **kwargs):
        if not code:
            return True
        spaceless_code = re.sub(r'\s','', code)
        if '(((((((' in spaceless_code:
            bad = BadCodeWarning(
                question = question,
                user = user,
                warn_datetime = timezone.now(),
                error_type = BadCodeWarning.OVER_NESTING,
                field_name = field_name,
                code = code
            )
            bad.save()
        if ('b"' in code) or ("b'" in code):
            bad = BadCodeWarning(
                question = question,
                user = user,
                warn_datetime = timezone.now(),
                error_type = BadCodeWarning.BYTE_STRINGS,
                field_name = field_name,
                code = code
            )
            bad.save()
        if '__' in code:
            bad = BadCodeWarning(
                question = question,
                user = user,
                warn_datetime = timezone.now(),
                error_type = BadCodeWarning.DOUBLE_UNDERSCORE,
                field_name = field_name,
                code = code
            )
            bad.save()
            return False
        return True

    def fail_response(validation_errors):
        return validation_errors

    AnswerChoice = questions.models.AnswerChoice
    validation_errors = defaultdict(list)
    data = dict(question=question, user=user, 
                            validation_errors=validation_errors)
    
    # Check that code is probably safe to run:
    varposs_code = [r.varposs for r in question.randvar_set.all()]
    varposs_okay = [code_probably_safe(code =code,field_name='randvar',**data) 
                                        for code in varposs_code]
    if not all(varposs_okay):
        validation_errors['randvar'].append('Potentially unsafe code in varposs field')
    
    condition_code = [c.condition_text for c in question.condition_set.all()]
    conditions_okay = [code_probably_safe(code=code,field_name='condition',**data) 
                                                for code in condition_code]
    if not all(conditions_okay):
        validation_errors['condition'].append('Potentially unsafe code in condition field')
    
    answerchoice_code = [a.choice_expr for a in question.answerchoice_set.all()]
    answerchoices_okay = [code_probably_safe(code=code,field_name='anschoice',**data) 
                                                for code in answerchoice_code]
    if not all(answerchoices_okay):
        validation_errors['anschoice'].append('Potentially unsafe code in answer choice expression')

    
    if not code_probably_safe(code=question.code, field_name='code',**data):
        validation_errors['code'].append('Potentially unsafe code in code field')
    
    
    # Check that symbolic variable is a comma or space separated list
    # of valid variable names.

    # Valid separators are commas, semicolons and whitespace.
    separator = re.compile(r'[\,\;\s|]')
    sym_vars = separator.split(question.symbol_vars)
    
    # Get rid of empty strings created by have ", " in the original string.
    sym_vars = [v for v in sym_vars if v]
    
    valid_varname = re.compile(r'[A-Za-z]\w*')
    for var in sym_vars:
        if not valid_varname.match(var):
            err_mess = '''{} is not a valid symbolic variable name.
                Valid names start with a letter, and
                contain only letters, digits, and underscores.'''.format(var)
            validation_errors['symbvar'].append(err_mess.strip())
        if var in keyword.kwlist:
            err_mess = '''{} is not a valid symbolic variable name.
            A name cannot be a reserved python keyword'''.format(var)
            validation_errors['symbvar'].append(err_mess.strip())
    
    
    # Handle answer-choice checking.  
    
    num_correct = question.answerchoice_set.filter(
                        choice_type=AnswerChoice.CORRECT).count()
    num_top3 = question.answerchoice_set.filter(
                        choice_type=AnswerChoice.TOP3).count()
    num_top4 = question.answerchoice_set.filter(
                        choice_type=AnswerChoice.TOP4).count()
    if num_correct == 0:
        validation_errors['anschoice'].append('There should be a correct answer choice.')
    if num_correct > 1:
        err_mess = '''
            There should be exactly one answer choice marked correct.
            Addtional answer choices may be marked as "{}".
            '''.format(dict(AnswerChoice.CHOICE_TYPES)['VARR'])
        validation_errors['anschoice'].append(err_mess.strip())
    if num_top3 > 3:
        validation_errors['anschoice'].append('There should be at most 3 distractors marked "Top 3".')
    if num_top3 + num_top4 > 4:
        validation_errors['anschoice'].append('eeek')
    
    
    # Check that all variables (random and symbolic) are used
    words = re.split('\W+',question.code) + re.split('\W+',question.question_text)
    for var in sym_vars:
        if var not in words:
            err_mess = '''
            Symbolic variable {} is defined, but not used in either the 
            question code or question text.'''.format(var)
            validation_errors['symbvar'].append(err_mess.strip())
    
    rand_vars = [r.varname for r in question.randvar_set.all()]
    for var in rand_vars:
        if var not in words:
            err_mess = '''
            Random variable {} is defined, but not used in either the 
            question code or question text.'''.format(var)
            validation_errors['randvar'].append(err_mess.strip())
    
    
    
    # We will now perform checks that involve eval() and exec(), so
    # if there are any errors (which could be potentially unsafe code),
    # we need to exit here.
    
    if validation_errors:
        return fail_response(validation_errors)
    
    
    # Check that every varposs returns an iterable
    safelocals = {}
    randvar_poss = [r.varposs for r in question.randvar_set.all()]
    for poss in randvar_poss:
        try:
            evaled = eval(poss, safeglobals, safelocals)
        except (SyntaxError, NameError) as exception:
            err_mess = '''Bloop 244:
            The code "{code}" returned an error:
            ERROR: {error}'''.format(code=poss,error=exception)
            validation_errors['randvar'].append(err_mess.strip())
            continue
        try:
            evaled.__iter__
        except SyntaxError:
            err_mess = '''Bloop 252:
            The code "{code}" returned <{value}>, which is not a
            set, list, or tuple of values.
            '''.format(code=poss, value=evaled)
            validation_errors['randvar'].append(err_mess.strip())
    
    if validation_errors:
        return fail_response(validation_errors)
    
    
    # Check that conditions all return boolean values for all possibilities
    from questions.handling import unfiltered_possibilities
    
    for cond in [c.condition_text for c in question.condition_set.all()]:
        for vardict in unfiltered_possibilities(question):
            try:
                evaled = eval(cond, safeglobals, vardict)
            except (SyntaxError, NameError) as exception:
                err_mess = '''Bloop 269:
                The code "{code}" returned an error
                with values {vals}.
                ERROR: {error}
                '''.format(code=cond,vals=display_dict(vardict),error=exception)
                validation_errors['condition'].append(err_mess.strip())
                break
            if evaled not in (True, False):
                err_mess = '''Bloop 274:
                The code "{code}" does not evaluate to a boolean
                with values {vals}.
                It evaluates to {evaled}
                '''.format(code=cond,vals=display_dict(vardict),evaled=evaled)
                validation_errors['condition'].append(err_mess.strip())
    
    
    if validation_errors:
        return fail_response(validation_errors)
    
    
    
    
    vardicts = filtered_possibilities(question)
    num_poss = len(vardicts)
    
    # Now we pick one set of values that meet the conditions (a vardict),
    # make the symbolic variables into sympy Symbols,
    # and check for errors in the following:
    #           * exec(code)
    #           * eval(choice_expr) for each answer choice
    safelocals = vardicts[0].copy()
    
    for v in sym_vars:
        exec('{v} = Symbol("{v}")'.format(v=v), safeglobals, safelocals)
    
    
    
    try:
        exec(question.code, safeglobals, safelocals)
    except (SyntaxError, NameError) as exception:
        err_mess = '''
        The main code block returned an error:"
        ERROR: {error}
        '''.format(error=exception)
        validation_errors['code'].append(err_mess.strip())
    
    choice_exprs = [
        a.choice_expr for a in question.answerchoice_set.all() if a.choice_expr
    ]
    for choice_expr in choice_exprs:
        try:
            evaled = eval(choice_expr, safeglobals,safelocals)
        except (SyntaxError, NameError) as exception:
            err_mess = '''
            The answer choice "{code}" returned an error:"
            ERROR: {error}
            '''.format(error=exception,code=choice_expr)
            validation_errors['anschoice'].append(err_mess.strip())
    
    if validation_errors:
        return fail_response(validation_errors)
    else:
        
        try:
            validation = question.validation
        except ObjectDoesNotExist:
            validation = questions.models.Validation(question = question)

        validation.last_verified = timezone.now()
        validation.vardicts = vardicts
        validation.num_poss = num_poss
        validation.validated_by = user

        validation.save()
        
        return
        







