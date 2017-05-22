#!/usr/bin/env python3
# encoding: utf-8
import sys
import re

#globals
#main file
main_file = ""
#dictionary file
dict_file = ""


# use this template to replace slices of a string
function_span = "<span onclick=\"translate('{0}')\">{1}</span>"
pres_item = "\n<pre id='{0}'>$word - {1}</pre>"

if __name__ == "__main__":
    if len(sys.argv) == 3:
        main_file = (sys.argv[1])
        dict_file = (sys.argv[2])
    elif len(sys.argv) == 2:
        dict_file = (sys.argv[1])
    else:
        print ('''Enter one  argumet to leave only unic entries in the file
        or two arguments, first file to convert and
        second file with dictionary entries.''')

# define function to open file and read it line by line


def adapt_file():
    pres = []
    content = ''
    dict_entries = []
    with open(main_file, 'r') as f:
        content = f.read()
        f.close()
    head = get_head()
    bottom = get_bottom()
    dict_entries = process_dict_entries(dict_file)
    content = create_paragraph(content)
    for e in dict_entries:
        word, pre = e
        pres.append(pre)
        content = substitute(word, content)
    with open(main_file + ".html", 'w') as w:
        w.write(head)
        w.write(content)
        for p in pres:
            w.write(p)
        w.write(bottom)
        w.close()


def substitute(w, text):
    p = re.compile('\\b' + w + '\\b', re.I)
    text = re.sub(p, create_span, text)
    return text


def create_span(math):
    '''Check if word start with capital letter and keep it if true'''
    word = math.group(0)
    if str.isupper(word[0]):
        word = word[0] + word[1:]
    return "<span onclick=\"translate('{0}')\">{1}</span>"\
            .format(word, word)


def create_paragraph(text):
    text = re.sub(r'^', '<p>', text)
    text = re.sub(r'\t|\s{4}', '</p><p>', text)
    text = re.sub(r'$', '</p>', text, 1)
    return text


def get_head():
    '''Read content of head file and return it as a string'''
    with open('head', 'r') as h:
        return h.read()


def get_bottom():
    '''Read content of bottom file and return it as a string'''
    with open('bottom', 'r') as b:
        return b.read()


def process_dict_entries(file):
    '''Extract dictionary entries from dict file. Check if it is unic.
    Create <pre> tag for resul file. Return list of tuples,
    where tuples are (word to find in main file, <pre>).'''
    unic_words = []
    lines = []
    definition = []
    definitions_list = []
    span = ''
    pre = ''
    dict_entries = []
    # read file line by line store tham as list entries
    with open(file) as f:
        for ln in f:
            if len(ln) > 1 and ln[:-1] == '\n':
            #strip the \n character
                lines.append(ln[:-1])
            else:
                lines.append(ln)
        f.close()
    lines_count = len(lines)
    # get word and it's definition
    for l in lines:
    # counter needed for last definition to be processed
        lines_count -= 1
        if l != '\n':
            definition.append(l)
        #append last defiition
        elif (l == '\n' or lines_count == 0) and len(definition) > 0:
            definitions_list.append(definition)
            definition = []
    if lines_count == 0 and len(definition) > 0:
        definitions_list.append(definition)
    # separate word in definition and actual translation
    for defin in definitions_list:
        translation = ''
        #get word to translate and strip all white spaces off
        word = defin[0]
        word = word.strip()
        defin = defin[1:]
        # if word not unic it will process it twice, so check 
        if word not in unic_words:
            unic_words.append(word)
            for tr in defin:
                translation = translation + tr + '\n'
            pre = "\n<pre id='{0}'>{1}\n{2}</pre>"\
            .format(word, word, translation)
            dict_entries.append((word, pre))
    return dict_entries

def clean_word(w):
    if len(w) == 0 or w =='':
        return
    word = []
    for ch in w:
        if not re.match('[^a-zA-Z-]', ch):
            word.append(ch)
    return str().join(word)


def unic_file(file):
    '''Take file as argument and write back only unic lines'''
    white_list =[]
    unic_list = []
    long_string = ''
    with open(file) as f:
    #get file as long line 
        long_string = f.read()
        f.close()
    #split words 
    dirty_list = re.split(r'\W+', long_string)
    #prepare words in dirty_list
    #import pdb; pdb.set_trace()
    for w in dirty_list:
        word = clean_word(w)
        if w != None:
            white_list.append(word)
    # add only unic entries to unic_list, search ignoring case
    for w in white_list:
        is_in = False
        if len(unic_list) == 0:
            unic_list.append(w)
        for uw in unic_list:
           if re.match(str(w), str(uw), re.I):
               is_in = True
        if not is_in:
            unic_list.append(w)
    if None in unic_list:
        unic_list.pop(unic_list.index(None))
    long_string = '\n\n\n'.join(unic_list)
    with open(file, 'w') as f:
        f.write(long_string)
        f.close()


if len(sys.argv) == 3:
    adapt_file()
elif len(sys.argv) == 2:
    unic_file(dict_file)
