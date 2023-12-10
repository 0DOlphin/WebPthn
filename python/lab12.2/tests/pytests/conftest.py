import pytest
from flask import url_for
from app import create_app, db
from app.auth.models import User
from app.posts.models import Post, PostCategory, Tag, EnumPriority
from datetime import date

@pytest.fixture(scope='module')
def client():
    app = create_app('test')

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()


@pytest.fixture(scope='module')
def default_user():
    user = User(name='John Doe', email='john.doe@gmail.com', password='password')
    yield user

@pytest.fixture(scope='module')
def tags():
    tags = [Tag(name='cars'),  Tag(name='cool'),  Tag(name='dogs'),  Tag(name='rock')]
    yield tags

@pytest.fixture(scope='module')
def categories():
    categories = [PostCategory(name='music'), PostCategory(name='programming')]
    yield categories

@pytest.fixture(scope='module')
def posts(categories, tags):
    posts= [
        Post(title='Extra News', text='flask app', created=date(2023, 12, 6), type=EnumPriority.high, enabled=False, category=categories[0], tags=[tags[0]]),
        Post(title='What is the best?', text='Java or Python', created=date(2023, 12, 7), type=EnumPriority.medium, enabled=True, category=categories[1], tags=[tags[0], tags[3]]),
        Post(title='Symphony of Destruction', text='Cool music', created=date(2023, 12, 8), type=EnumPriority.low, enabled=False, category=categories[0], tags=[tags[2], tags[1]])
    ]
    yield posts


@pytest.fixture(scope='module')
def init_database(default_user, posts, categories):
    
    user2 = User(name='Test user', email='test@gmail.com', password='password')
    
    user2.posts = [posts[2]]
    default_user.posts = [posts[0], posts[1]]

    db.session.add_all([default_user, user2, categories[0], categories[1]])
    db.session.commit()

    yield

@pytest.fixture(scope='function')
def logged_in_user(client, default_user):
    client.post(
        url_for('auth.login'),
        data={'email': default_user.email, 'password': 'password'},
        follow_redirects=True
    )

    yield default_user

    client.post(url_for('auth.logout'))

