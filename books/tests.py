from django.test import TestCase

# Create your tests here.
from .models import Book

class BookTestCase(TestCase):
    def setUp(self):
        Book.objects.create(title="mytestbook")

    def test_book_title(self):
        test = Book.objects.get(title="mytestbook")
        print(test)
        self.assertEqual(test.title, 'mytestbook')
