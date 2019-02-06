import difflib


def test_operater():
    base = [
        'c435ad',
        '11a90c',
        '187ef4',
        '024043',
        'cff069',
        'c72569',
        '5d3ab9',
        '580253',
        '97f059',
        '1e23ee',
        '18a713',
        'b07cce',
        '9a8463',
        '8c2767',
        'e6e1f7',
        'd352bc',
        'b80be8',
        '26accc',
        '898dff',
        '15bc8d',
        'd41d8c',
        'd41d8c',
    ]

    source = [
        'c435ad',
        '11a90c',
        'cff069',
        'c72569',
        'c72569',
        '5d3ab9',
        '580253',
        '97f059',
        '1e23ee',
        '1e23ee',
        '1e2sde',
        '18a713',
        'b07cce',
        '9a8463',
        '8c2767',
        'e6e1f7',
        'd352bc',
        'b80be8',
        '26accc',
        '898dff',
        '15bc8d',
        'd41d8c',
        'd41d8c',
    ]

    target = [
        'c435ad',
        '11a90c',
        '187ef4',
        '024043',
        'cff069',
        'c72569',
        'c72569',
        '580253',
        '97f059',
        '1e23ee',
        '18a313',
        'b07cce',
        '9a8463',
        '8c2767',
        'e6e3f7',
        'd354bc',
        'b80be8',
        '26accc',
        '89ddff',
        '15bc8d',
        'd41d8c',
        'd41d8c',
    ]

    ms = difflib.SequenceMatcher(None, base, source)
    mt = difflib.SequenceMatcher(None, base, target)

    # matcher = difflib.SequenceMatcher(None, s1, s2)
    for s,t in zip(ms.get_opcodes(),mt.get_opcodes()):
        # tag, i1, i2, j1, j2
        print(s)
        print(t)