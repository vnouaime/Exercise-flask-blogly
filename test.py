from unittest import TestCase
from app import app
from flask import session
from models import db, connect_db, default_image, User, Post

class FlaskTests(TestCase): 
    
    def setUp(self): 
        """Set up the Flask app for testing."""
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
        app.config['SQLALCHEMY_ECHO'] = False
        app.config['TESTING'] = True 
        connect_db(app)
        db.create_all()

    def tearDown(self): 
        """ Deletes test users from database """ 

        db.session.close()

    def test_home_page(self): 
        """ Tests redirect to users route and status code """
        with app.test_client() as client: 

            response = client.get('/')

            self.assertEqual(response.status_code, 302)  
            self.assertEqual(response.location, '/users') 
            

    def test_users(self): 
        """ Tests user page to make sure that database is working and displaying
        the list of users in html page"""
        with app.test_client() as client:

            response = client.get('/users')
            html = response.get_data(as_text=True)
            user_1 = User.query.filter_by(first_name="Vera", last_name="Nouaime").first()
            user_2 = User.query.filter_by(first_name="John", last_name="Smith").first()
            user_3 = User.query.filter_by(first_name="Susie", last_name="Sal").first()

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1>Users:</h1>', html)
            self.assertIn(f'<li><a href="/users/{user_1.id}">Vera Nouaime</a></li>', html)
            self.assertIn(f'<li><a href="/users/{user_2.id}">John Smith</a></li>', html)
            self.assertIn(f'<li><a href="/users/{user_3.id}">Susie Sal</a></li>', html)
        

    def test_user_page(self): 
        """ Tests to make sure that image, full name, edit, and delete button are all 
        being displayed with html to user"""
        with app.test_client() as client: 
            
            user = User.query.filter_by(first_name="Vera", last_name="Nouaime").first()

            response = client.get(f'/users/{user.id}')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertTrue(user.image_url)
            self.assertIn(f'<img class="profile_pic" src="{user.image_url}" alt="{user.get_full_name}">', html)
            self.assertIn('<button type="submit" class="edit_button">Edit</button>', html)
            self.assertIn('<button type="submit" class="delete_button">Delete</button>', html)

    def test_new_user_form(self):
        """ Testing post request for creating new user"""
        with app.test_client() as client: 

            data = {'first_name': 'Leo', 'last_name': 'Star', 'image_url': default_image}

            response = client.post('/users/new', data=data, follow_redirects=True)
            user = User.query.filter_by(first_name="Leo", last_name="Star").first()
            html = response.get_data(as_text=True)


            self.assertEqual(response.status_code, 200)
            self.assertIn(f'<li><a href="/users/{user.id}">Leo Star</a></li>', html)
            

            


