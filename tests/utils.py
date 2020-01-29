import json
from copy import deepcopy
from nb.config import cell_line

def assert_ipynb(ipynb):
    with open(ipynb, 'rb') as f:
        line = f.read()
    # import pdb; pdb.set_trace()
    assert line
    struct = json.loads(line.decode('utf-8'))
    assert 'cells' in struct.keys()

def add_tail_lines(ipynb,lines):
    with open(ipynb, 'rb') as f:
        line = f.read()
    # import pdb; pdb.set_trace()
    struct = json.loads(line.decode('utf-8'))
    origin_lines = len(struct['cells'])
    for source,output in lines:
        s = deepcopy(cell_line)
        s["source"]=source
        # s["outputs"]["text"] = output
        struct['cells'].append(s)
    end_lines = len(struct['cells'])

    with open(ipynb, 'wb') as f:
        f.write(json.dumps(struct).encode('utf-8'))
    return end_lines - origin_lines

def resume_last_add(ipynb,nums):
    with open(ipynb, 'rb') as f:
        struct = json.loads(f.read().decode('utf-8'))
    if len(struct["cells"]) < nums:
        raise ValueError('length of ipynb cells error:{}'.format(len(struct['cells'])))
    struct["cells"] = struct["cells"][:-nums]
    with open(ipynb, 'wb') as f:
        f.write(json.dumps(struct).encode('utf-8'))