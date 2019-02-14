import shelve
import difflib
import logging
logger = logging.getLogger(__name__)
from blob import Blob
from diff import replace, equal, insert, delete, get_reversed_opecodes, constructer


def test_build():
    db = shelve.open('../data/spam', writeback=True)
    bb = Blob(db,'../data/Untitled.ipynb')
    key_origin,key_diff = None,None
    with shelve.open('../data/spam') as db:
        for k,v in db.items():
            if v['db_type']=='meta' :
                if v.get('dir','') == '../data/Untitled.ipynb':
                    key_origin = k
                if v.get('dir','') == '../data/Untitled_diff.ipynb':
                    key_diff = k
    if key_origin == None or key_diff == None:
        raise ValueError('none meta key')
    origin_cells = bb.db[key_origin]['cells']
    # print(origin['cells'])
    diff_cells = bb.db[key_diff]['cells']
    dif = difflib.Differ()
    # difstr = difflib.context_diff(origin_cells,diff_celss)
    difstr = dif.compare(origin_cells,diff_cells)

    for d in difstr:
        # print(type(d))
        # print(d)
        # print(d[:2])
        print('\''+d[2:8]+'\',')


    matcher = difflib.SequenceMatcher(None,origin_cells,diff_cells)
    # matcher = difflib.SequenceMatcher(None, s1, s2)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        logger.info('{}{}{}{}{}'.format(tag,i1, i2, j1, j2))


def test_opcodes_unit():
    cs0 = [
        '3c8067e6e1f8fd14fca2ae8ac5a02118',
        'c435addc2b156ab46ccde41894387f57',
        '11a90cd73041f7d51f6ae3af6e933238',
        '187ef4436122d1cc2f40dc2b92f0eba0',
        '024043b6cd4b69189af2aa036af3fdd0',
        'cff06947897310f8e8b2a5fb9a035109',
        'c72569b365ccb3e3bb1cd3736e3ce8f8',
        '5d3ab960764a9557886e3b81c3fab27e',
        '58025327d3126668344e8d699fc582f0',
        '97f0599af65f827092286525cc36c3ae',
        '1e23ee2e3c1fdfe98eed3f6e960a5216',
        '18a7134013a1a29c0348fbdbc500c760',
        'b07cce9f533d2a44ac6f018887f06f1b',
        '9a8463e12d7eb8be5e9bf29be73d6cb2',
        '8c27676a1ac6e72d2e11cae5f5decec5',
        'e6e1f7ace4ab76cf3e5bb08e66e3b883',
        'd352bc6653eca81f112aa769d3c4398c',
        'b80be85bd8f85097489b84abbe016c8b',
        '26acccd9a21a9beb7048aae45e13be50',
        '898dff5656f1a400d1cd11dc50b701b2',
        '15bc8d095c82e6657a5e90f17ae2a6cc',
        'd41d8cd98f00b204e9800998ecf8427e',
        'd41d8cd98f00b204e9800998ecf8427e',
    ]

    cs1 = [
        '3c8067e6e1f8fd14fca2ae8ac5a02118',
        'c435addc2b156ab46ccde41894387f57',
        '11a90cd73041f7d51f6ae3af6e933238',
        '187ef4436122d1cc2f40dc2b92f0eba0',
        '024043b6cd4b69189af2aa036af3fdd0',
        'cff06947897310f8e8b2a5fb9a035109',
        'c72569b365ccb3e3bddcd3736e3ce8f8',
        '5d3ab960764a9557886e3b81c3fab27e',
        '58025327d3126668344e8d699fc582f0',
        '97f0599af65f827092286525cc36c3ae',
        '18a7134013a1a29c0348fbdbc500c760',
        '1e23ee2e3c1fdfe98eed3f6e960a5216',
        'b07cce9f533d2a44ac6f018887f06f1b',
        '8c27676a1ac6e72d2e11cae5f5decec5',
        'e6e1f7ace4ab76cf3e5bb08e66e3b883',
        'd352bc6653eca81f112aa769d3c4398c',
        'd352bc6653eca81f112aa769d3c4398c',
        'b80be85bd8f85097489b84abbe016c8b',
        '26acccd9a21a9beb7048aae45e13be50',
        '898dff5656f1a400d1cd11dc50b701b2',
        '15bc8d095c82e6657dfe90f17ae2a6cc',
        'd41d8cd98f00b204e9800998ecf8427e',
        'd41d8cd98f00b204e9800998ecf8427e',
    ]

    matcher = difflib.SequenceMatcher(None,cs0,cs1)
    # matcher = difflib.SequenceMatcher(None, s1, s2)
    cs0_copy = cs0.copy()
    for tag, i1, i2, j1, j2 in reversed(matcher.get_opcodes()):
        if tag == 'insert':
            insert(cs0_copy,i1,i2,cs1[j1:j2])
        elif tag == 'replace':
            replace(cs0_copy,i1,i2,cs1[j1:j2])
        elif tag == 'delete':
            delete(cs0_copy,i1,i2,cs1[j1:j2])

    # _ = [(tag, i0, i1, cs1[j0:j1]) for tag, i0, i1, j0, j1 in reversed(matcher.get_opcodes())]
    # cs0_copy =     constructer(cs0_copy,_)

    # for a,b in zip(cs0_copy,cs1):
    #     print(a,b,a==b)
    assert cs0 != cs1
    assert cs0_copy == cs1

    cs1_copy = cs1.copy()
    for tag, i1, i2, j1, j2 in reversed(matcher.get_opcodes()):
        # print(("%7s a[%d:%d] (%s) b[%d:%d] (%s)" %
        #        (tag, i1, i2, cs0[i1:i2], j1, j2, cs1[j1:j2])))

        if tag == 'insert':
            delete(cs1_copy,j1,j2,cs0[i1:i2])
        elif tag == 'replace':
            replace(cs1_copy,j1,j2,cs0[i1:i2])
        elif tag == 'delete':
            insert(cs1_copy,j1,j2,cs0[i1:i2])

    # for a,b in zip(cs0_copy,cs1):
    #     print(a,b,a==b)
    assert cs0 != cs1
    assert cs1_copy == cs0



