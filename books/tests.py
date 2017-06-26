from django.test import TestCase, LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# browser = webdriver.Chrome()
# browser.get('http://google.com')
# browser.quit()
# dr = webdriver.PhantomJS()
import json
from rest_framework.test import APIRequestFactory, APITestCase

factory = APIRequestFactory()
request = factory.post('/listbooks/', {'title': 'new idea'}, format='json')

from .models import Book
from django.urls import reverse
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from .views import *
# c = Client()
from selenium.webdriver.common.by import By


# print(json.dumps({'4':5, '6':7}), sort_keys=True,indent=4)


def create_title(title):
    return Book.objects.create(title=title)

class APITest(APITestCase):
    def test_create_book(self):
        url = reverse('listbooks')
        # url='/listbooks/'
        data = {'title': 'test title', 'author':'test author'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get().title, 'test title')
        self.assertEqual(Book.objects.get().author, 'test author')
        self.assertEqual(Book.objects.get().id, 1)
        data = {'x': 'test title'}
        response = self.client.post(url, data, format='json')
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        view = BookDetail.as_view()
        request = factory.get('/bookdetail/1')
        response = view(request, pk='1')
        response.render()
        print (response.content)

        self.assertEqual(response.content, b'{"id":1,"title":"test title","author":"test author"}')


        view = BookList.as_view()
        request = factory.post('/booklist', {'title': 'new idea'}, format='json')
        response = view(request)
        response.render()
        print(response.content)

        self.assertEqual(Book.objects.count(), 2)


        view = BookDetail.as_view()
        request = factory.put('/bookdetail/1', {'title': 'put book', 'author':'put author'}, format='json')
        response = view(request, pk='1')
        response.render()

        self.assertEqual(response.content,  b'{"id":1,"title":"put book","author":"put author"}')
        self.assertEqual(Book.objects.count(), 2)

        view = BookDetail.as_view()
        request = factory.delete('/bookdetail/2')
        response = view(request, pk='2')
        response.render()

        self.assertEqual(Book.objects.count(), 1)


#














class AdminTestCase(LiveServerTestCase):
    def setUp(self):
        User.objects.create_superuser(
        username="admin",
        password="admin",
        email="admin@example.com"
        )

        # self.selenium = webdriver.Chrome()

        self.selenium = webdriver.PhantomJS()
        self.selenium.maximize_window()
        super(AdminTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(AdminTestCase, self).tearDown()


    def test_admin_site(self):
        self.selenium.get(self.live_server_url + '/admin/')
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)
        username_field = self.selenium.find_element_by_name('username')
        username_field.send_keys('admin')
        password_field = self.selenium.find_element_by_name('password')
        password_field.send_keys('admin')
        password_field.send_keys(Keys.RETURN)

        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Site administration', body.text)
        self.assertIn('Books', body.text)

    def test_index_site(self):
        self.selenium.get(self.live_server_url + '/books/')
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Your Library of Books', body.text)

    def test_add_update_delete_site(self):
        #  add a book
        self.selenium.get(self.live_server_url + '/books/add')
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Add a book', body.text)
        add_book_field = self.selenium.find_element_by_id('id_title')
        add_book_field.send_keys('selenium test book')
        add_book_field.send_keys(Keys.RETURN)
        self.selenium.get(self.live_server_url + '/books/')
        body = self.selenium.find_element_by_tag_name('li')
        print(body)
        self.assertIn('selenium test book', body.text)
        test = Book.objects.get(title="selenium test book")
        specific = Book.objects.get(title="selenium test book").id

        # view the details of a book
        self.selenium.get(self.live_server_url + '/books/' + str(specific))
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('DETAIL VIEW', body.text)
        # update a book
        self.selenium.get(self.live_server_url + '/books/' + str(specific) + '/books_update_form')
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Update', body.text)
        update_book_field = self.selenium.find_element_by_id('id_title')
        update_book_field.send_keys('update test book')
        update_book_field.send_keys(Keys.RETURN)
        self.selenium.get(self.live_server_url + '/books/')
        body = self.selenium.find_element_by_tag_name('li')
        self.assertIn('update test book', body.text)
        # delete a book
        self.selenium.get(self.live_server_url + '/books/' + str(specific) + '/book_confirm_delete')
        body = self.selenium.find_element_by_tag_name('p')
        self.assertIn('Are you sure you want to delete', body.text)
        delete_book = self.selenium.find_element_by_id('deleteBook').click()
        self.selenium.get(self.live_server_url + '/books/')
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Add', body.text)
        p = self.selenium.find_element_by_id('no')
        self.assertIn('No Books', p.text)




class BookTestCase(TestCase):
    def setUp(self):
        Book.objects.create(title="mytestbook")

    def test_book_title(self):
        test = Book.objects.get(title="mytestbook")
        print(test)
        self.assertEqual(test.title, 'mytestbook')

# def create_title(title):
#     return Book.objects.create(title=title)

class BookIndexViewTests(TestCase):
    def test_no_titles(self):
        response = self.client.get(reverse('books:index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response, 'No Books')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_past_title(self):
        create_title(title="past_title")
        response=self.client.get(reverse('books:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Book: past_title>'])
