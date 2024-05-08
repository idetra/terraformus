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
