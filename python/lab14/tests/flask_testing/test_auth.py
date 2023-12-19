from flask import url_for
from flask_login import current_user, login_user
from .base_test import BaseTest
from app.auth.models import User
from app import db

class AuthTest(BaseTest):

    def setUp(self):
        super().setUp()
        db.session.add(User(name='user', email='user@gmail.com', password='password'))
        db.session.commit()
        
    def test_view_login_page(self):

        response = self.client.get(url_for('auth.login'))

        self.assert200(response)
        self.assertIn(b'Email', response.data)
        self.assertIn(b'Password', response.data)
        self.assertIn(b'Remember me', response.data)
        self.assertIn(b'Sign in', response.data)

    def test_view_register_page(self):

        response = self.client.get(url_for('auth.register'))

        self.assert200(response) 
        self.assertIn(b'User name', response.data)
        self.assertIn(b'Email', response.data)
        self.assertIn(b'Password', response.data)
        self.assertIn(b'Confirm password', response.data)
        self.assertIn(b'Sign up', response.data)

    def test_register(self):

        with self.client:
            response = self.client.post(
                url_for('auth.register'),
                data=dict(username='TestUser', email='test@ukr.net.ua', password='1234567q', confirm_password='1234567q'),
                follow_redirects=True
            )

            self.assert200(response)
            self.assertMessageFlashed('Account created for TestUser!', 'success')
            
            user = User.query.filter_by(email='test@ukr.net.ua').first()
            self.assertEqual(user.email, 'test@ukr.net.ua')

    def test_login(self):

        with self.client:
            response = self.client.post(
                url_for('auth.login'),
                data=dict(email='user@gmail.com', password='password'),
                follow_redirects=True
            )

            self.assert200(response)
            self.assertMessageFlashed("Logged in successfully!!", 'success')
            self.assertEqual(current_user.username, 'user')

    def test_logout(self):

        login_user(User.query.filter_by(email='user@gmail.com').first())

        with self.client:
            response = self.client.post(
                url_for('auth.logout'),
                follow_redirects=True
            )

            self.assert200(response)
            self.assertMessageFlashed("Logged out successfully!!", 'success')
            self.assertFalse(current_user.is_authenticated)

    def test_update(self):

        login_user(User.query.filter_by(email='user@gmail.com').first())

        with self.client:
            response = self.client.post(
                url_for('auth.update_user'),
                data=dict(username='UpdatedUser', email='user@gmail.com', about_me="about"),
                follow_redirects=True
            )

            self.assert200(response)
            self.assertMessageFlashed("Info updated!", 'success')
            self.assertEqual(current_user.username, 'UpdatedUser')
            self.assertEqual(current_user.about_me, 'about')
