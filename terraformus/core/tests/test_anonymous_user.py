from django.test import TestCase
from terraformus.core.models import User, Solution, Strategy, Profile


class UserReplacementTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Test', password='Test')
        self.solution = Solution.objects.create(user=self.user)
        self.strategy = Strategy.objects.create(user=self.user)

    def test_replacement(self):
        self.user.delete()

        # Get the anonymous user which should be the only user left now
        anonymous_user = User.objects.filter(username__startswith='Anonymous-').last()

        self.assertIsNotNone(anonymous_user, 'Anonymous user was not created')

        # Reload the objects from the DB to get the updated user relations
        self.solution = Solution.objects.get(id=self.solution.id)
        self.strategy = Strategy.objects.get(id=self.strategy.id)

        self.assertEqual(self.solution.user, anonymous_user)
        self.assertEqual(self.strategy.user, anonymous_user)


class UserSetupTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Test', password='Test')
        self.solution = Solution.objects.create(user=self.user)
        self.strategy = Strategy.objects.create(user=self.user)

    def test_user_and_objects_creation(self):
        self.assertIsNotNone(self.user, 'User was not created')
        self.assertIsNotNone(self.solution, 'Solution was not created')
        self.assertIsNotNone(self.strategy, 'Strategy was not created')
        self.assertEqual(self.solution.user, self.user)
        self.assertEqual(self.strategy.user, self.user)

    def test_user_deletion(self):
        self.user.delete()
        self.assertFalse(User.objects.filter(username='Test').exists(), 'User was not deleted')

    def test_anonymous_user_creation(self):
        self.user.delete()
        anonymous_user = User.objects.filter(username__startswith='Anonymous-').last()
        self.assertIsNotNone(anonymous_user, 'Anonymous user was not created')

    def test_objects_update_to_anonymous_user(self):
        self.user.delete()
        anonymous_user = User.objects.filter(username__startswith='Anonymous-').last()

        # Reload the objects from the DB to get the updated user relations
        solution = Solution.objects.get(id=self.solution.id)
        strategy = Strategy.objects.get(id=self.strategy.id)

        self.assertIsNotNone(anonymous_user, 'Anonymous user was not created')
        self.assertEqual(solution.user, anonymous_user, 'Solution user not updated to anonymous')
        self.assertEqual(strategy.user, anonymous_user, 'Strategy user not updated to anonymous')
