from flask import url_for
from .base_test import BaseTest

class ResumeTest(BaseTest):
        
    def test_view_about_page(self):
        '''Tests an about page contains name'''

        response = self.client.get(url_for('resume.about_page'))   

        self.assert200(response)
        self.assertIn(b'Dmytro Ivanov', response.data)

    def test_view_contacts_page(self):
        '''Tests an contacts page contains phone, email, github'''
        
        response = self.client.get(url_for('resume.contacts_page'))

        self.assert200(response)
        self.assertIn(b'Phone', response.data)
        self.assertIn(b'Email', response.data)
        self.assertIn(b'Github', response.data)

    def test_view_skills_page(self):
        '''Tests an skills page contains some skills and image link'''

        response = self.client.get(url_for('resume.skills_page'))

        self.assert200(response)
        self.assertIn(b'Java', response.data)
        self.assertIn(b'Python', response.data)
        self.assertIn(f"{url_for('resume.static', filename='images/java.svg')}".encode(), response.data) 
