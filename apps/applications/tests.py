from django.test import TestCase
from django.contrib.auth import get_user_model

from apps.applications.models import Plan, App, Subscription

User = get_user_model()

class AuthTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')

    def test_user_not_authenticated(self):
        response = self.client.get('/api/v1/applications/app/')
        self.assertEqual(response.status_code, 401)

        response = self.client.get('/api/v1/applications/plan/')
        self.assertEqual(response.status_code, 401)

        response = self.client.get('/api/v1/applications/subscription/')
        self.assertEqual(response.status_code, 401)
    
    def test_user_authenticated(self):
        self.client.login(username='test', password='test')
        response = self.client.get('/api/v1/applications/app/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/v1/applications/plan/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/v1/applications/subscription/')
        self.assertEqual(response.status_code, 200)
        

class AppTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user_app = App.objects.create(name='Test App', description='Test App Description', type='Django', framework='Django', domain_name='test.com', user=self.user)

        self.user_extra = User.objects.create_user(username='testuser_extra', password='12345')
        self.user_extra_app = App.objects.create(name='Test App Extra', description='Test App Description', type='Django', framework='Django', domain_name='test.com', user=self.user_extra)

    def test_app_listing(self):
        # Should list only apps created by the user
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/api/v1/applications/app/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test App')

    def test_app_creation(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/api/v1/applications/app/', {
            'name': 'Test App',
            'description': 'Test App Description',
            'type': 'Web',
            'framework': 'Django',
            'domain_name': 'testapp.com',
        })
        self.assertEqual(response.status_code, 201)

        created_app = App.objects.get(pk=response.data['id'])
        
        self.assertEqual(created_app.name, 'Test App')
        self.assertEqual(created_app.description, 'Test App Description')
        self.assertEqual(created_app.type, 'Web')
        self.assertEqual(created_app.framework, 'Django')
        self.assertEqual(created_app.domain_name, 'testapp.com')
        self.assertEqual(created_app.user, self.user)
    
    def test_app_editing(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.put(f'/api/v1/applications/app/{self.user_app.id}/', {
            'name': 'Test App Edited',
            'description': 'Test App Description Edited',
            'type': 'Web',
            'framework': 'Django',
            'domain_name': 'testapp.com',
        }, 'application/json')
        self.assertEqual(response.status_code, 200)

        edited_app = App.objects.get(pk=response.data['id'])
        
        self.assertEqual(edited_app.name, 'Test App Edited')
        self.assertEqual(edited_app.description, 'Test App Description Edited')
        self.assertEqual(edited_app.type, 'Web')
        self.assertEqual(edited_app.framework, 'Django')
        self.assertEqual(edited_app.domain_name, 'testapp.com')
        self.assertEqual(edited_app.user, self.user)
    
    def test_app_editing_another_users_app(self):
        """
        Should not be able to edit another users app
        """
        self.client.login(username='testuser_extra', password='12345')
        response = self.client.put(f'/api/v1/applications/app/{self.user_app.id}/', {
            'name': 'Test App Edited',
            'description': 'Test App Description Edited',
            'type': 'Web',
            'framework': 'Django',
            'domain_name': 'testapp.com',
        })
        self.assertEqual(response.status_code, 404)


class SubscriptionTestCase(TestCase):
    def setUp(self):
        self.plan = Plan.objects.create(name='Test Plan', description='Test Plan Description', price=10)
        self.plan2 = Plan.objects.create(name='Test Plan 2', description='Test Plan Description 2', price=20)

        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user_app = App.objects.create(name='Test App', description='Test App Description', type='Django', framework='Django', domain_name='test.com', user=self.user)

        self.user_extra = User.objects.create_user(username='testuser_extra', password='12345')
        self.user_extra_app = App.objects.create(name='Test App Extra', description='Test App Description', type='Django', framework='Django', domain_name='test.com', user=self.user_extra)

        # self.user_extra_subscription = Subscription.objects.create(app=self.user_extra_app, plan=self.plan, active = True)

    def test_subscription_listing(self):
        """
        Should list only subscriptions created by the user
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/api/v1/applications/subscription/')
        self.assertEqual(response.status_code, 200)
        # All subscriptions created by the user
        for subscription in response.data:
            self.assertEqual(subscription['user'], self.user)

        self.client.login(username='testuser_extra', password='12345')
        response = self.client.get('/api/v1/applications/subscription/')
        self.assertEqual(response.status_code, 200)
        for subscription in response.data:
            self.assertEqual(subscription['user'], self.user_extra)
    
    def test_subscription_on_a_app_from_another_user(self):
        """
        Test that a user can't create a subscription on an app created by another user
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/api/v1/applications/subscription/', {
            'app': self.user_extra_app.id,
            'plan': self.plan.id,
            'active': True,
        })
        self.assertEqual(response.status_code, 400)
    
    def test_subscription_creation(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/api/v1/applications/subscription/', {
            'app': self.user_app.id,
            'plan': self.plan.id,
            'active': True,
        })
        self.assertEqual(response.status_code, 201)

        created_subscription = Subscription.objects.get(pk=response.data['id'])
        
        self.assertEqual(created_subscription.app, self.user_app)
        self.assertEqual(created_subscription.plan, self.plan)
        self.assertEqual(created_subscription.active, True)
    
    def test_subscription_after_app_delete(self):
        """
        Test that a subscription is not deleted when the app is deleted
        """
        app = App.objects.create(name='Test App', description='Test App Description', type='Django', framework='Django', domain_name='test.com', user=self.user)
        
        self.client.login(username='testuser', password='12345')
        subs_response = self.client.post('/api/v1/applications/subscription/', {
            'app': app.id,
            'plan': self.plan.id,
            'active': True,
        })
        self.assertEqual(subs_response.status_code, 201)

        response = self.client.delete(f'/api/v1/applications/app/{app.id}/')
        self.assertEqual(response.status_code, 204)

        created_subscription = Subscription.objects.get(pk=subs_response.data['id'])
        
        self.assertEqual(created_subscription.app, None)
        self.assertEqual(created_subscription.plan, self.plan)
        self.assertEqual(created_subscription.active, True)
    
    def test_subscription_app_field_edit(self):
        """
        Test that the app field can not be edited
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/api/v1/applications/subscription/', {
            'app': self.user_app.id,
            'plan': self.plan.id,
            'active': True,
        })
        self.assertEqual(response.status_code, 201)

        created_subscription = Subscription.objects.get(pk=response.data['id'])
        
        self.assertEqual(created_subscription.app, self.user_app)
        self.assertEqual(created_subscription.plan, self.plan)
        self.assertEqual(created_subscription.active, True)

        response = self.client.patch(f'/api/v1/applications/subscription/{created_subscription.id}/', {
            'app': self.user_extra_app.id,
        }, 'application/json')
        self.assertEqual(response.status_code, 400)