def test_operater():
    seq0 = [
        '3c8067e6e1f8fd14fca2ae8ac5a02118',
        'c435addc2b156ab46ccde41894387f57',
        '11a90cd73041f7d51f6ae3af6e933238',
        '187ef4436122d1cc2f40dc2b92f0eba0',
        '024043b6cd4b69189af2aa036af3fdd0',
        'cff06947897310f8e8b2a5fb9a035109',
        'c72569b365ccb3e3bb1cd3736e3ce8f8',
        '5d3ab960764a9557886e3b81c3fab27e',
        '58025327d3126668344e8d699fc582f0',
        '97f0599af65f827092286525cc36c3ae',
        '1e23ee2e3c1fdfe98eed3f6e960a5216',
        '18a7134013a1a29c0348fbdbc500c760',
        'b07cce9f533d2a44ac6f018887f06f1b',
        '9a8463e12d7eb8be5e9bf29be73d6cb2',
        '8c27676a1ac6e72d2e11cae5f5decec5',
        'e6e1f7ace4ab76cf3e5bb08e66e3b883',
        'd352bc6653eca81f112aa769d3c4398c',
        'b80be85bd8f85097489b84abbe016c8b',
        '26acccd9a21a9beb7048aae45e13be50',
        '898dff5656f1a400d1cd11dc50b701b2',
        '15bc8d095c82e6657a5e90f17ae2a6cc',
        'd41d8cd98f00b204e9800998ecf8427e',
        'd41d8cd98f00b204e9800998ecf8427e',
    ]

    seq1 = [
        '3c8067e6e1f8fd14fca2ae8ac5a02118',
        'c435addc2b156ab46ccde41894387f57',
        '11a90cd73041f7d51f6ae3af6e933238',
        '187ef4436122d1cc2f40dc2b92f0eba0',
        '024043b6cd4b69189af2aa036af3fdd0',
        'cff06947897310f8e8b2a5fb9a035109',
        'c72569b365ccb3e3bddcd3736e3ce8f8',
        '5d3ab960764a9557886e3b81c3fab27e',
        '58025327d3126668344e8d699fc582f0',
        '97f0599af65f827092286525cc36c3ae',
        '18a7134013a1a29c0348fbdbc500c760',
        '1e23ee2e3c1fdfe98eed3f6e960a5216',
        'b07cce9f533d2a44ac6f018887f06f1b',
        '8c27676a1ac6e72d2e11cae5f5decec5',
        'e6e1f7ace4ab76cf3e5bb08e66e3b883',
        'd352bc6653eca81f112aa769d3c4398c',
        'd352bc6653eca81f112aa769d3c4398c',
        'b80be85bd8f85097489b84abbe016c8b',
        '26acccd9a21a9beb7048aae45e13be50',
        '898dff5656f1a400d1cd11dc50b701b2',
        '15bc8d095c82e6657dfe90f17ae2a6cc',
        'd41d8cd98f00b204e9800998ecf8427e',
        'd41d8cd98f00b204e9800998ecf8427e',
    ]

    reversed_opecodes = get_reversed_opecodes(seq0,seq1)
    assert seq0 != seq1
    seq0_build = constructer(seq0.copy(),reversed_opecodes)
    for a,b in zip(seq0_build , seq1):
        logger.info("{}:{}={}".format(a,b,a==b))
    assert seq0_build == seq1
    #
    # assert seq0 != seq1
    # seq1_build = back_constructer(seq1.copy(), reversed_opecodes)
    # assert seq1_build == seq0

