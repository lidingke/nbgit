import os
import shutil
import glob
import sys 
sys.path.append('src')
from commit import Commit_Tree, Branch


# def test_workflow_init():
#     for g in glob.glob(os.path.join('..','data','.ipynb_git','Untitled_for_change.*')):
#         print(os.path.abspath(g))
#         os.remove(os.path.abspath(g))
#     print(os.listdir('../data/.ipynb_git'))
#     shutil.copy('../data/Untitled.ipynb','../data/Untitled_for_change.ipynb')


#     ipynb = ('..','data','Untitled_for_change.ipynb')
#     ipynb = os.path.join(*ipynb)
#     # print(ipynb,os.path.split(ipynb))
#     dirname,basename = os.path.dirname(ipynb),os.path.basename(ipynb).split('.')[0]
#     db_dir = os.path.join(dirname,'.ipynb_git',basename)
#     json_dir = os.path.join(dirname,'.ipynb_git',str(basename)+'.json')
#     print(ipynb,db_dir,json_dir)
#     #
#     commit_tree = Commit_Tree(ipynb,db_dir)
#     print('exists',os.path.exists(json_dir))
#     branch = Branch(commit_tree,json_dir)
#     branch.new_commit()

def test_nbgit_workflow_init():
    """
    1. mv old ipynb workflow.ipynb
    2. nbgit add
    3. nbgit diff
    4. nbgit commit
    5. 
    """ 

def test_nbgit_workflow_commit():
    """
    1. mv old ipynb workflow.ipynb
    2. nbgit add 
    3. nbgit diff
    4. nbgit commit
    5. 
    """ 
