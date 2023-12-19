from flask import url_for
from app.posts.models import Tag


def test_tags_page(client, init_database, logged_in_user, tags):
    response = client.get(url_for('posts.tags_page'))
    
    data = response.get_data(as_text=True)
    
    for tag in tags:
        assert tag.name in data
    
    assert len(tags) == len(Tag.query.all())


def test_create_tag(client, init_database, logged_in_user):
    data = {
        'name' : 'New tag',
    }

    response = client.post(url_for('posts.add_tag'), data=data ,follow_redirects=True)
    
    created = Tag.query.filter_by(name=data['name']).first()

    assert created is not None
    assert response.request.path == url_for('posts.tags_page')
    assert f'Tag (#{created.name}) created!' in response.get_data(as_text=True)


def test_delete_tag(client, init_database, logged_in_user, tags):
    tag = tags[0]

    response = client.post(url_for('posts.delete_tag', id=tag.id), follow_redirects=True)
    
    deleted = Tag.query.filter_by(id=tag.id).first()

    assert deleted is None
    assert response.request.path == url_for('posts.tags_page')
    assert f'Tag (#{tag.name}) deleted!' in response.get_data(as_text=True)
