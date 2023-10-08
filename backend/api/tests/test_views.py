from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post
from ..forms import PostForm

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth_test1')
        cls.group = Group.objects.create(
            title='Тестовая группа 1',
            slug='test_slug1',
            description='Тестовое описание 1',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Тестовый пост 1',
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_index_show_correct_context(self):
        pages_context = [
            reverse('posts:index'),
            reverse(
                'posts:group_list', kwargs={'slug': self.group.slug}
            ),
            reverse(
                'posts:profile', kwargs={'username': self.user.username}
            ),
        ]
        for items in pages_context:
            with self.subTest(items=items):
                response = self.guest_client.get(items)
                self.assertIn(self.post, response.context['page_obj'])

    def test_post_detail_show_correct_context(self):
        response = self.guest_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.id})
        )
        self.assertEqual(response.context['post'], self.post)

    def test_post_edit_show_correct_form(self):
        response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id})
        )
        form = response.context['form']
        self.assertIsInstance(form, PostForm)
        self.assertEqual(form.instance, self.post)

    def test_post_create_show_correct_form(self):
        response = self.authorized_client.get(
            reverse('posts:post_create')
        )
        self.assertIsInstance(response.context['form'], PostForm)
