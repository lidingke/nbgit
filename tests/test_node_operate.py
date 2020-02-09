
from random import randint
from nb.branch import   Repo, init_cmd
from .utils import add_tail_lines, resume_last_add, assert_ipynb
import shutil 
test_ipynb_dir = 'data/Untitled.ipynb'
test_ipynb_dir_origin = 'data/Untitled_origin.ipynb'

shutil.copy(test_ipynb_dir_origin,test_ipynb_dir)

def get_random_line():
    line = []
    for i in range(1,randint(3, 20)):
        c = randint(65,122)
        line.append(chr(c))
    return "".join(line)

def test_init_bare_repo():
    """
    nbgit init: run cmd in ipynb, create a emputy file.
    """
    init_cmd(test_ipynb_dir)
    cb = Repo(test_ipynb_dir)
    # assert cb
    # cb.init_cmd()
    assert cb.cache.parents[0] == 'root'
    assert cb.current.name == 'master'
    assert cb.current.index == 'root'


def test_add_cmd():
    add_lines = []
    for i in range(1,randint(3,20)):
        add_lines.append(
            ((get_random_line(),get_random_line()))
        )
    len_ = len(add_lines)    
    assert_ipynb(test_ipynb_dir)
    cb = Repo(test_ipynb_dir)
    nums = add_tail_lines(test_ipynb_dir,add_lines)
    cb.add_cmd()
    cb.commit_cmd('test commit')
    resume_last_add(test_ipynb_dir,nums)
    cb.log_cmd()

def test_log_operate():
    cb = Repo(test_ipynb_dir)
    print('log first',cb.cache.index)
    cb.log_cmd()

def test_reset_cmd():
    # TODO impl resume cmd
    add_lines = []
    for i in range(1,randint(3,20)):
        add_lines.append(
            ((get_random_line(),get_random_line()))
        )
    # len_ = len(add_lines)    
    assert_ipynb(test_ipynb_dir)
    cb = Repo(test_ipynb_dir)
    nums0 = add_tail_lines(test_ipynb_dir,add_lines)
    cb.add_cmd()
    index0 = cb.commit_cmd('test commit0')
    nums1 = add_tail_lines(test_ipynb_dir,add_lines)
    cb.add_cmd()
    index1 = cb.commit_cmd('test commit1')
    nums2 = add_tail_lines(test_ipynb_dir,add_lines)
    cb.add_cmd()
    index2 = cb.commit_cmd('test commit2')
    print('log at commits')
    print(cb.cache)
    # cb2 = Branch(test_ipynb_dir)
    print('log at commits afer Branch',cb.cache.index)
    cb.log_cmd()
    cb.reset_hard_cmd(index=index0)
    resume_last_add(test_ipynb_dir,nums0)
    print('log at reset')
    print(cb.cache)
    cb.log_cmd()

def test_log_operate2():
    print('log 2:')
    cb = Repo(test_ipynb_dir)
    cb.log_cmd()

def test_branch_cmd():
    add_lines = []
    for i in range(1,randint(3,20)):
        add_lines.append(
            ((get_random_line(),get_random_line()))
        )
    assert_ipynb(test_ipynb_dir)
    cb = Repo(test_ipynb_dir)
    print(cb.cache)
    cb.commit_cmd('save bug')
    # import pdb; pdb.set_trace()
    # cb.cache.clear()
    cb.branch_cmd('dog')
    cb.checkout_cmd('dog')
    nums0 = add_tail_lines(test_ipynb_dir,add_lines)
    cb.add_cmd()
    index0 = cb.commit_cmd('test commit0')
    nums1 = add_tail_lines(test_ipynb_dir,add_lines)
    cb.add_cmd()
    index1 = cb.commit_cmd('test commit1')
    nums2 = add_tail_lines(test_ipynb_dir,add_lines)
    cb.add_cmd()
    index2 = cb.commit_cmd('test commit2')
    print('log dog')
    cb.log_cmd()
    cb.checkout_cmd('master')
    print('log master')
    cb.log_cmd()


def test_diff_cmd():
    add_lines = []
    for i in range(1,randint(3,20)):
        add_lines.append(
            ((get_random_line(),get_random_line()))
        )
    assert_ipynb(test_ipynb_dir)
    cb = Repo(test_ipynb_dir)
    nums0 = add_tail_lines(test_ipynb_dir,add_lines)
    cb.add_cmd()
    index0 = cb.commit_cmd('test commit0')
    nums1 = add_tail_lines(test_ipynb_dir,add_lines)
    cb.add_cmd()
    index1 = cb.commit_cmd('test commit1')
    cb.diff_cmd(index0,index1)
    resume_last_add(test_ipynb_dir,nums0+nums1)

def test_merge_cmd():
    pass
