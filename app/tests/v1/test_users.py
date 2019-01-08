from flask import json
from .base_test import BaseTest

class TestUser(BaseTest):
    """ Test class for user endpoints """

    def setUp(self):
        """ Initialize variables to be used for user tests """
        super().setUp()

    def test_signup_no_data(self):
        """ Test sign up with no data sent """
        res = self.client.post('/api/v1/register')
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'No data provided')

    def test_signup_empty_data(self):
        """ Test sign up with empty data sent """
        user = {}

        res = self.client.post('/api/v1/register', json=json.dumps(user), headers={'Content-Type': 'application/json'})
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'No data provided')

    def test_signup_missing_fields(self):
        """ Test signup with missing fields in data sent """
        user = {
            'firstname' : 'Vincent',
            'lastname' : 'Tirgei',
            'password' : 'asfsgsdg'
        }

        res = self.client.post('/api/v1/register', json=json.dumps(user), headers={'Content-Type': 'application/json'})
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'Incomplete data. Please fill all required fields')

    def test_signup_invalid_email(self):
        """ Test sign up with invalid email """

        user = {
            'firstname' : 'Vincent',
            'lastname' : 'Tirgei',
            'othername' : 'Doe',
            'username' : 'tirgei',
            'email' : 'tirgei',
            'password' : 'asfsgsdg',
            'phonenumber' : '0712345678'
        }

        res = self.client.post('/api/v1/register', json=json.dumps(user), headers={'Content-Type': 'application/json'})
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'Invalid email')

    def test_signup_invalid_password(self):
        """ Test signup with invalid password """

        user = {
            'firstname' : 'Vincent',
            'lastname' : 'Tirgei',
            'othername' : 'Doe',
            'username' : 'tirgei',
            'email' : 'tirgei@gmail.com',
            'password' : 'asfsgsdg',
            'phonenumber' : '0712345678'
        }

        res = self.client.post('/api/v1/register', json=json.dumps(user), headers={'Content-Type': 'application/json'})
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'Invalid password')

    def test_signup(self):
        """ Test sign up with correct data """

        user = {
            'firstname' : 'Vincent',
            'lastname' : 'Tirgei',
            'othername' : 'Doe',
            'username' : 'tirgei',
            'email' : 'tirgei@gmail.com',
            'password' : 'asfD3#sdg',
            'phonenumber' : '0712345678'
        }

        res = self.client.post('/api/v1/register', json=json.dumps(user), headers={'Content-Type': 'application/json'})
        data = res.get_json()

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['status'], 201)
        self.assertEqual(data['error'], 'User created successfully')
        self.assertEqual(data['data']['username'], user['username'])

    def test_signup_existing_email(self):
        """ Test sign up with existing email """

        # Create new user and test response
        user_1 = {
            'firstname' : 'John',
            'lastname' : 'Doe',
            'othername' : 'Oketch',
            'username' : 'joketch',
            'email' : 'jd@gmail.com',
            'password' : 'asfD3#sdg',
            'phonenumber' : '0712345678'
        }

        res_1 = self.client.post('/api/v1/register', json=json.dumps(user_1), headers={'Content-Type': 'application/json'})
        data_1 = res_1.get_json()

        self.assertEqual(res_1.status_code, 201)
        self.assertEqual(data_1['status'], 201)

        # Create another user with same email
        user_2 = {
            'firstname' : 'Jane',
            'lastname' : 'Dilly',
            'othername' : 'Dudley',
            'username' : 'dilly',
            'email' : 'jd@gmail.com',
            'password' : 'asfD3#sdg',
            'phonenumber' : '0712345678'
        }

        res_2 = self.client.post('/api/v1/register', json=json.dumps(user_2), headers={'Content-Type': 'application/json'})
        data_2 = res_2.get_json()

        self.assertEqual(res_2.status_code, 409)
        self.assertEqual(data_2['status'], 409)
        self.assertEqual(data_2['error'], 'Email already exists')

    def test_signup_existing_username(self):
        """ Test sign up with existing username """

        # Create new user and test response
        user_1 = {
            'firstname' : 'John',
            'lastname' : 'Doe',
            'othername' : 'Oketch',
            'username' : 'doe',
            'email' : 'john@gmail.com',
            'password' : 'asfD3#sdg',
            'phonenumber' : '0712345678'
        }

        res_1 = self.client.post('/api/v1/register', json=json.dumps(user_1), headers={'Content-Type': 'application/json'})
        data_1 = res_1.get_json()

        self.assertEqual(res_1.status_code, 201)
        self.assertEqual(data_1['status'], 201)

        # Create another user with same email
        user_2 = {
            'firstname' : 'Jane',
            'lastname' : 'Dilly',
            'othername' : 'Dudley',
            'username' : 'doe',
            'email' : 'jdoe@gmail.com',
            'password' : 'asfD3#sdg',
            'phonenumber' : '0712345678'
        }

        res_2 = self.client.post('/api/v1/register', json=json.dumps(user_2), headers={'Content-Type': 'application/json'})
        data_2 = res_2.get_json()

        self.assertEqual(res_2.status_code, 409)
        self.assertEqual(data_2['status'], 409)
        self.assertEqual(data_2['error'], 'Username already exists')