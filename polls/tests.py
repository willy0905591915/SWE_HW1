from django.test import TestCase
from django.urls import reverse
from .models import Question, Choice
from django.utils import timezone


class PollsViewTests(TestCase):

    def setUp(self):
        """Set up a sample question for testing."""
        self.question = Question.objects.create(
            question_text="Sample Question", pub_date=timezone.now()
        )
        self.choice1 = Choice.objects.create(
            question=self.question, choice_text="Option 1", votes=0
        )
        self.choice2 = Choice.objects.create(
            question=self.question, choice_text="Option 2", votes=0
        )

    def test_index_view_status_code(self):
        """Test that the index page loads successfully."""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sample Question")

    def test_detail_view_status_code(self):
        """Test that the detail page for a poll loads successfully."""
        response = self.client.get(reverse("polls:detail", args=[self.question.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.question.question_text)

    def test_results_view_status_code(self):
        """Test that the results page loads successfully."""
        response = self.client.get(reverse("polls:results", args=[self.question.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.question.question_text)

    def test_vote_functionality(self):
        """Test the vote functionality."""
        response = self.client.post(
            reverse("polls:vote", args=[self.question.id]), {"choice": self.choice1.id}
        )
        self.choice1.refresh_from_db()  # Refresh to get updated vote count
        self.assertEqual(self.choice1.votes, 1)
        self.assertRedirects(
            response, reverse("polls:results", args=[self.question.id])
        )
