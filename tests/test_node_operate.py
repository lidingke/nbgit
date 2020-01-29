
from random import randint
from nb.branch import   Branch
from .utils import add_tail_lines, resume_last_add, assert_ipynb
test_ipynb_dir = 'data/Untitled.ipynb'

def get_random_line():
    line = []
    for i in range(1,randint(3, 20)):
        c = randint(65,122)
        line.append(chr(c))
    return "".join(line)

def test_add_cmd():
    add_lines = []
    for i in range(1,randint(3,20)):
        add_lines.append(
            ((get_random_line(),get_random_line()))
        )
    len_ = len(add_lines)    
    assert_ipynb(test_ipynb_dir)
    cb = Branch(test_ipynb_dir)
    nums = add_tail_lines(test_ipynb_dir,add_lines)
    cb.add_cmd()
    cb.commit_cmd('test commit')
    resume_last_add(test_ipynb_dir,nums)

def test_log_operate():
    cb = Branch(test_ipynb_dir)
    cb.log_cmd()