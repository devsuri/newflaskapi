import unittest
import os
import json
from app import create_app, db


class ResttestingTestCase(unittest.TestCase):
    """This class represents the Resttesting test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.Resttesting = {'name': 'Go to rest'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def register_user(self, email="richev@test.com", password="test1234"):
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/auth/register', data=user_data)

    def login_user(self, email="richev@test.com", password="test1234"):
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/auth/login', data=user_data)

    def test_Resttesting_creation(self):
        """Test API can create a Resttesting (POST request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post(
            '/resttest1/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.Resttesting)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Go to rest', str(res.data))

    def test_api_can_get_all_resttest1(self):
        """Test API can get a Resttesting (GET request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post(
            '/resttest1/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.Resttesting)
        self.assertEqual(res.status_code, 201)
        res = self.client().get(
            '/resttest1/',
            headers=dict(Authorization="Bearer " + access_token),
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn('Go to rest', str(res.data))

    def test_api_can_get_Resttesting_by_id(self):
        """Test API can get a single Resttesting by using it's id."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        rv = self.client().post(
            '/resttest1/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.Resttesting)
        self.assertEqual(rv.status_code, 201)
        results = json.loads(rv.data.decode())
        result = self.client().get(
            '/resttest1/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Go to rest', str(result.data))

    def test_Resttesting_can_be_edited(self):
        """Test API can edit an existing Resttesting. (PUT request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        rv = self.client().post(
            '/resttest1/',
            headers=dict(Authorization="Bearer " + access_token),
            data={'name': 'rest test only'})
        self.assertEqual(rv.status_code, 201)
        # get the json with the Resttesting
        results = json.loads(rv.data.decode())
        rv = self.client().put(
            '/resttest1/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token),
            data={
                "name": "rest testing start :-)"
            })

        self.assertEqual(rv.status_code, 200)
        results = self.client().get(
            '/resttest1/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token))
        self.assertIn('just start', str(results.data))

    def test_Resttesting_deletion(self):
        """Test API can delete an existing Resttesting. (DELETE request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        rv = self.client().post(
            '/resttest1/',
            headers=dict(Authorization="Bearer " + access_token),
            data={'name': 'rest test only'})
        self.assertEqual(rv.status_code, 201)
        # get the Resttesting in json
        results = json.loads(rv.data.decode())
        res = self.client().delete(
            '/resttest1/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token),)
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get(
            '/resttest1/1',
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()