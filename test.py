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
        db.create_all()

    def tearDown(self): 
        """ Deletes test users from database """ 

        db.session.close()

    #####################################################################################################################
    # User Route Tests
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

            user_1 = User.query.get(1)
            user_2 = User.query.get(2)
            user_3 = User.query.get(3)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1>Users:</h1>', html)
            self.assertIn(f'<li><a href="/users/{user_1.id}">{user_1.get_full_name}</a></li>', html)
            self.assertIn(f'<li><a href="/users/{user_2.id}">{user_2.get_full_name}</a></li>', html)
            self.assertIn(f'<li><a href="/users/{user_3.id}">{user_3.get_full_name}</a></li>', html)
        

    def test_user_page(self): 
        """ Tests to make sure that image, full name, edit, and delete button are all 
        being displayed with html to user"""
        with app.test_client() as client: 
            
            user = User.query.get(1)
            posts = Post.query.filter_by(user_FK=user.id).all()

            response = client.get(f'/users/{user.id}')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertTrue(user.image_url)
            self.assertIn(f'<img class="profile_pic" src="{user.image_url}" alt="{user.get_full_name}">', html)
            self.assertIn(f'<h1 class="user_name">{user.get_full_name}</h1>', html)
            self.assertIn('<button type="submit" class="button_profile_page edit">Edit</button>', html)
            self.assertIn('<button type="submit" class="button_profile_page delete">Delete</button>', html)
            self.assertIn('<h2>Posts</h2>', html)
        
            for post in posts: 
                self.assertIn(f'<li><a href="/posts/{post.id}">{post.title}</a></li>', html)


    def test_display_new_user_form(self): 
        """ Tests display of new user form """
        with app.test_client() as client: 

            response = client.get("/users/new")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1>Create New User: </h1>', html)
            self.assertIn('<input name="first_name" id="first_name" placeholder="Enter a first name" required>', html)
            self.assertIn('<input name="last_name" id="last_name" placeholder="Enter a last name" required>', html) 
            self.assertIn('<input name="image_url" id="image_url" placeholder="Provide an image of this user">', html)
            self.assertIn('<button class="green_button" type="submit">Add</button>', html)
            
    def test_new_user_form(self):
        """ Testing POST request for creating new user"""
        with app.test_client() as client: 

            if User.query.get(4) is None: 
            
                data = {'first_name': 'Leo', 'last_name': 'Star', 'image_url': default_image}

                response = client.post('/users/new', data=data, follow_redirects=True)
                user = User.query.get(4)
                html = response.get_data(as_text=True)

                self.assertEqual(response.status_code, 200)
                self.assertIn(f'<li><a href="/users/{user.id}">{user.get_full_name}</a></li>', html)

    def test_display_edit_user_form(self): 
        """ Tests display of edit user form """
        with app.test_client() as client: 

            user = User.query.get(1)

            response = client.get(f'/users/{user.id}/edit')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(f'<title>Edit {user.get_full_name}</title>', html)
            self.assertIn('<input name="first_name" id="first_name" placeholder="Enter a first name">', html)
            self.assertIn('<input name="last_name" id="last_name" placeholder="Enter a last name">', html)
            self.assertIn('<input name="image_url" id="image_url" placeholder="Provide an image of this user">', html)
            
    def test_edit_user_form(self):
        """ Testing POST request for editing existing user """
        with app.test_client() as client: 
            
            user = User.query.get(1)
            data = {'first_name': 'Amanda', 'last_name': 'Comet', 'image_url': default_image }

            if (user.first_name != data["first_name"]) or (user.last_name != data["last_name"]) or (user.image_url != data["image_url"]): 

                response = client.post(f'/users/{user.id}/edit', data=data, follow_redirects=True)
                html = response.get_data(as_text=True)
                
                self.assertEqual(response.status_code, 200)
                self.assertIn(f'<img class="profile_pic" src="{data["image_url"]}" alt="{data["first_name"]} {data["last_name"]}">', html)
                self.assertIn(f'<h1 class="user_name">{data["first_name"]} {data["last_name"]}</h1>', html)

    def test_user_delete(self): 
        """ Tests POST request of deleting a user """ 
        with app.test_client() as client: 
            
            user = User.query.get(5)
            if user is not None:
            
            
                response = client.post(f'/users/{user.id}/delete', follow_redirects=True)
         
                self.assertEqual(response.status_code, 200)
                self.assertIsNone(user)


    #####################################################################################################################
    # Post Route Tests

    def test_new_post(self):
        """ Testing display of new post form """ 
        with app.test_client() as client: 

            user = User.query.get(1)
            response = client.get(f'/users/{user.id}/posts/new')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(f'<h1>Add New Post for {user.get_full_name} </h1>', html)
            self.assertIn('<input name="title" id="title" placeholder="Enter a title" required>', html)
            self.assertIn('<input name="content" id="content" placeholder="Enter content" required>', html)
            self.assertIn('<button class="green_button" type="submit">Add</button>', html)
            self.assertIn('<button type="submit" class="button_profile_page edit">Cancel</button>', html)
    
    def test_create_new_post(self): 
        """ Tests POST request for new post for user """
        with app.test_client() as client: 

            if Post.query.get(11) is None: 
            
                user = User.query.get(1)

                data = {'title': 'Test Post Case', 'content': 'This is a test to make sure that new posts are created'}

                response = client.post(f'/users/{user.id}/posts/new', data=data, follow_redirects=True)
                post = Post.query.get(11)
                html = response.get_data(as_text=True)

                self.assertEqual(response.status_code, 200)
                self.assertIn(f'<li><a href="/posts/{post.id}">{post.title}</a></li>', html)

    def test_display_post(self): 
        """ Tests display page for individual post with title, content, and author shown """
        with app.test_client() as client: 

            post = Post.query.get(1)

            response = client.get(f"/posts/{post.id}")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(f'<h1>{post.title}</h1>', html)
            self.assertIn(f'<p class="post_content">{ post.content }</p>', html)
            self.assertIn(f'<p><i>By: {post.user.get_full_name}</i></p>', html)
            self.assertIn(f'<button type="submit" class="button_profile_page cancel">Cancel</button>', html)
            self.assertIn(f'<button type="submit" class="button_profile_page edit">Edit</button>', html)
            self.assertIn(f'<button type="submit" class="button_profile_page delete">Delete</button>', html)

    def test_display_post_edit(self): 
        """ Tests display of edit post form """
        with app.test_client() as client: 

            post = Post.query.get(1)

            response = client.get(f'/posts/{post.id}/edit')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(f'<title>Edit {post.title} By {post.user.get_full_name}</title>', html)
            self.assertIn(f'<input name="title" id="title" value="{ post.title}">', html)
            self.assertIn(f'<input name="content" id="content" value="{post.content}">', html)

    def test_post_edit(self):
        """ Testing POST request for editing existing post """
        with app.test_client() as client: 
            
            post = Post.query.get(1)
            data = {'title': 'Hello World', 'content': post.content}

            if (post.title != data['title']) or (post.content != data['content']): 

                response = client.post(f'/posts/{post.id}/edit', data=data, follow_redirects=True)
                html = response.get_data(as_text=True)
                
                self.assertEqual(response.status_code, 200)
                self.assertIn(f'<h1>{data["title"]}</h1>', html)
                self.assertIn(f'<p class="post_content">{data["content"]}</p>', html)
                self.assertIn(f'<p><i>By: {post.user.get_full_name}</i></p>', html)
        
    def test_post_delete(self): 
        """ Testing POST request for deleting post """
        with app.test_client() as client: 

            post = Post.query.get(10)

            if post is not None:
            
                response = client.post(f'/posts/{post.id}/delete', follow_redirects=True)
         
                self.assertEqual(response.status_code, 200)
                self.assertIsNone(post)


    


