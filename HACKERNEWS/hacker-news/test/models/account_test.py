from src.models.account import Account

def test_create_account():
    acc = Account("abc", "123")
    assert acc.username == "abc"
