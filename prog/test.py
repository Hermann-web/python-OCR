print(6*'----------------------------------')
import re
import string 


PUNCTUATION = string.punctuation
TEMPLATE_NUM_FACTURE_STR = 'Template'
DIGIT_STR = 'Number'
CHAR_STR = 'Character' #ex f,g,h
CHAR_UPPER_STR = 'UpperCharacter'
CHAR_LOWER_STR = 'LowerCharacter'
DICT_REGEX = {
        DIGIT_STR: '\d',
        CHAR_STR: '[a-zA-Z]',
        CHAR_UPPER_STR: '[A-Z]',
        CHAR_LOWER_STR: '[a-z]'
        }

#la fonction de match 
def ismatch(sequence,template):
    regex=''
    for tuple in template:
        expression,occurence = tuple[0], tuple[1]
        if expression in DICT_REGEX:
            print(expression, 'found in DICT_REGEX')
            regex += DICT_REGEX[expression]
        elif expression in PUNCTUATION:
            print(expression, 'found in PUNCTUATION')
            regex += "\\"+expression
        else:
            print(expression, 'found in DICT_REGEX nor PUNCTUATION')
            regex += "("+expression+")"

        regex += '{'+str(occurence)+'}'
    regex = "\\" + "b" + regex + "\\" +'b'
    print('regex: ',[regex])
    
    
    return re.findall(regex,sequence) or []



#template = [(DIGIT_STR,3),('\/',1)]
template = [(DIGIT_STR,3),('!',1)]


#print(ismatch('666! 7895',template))


#print(re.findall('\\b\\d{3}[?]\\b','55 666? 6656// 6667 666/ 45p/ 666'))
print('a:',re.findall('\d{3}[\?]','55 666? 6656// 6667 666/ 45p/ 666'))
template = [(DIGIT_STR,3),('\!',1),('!',1)]
print('a1',ismatch('666!!7895',template))
#A retenir 
        #'\!' == '\\!' == '\\'+'!'
        # '\\\!' == '\\\\!' == '\\\\'+'!' == '\\' + '\\' + '!'
print('------------un test avec poctuation, chiffres et symboles----------------------')
Gt = []
from string import punctuation
def test_punctuation():
    Liste_punc = list(punctuation)
    for punc in Liste_punc:
        punc_ = punc
        print(f'----------------------------------------{punc_}---')
        print('punc use = ',[punc_])
        template = [('§',1),(DIGIT_STR,3),(punc_,1)]
        print('template = ',template)
        sequence = '§666'+punc_
        print('sequence = ',sequence)
        try:
            L = ismatch(sequence,template)
            print(L)
            if not L: print('\n\n');Gt.append(punc)
        except Exception as e:
            print('[]')
            #raise e

test_punctuation()
print('not got right: ',Gt)

print('----------un test sur les carac sppeciaux----------------------')
import re
liste = ['This sentence is correct.','This sentence is not correct', 'Something is !wrong! here.','"This is an example of *correct* sentence."']
# What I tried so for is:
for sentence in liste:
    print(re.match('^[A-Z][^?!.]*[?.!]$', sentence) is not None)


print('-----------------------------')
regex = "(\d{3}(!|\/|\?|\[|\^|\$|\,|\-|\'))"
regex = "\d{3}[!\/\?\[\^\$\,\-\']"
regex = "\d{3}[!/?\]\[^$,\-'\\\\]"
#regex = "\d{3}" +"["+ punctuation + "]"

Listetofound = ['000!', '111/', '222?', '333[', '444^', ',555$', '666,', '777-,', "888'", '999\\']
str_ = ' '.join(Listetofound)
found = re.findall(regex, str_)

if set(Listetofound).difference(found):
    print('weird',set(Listetofound).difference(found),'has not been found !')
else:
    print('ok')

Listenottofound = ['hhh']
str_ = ' '.join(Listetofound)
found = re.findall(regex, str_)
if found:
    print('weird',found,'has been found !')
else:
    print('ok')


print('-----------------------------')
str_ = "A111-145 a111-145" #CHAR_STR, CHAR_UPPER_STR, CHAR_LOWER_STR 
template=[(CHAR_LOWER_STR,1),(DIGIT_STR,3),('-',1),(DIGIT_STR,3)]
print(ismatch(str_,template))


print('-----------------------------')
str_ = "a111-145 a112-1457" #CHAR_STR, CHAR_UPPER_STR, CHAR_LOWER_STR 
template=[(CHAR_LOWER_STR,1),(DIGIT_STR,3),('-',1),(DIGIT_STR,3)]
print(ismatch(str_,template))
print(re.findall('\\b\\d{3}\\b','55 666 6656'))
