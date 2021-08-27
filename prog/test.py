import re

TEMPLATE_NUM_FACTURE_STR = 'Template'
DIGIT_STR = 'Number'
CHAR_STR = 'Character' #ex f,g,h
CHAR_UPPER_STR = 'UpperCharacter'
CHAR_LOWER_STR = 'LowerCharacter'
def ismatch(sequence,template):
    regex=''
    for tuple in template:
        expression,occurence = tuple[0], tuple[1]
        if expression in DICT_REGEX:
            regex += DICT_REGEX[expression]
        else:
            regex += expression
        regex += '{'+str(occurence)+'}'
    regex = '\\'+'b'+regex+'\\'+'b'
    print([regex])
    
    return re.findall(regex,sequence)

DICT_REGEX = {
        DIGIT_STR: '\d',
        CHAR_STR: '[a-zA-Z]',
        CHAR_UPPER_STR: '[A-Z]',
        CHAR_LOWER_STR: '[a-z]'
        }

#template = [(DIGIT_STR,3),('\/',1)]
template = [(DIGIT_STR,3)]


print(ismatch('666 7895',template))


print(re.findall('\\b\\d{3}\\b','55 666 6656// 6667 666/ 45p/ 666'))
