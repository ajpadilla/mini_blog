import unittest

from sqlalchemy import desc

from app.auth.models import User
from app.models import Post, Comment
from . import BaseTestClass
from app import db


class PostModelTestCase(BaseTestClass):

    def test_title_slug(self):
        with self.app.app_context():
            admin = User.get_by_email('admin@xyz.com')
            post = Post(user_id=admin.id, title='Post de prueba', context='Lorem Ipsum')
            post.save()
            self.assertEqual('post-de-prueba', post.title_slug)

    def test_title_slug_duplicate(self):
        with self.app.app_context():
            admin = User.get_by_email('admin@xyz.com')
            post = Post(user_id=admin.id, title='Prueba', context='Lorem Ipsum')
            post.save()

            post_2 = Post(user_id=admin.id, title='Prueba', context='Lorem Ipsum Lorem Ipsum')
            post_2.save()
            self.assertEqual('prueba-1', post_2.title_slug)

            post_3 = Post(user_id=admin.id, title='Prueba', context='Lorem Ipsum Lorem Ipsum')
            post_3.save()
            self.assertEqual('prueba-2', post_3.title_slug)

            posts = Post.get_all()
            self.assertEqual(3, len(posts))

    def test_show_comments_from_post(self):
        with self.app.app_context():
            guest_user = User.get_by_email('guest@xyz.com')

            post = Post(user_id=guest_user.id, title='Prueba', context='Lorem Ipsum Lorem Ipsum')
            post.save()

            content = "is simply dummy text of the printing and typesetting industry.";
            comment = Comment(content=content, user_id=guest_user.id, user_name=guest_user.name, post_id=post.id)
            comment.save()

            print(f"Type de comentario {type(post.comments)}")
            print(f"Datos de cometario user_id: {comment.user_id}  post_id: {comment.post_id}")

            self.assertEqual(1, len(post.comments))

    def test_post_query_order_by_date(self):
        with self.app.app_context():
            admin_user = User.get_by_email('admin@xyz.com')
            guest_user = User.get_by_email('guest@xyz.com')

            post_0 = Post(user_id=admin_user.id, title='Prueba', context='Lorem Ipsum for user1')
            post_0.save()

            content = "is simply dummy text of the printing and typesetting industry.";
            comment = Comment(content=content, user_id=guest_user.id, user_name=guest_user.name, post_id=post_0.id)
            comment.save()

            post_1 = Post(user_id=guest_user.id, title='Prueba', context='Lorem Ipsum Lorem Ipsum')
            post_1.save()
            self.assertEqual('prueba-1', post_1.title_slug)

            content = "is simply dummy text of the printing and typesetting industry.2";
            comment = Comment(content=content, user_id=guest_user.id, user_name=guest_user.name, post_id=post_1.id)
            comment.save()

            post_2 = Post(user_id=guest_user.id, title='Prueba', context='Lorem Ipsum Lorem Ipsum')
            post_2.save()

            content = "is simply dummy text of the printing and typesetting industry.3";
            comment = Comment(content=content, user_id=guest_user.id, user_name=guest_user.name, post_id=post_2.id)
            comment.save()

            # post_list = db.session.query(Post)
            post_list = Post.query.order_by(desc(Post.user_id)).all()

            post_item = Post.query.filter(Post.user_id == 1).filter(Post.context.ilike('%user1%')).first()
            print(
                f"user_id: {post_item.user_id}, context {post_item.context} , post_id: {post_item.id} , comment: {post_item.comments}")

            post_item = Post.query.join(Post.comments).filter(Comment.content.ilike('%industry.3%')).first()
            print(f"Join user_id: {post_item.user_id}, context {post_item.context} , post_id: {post_item.id} , comment: {post_item.comments}")

            for post in post_list:
                print(f"user_id: {post.user_id}, post_id: {post.id} , comment: {post.comments}")

            self.assertIsNotNone(post_list)
