from flask import url_for
from app.posts.models import PostCategory


def test_categories_page(client, init_database, logged_in_user, categories):
    response = client.get(url_for('posts.categories_page'))

    data = response.get_data(as_text=True)
    
    for category in categories:
        assert category.name in data

    assert len(categories) == len(PostCategory.query.all())


def test_create_category(client, init_database, logged_in_user):
    data = {
        'name' : 'New category',
    }

    response = client.post(url_for('posts.add_category'), data=data ,follow_redirects=True)
    
    created = PostCategory.query.filter_by(name=data['name']).first()

    assert created is not None
    assert response.request.path == url_for('posts.categories_page')
    assert f'Category ({created.name}) created!' in response.get_data(as_text=True)


def test_delete_category(client, init_database, logged_in_user, categories):
    category = categories[1]

    response = client.post(url_for('posts.delete_category', id=category.id), follow_redirects=True)
    
    deleted = PostCategory.query.filter_by(id=category.id).first()

    assert deleted is None
    assert response.request.path == url_for('posts.categories_page')
    assert f'Category ({category.name}) deleted!' in response.get_data(as_text=True)
