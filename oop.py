from data import logger
from classes import Document
from random import randint


def doc_gen():
    n = ['Presentation', 'Diploma', 'Research']
    m = ['biology', 'mathematics', 'physics', 'chemistry']
    a = []
    for i in range(1, randint(9, 20)):
        a.append(Document(title=n[randint(-1, 2)] + ' in ' + m[randint(-1, 2)], number=i))
        logger.info(f'doc_gen(): {a[i-1].display_info()}')
    return a


def doc_search(docs, s):
    logger.info(f'doc_search(), s: {s}')
    tmp = ''
    for i in docs:
        if s in i.get_title() or s in i.content: tmp += '\n' + i.display_info()
    return tmp
