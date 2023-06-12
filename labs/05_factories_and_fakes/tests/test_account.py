"""
Test Cases TestAccountModel
"""

from unittest import TestCase
from models import db
from models.account import Account, DataValidationError
from factories import AccountFactory

ACCOUNT_DATA = {}

class TestAccountModel(TestCase):
    """Test Account Model"""

    @classmethod
    def setUpClass(cls):
        """ Load data needed by tests """
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def tearDownClass(cls):
        """Disconnext from database"""
        db.session.close()

    def setUp(self):
        """Truncate the tables"""
        db.session.query(Account).delete()
        db.session.commit()

    def tearDown(self):
        """Remove the session"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_all_accounts(self):
        """ Test creating multiple Accounts """
        for _ in range(10):
            account = AccountFactory()
            account.create()
        self.assertEqual(len(Account.all()), 10)
    
    def test_create_an_account(self):
        """ Test Account creation using known data """
        account = AccountFactory()
        account.create()
        self.assertEqual(len(Account.all()), 1)
    
    def test_to_dict(self):
        """ Test account to dict """
        account = AccountFactory()
        result = account.to_dict()
        keys = list(result.keys())
        for key in keys:
            self.assertEqual(getattr(account,key), result[f"{key}"])

    
    def test_from_dict(self):
        """ Test account from dict """
        data = AccountFactory().to_dict()
        account = Account()
        account.from_dict(data)
        keys = list(data.keys())
        for key in keys:
            self.assertEqual(getattr(account,key), data[f"{key}"])

    def test_update_an_account(self):
        """ Test Account update using known data """
        account = AccountFactory()
        account.create()
        new_data = {
            "name": "Trust",
            "email": "test@gmail.com",
            "phone_number": "+123456789"
        }
        self.assertIsNotNone(account.id)
        for key, val in new_data.items():  
            setattr(account, key, val) 
        account.update()
        found = Account.find(account.id)
        
        for key, val in new_data.items():
            self.assertEqual(getattr(found, key), val)

        
    def test_invalid_id_on_update(self):
        """ Test invalid ID update """
        account = AccountFactory()
        account.id = None
        self.assertRaises(DataValidationError, account.update)

    def test_delete_an_account(self):
        """ Test Account update using known data """
        account = AccountFactory()
        account.create()
        self.assertEqual(len(Account.all()), 1)
        account.delete()
        self.assertEqual(len(Account.all()), 0)