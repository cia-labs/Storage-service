from s1_client import crud

def test_post():
    assert crud.post() == 'posted'
