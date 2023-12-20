from flask import url_for
from app.posts.models import Post, EnumPriority


#  --- Posts page ---

def test_posts_page_show_my_disabled(client, init_database, logged_in_user, posts):
    response = client.get(url_for('posts.posts_page'))
    
    assert response.status_code == 200
    assert posts[0].title in response.get_data(as_text=True)


def test_posts_page_not_show_disabled(client, init_database, logged_in_user, posts):
    response = client.get(url_for('posts.posts_page'))
    
    assert response.status_code == 200
    assert posts[2].title not in response.get_data(as_text=True)


def test_posts_page_user_not_authorized(client, init_database):
    response = client.get(url_for('posts.posts_page'), follow_redirects=True)
    
    assert response.request.path == url_for('auth.login')


def test_posts_page_show_selected_category(client, init_database, logged_in_user, categories):
    selected_category = categories[0]

    response = client.get(url_for('posts.posts_page', category=selected_category.id))
    
    assert selected_category.name in response.get_data(as_text=True)
    assert f'<span class="badge bg-primary">{categories[1].name}</span>' not in response.get_data(as_text=True)


#  --- Post page ---

def test_post_page_show_author_view(client, init_database, logged_in_user, posts):
    post = posts[0]

    response = client.get(url_for('posts.post_page', id=post.id))
    
    assert post.title in response.get_data(as_text=True)
    assert 'Update' in response.get_data(as_text=True)
    assert 'Delete' in response.get_data(as_text=True)


def test_post_page_post_not_exists(client, init_database, logged_in_user):
    response = client.get(url_for('posts.post_page', id=200), follow_redirects=True)
    
    assert response.status_code == 404


#  --- Post creation ---

def test_create_post(client, init_database, logged_in_user, categories, tags):
    data = {
        'title' : 'New post',
        'text' : 'Random text',
        'type' : EnumPriority.high.value,
        'enabled' : False,
        'categories' : categories[0].id,
        'tags' : [tags[0].id, tags[1].id],
    }

    response = client.post(url_for('posts.add_post'), data=data ,follow_redirects=True)
    
    created = Post.query.filter_by(title='New post').first()

    assert created is not None
    assert created.user_id == logged_in_user.id
    assert created.category.name == categories[0].name
    assert response.request.path == url_for('posts.post_page', id=created.id)
    assert 'Post created!' in response.get_data(as_text=True)

def test_create_post_validation_error(client, init_database, logged_in_user, categories, tags):
    data = {
        'title' : '',
        'text' : 'Random text',
        'type' : EnumPriority.high.value,
        'enabled' : False,
        'categories' : categories[0].id,
        'tags' : [tags[0].id, tags[1].id],
    }

    response = client.post(url_for('posts.add_post'), data=data ,follow_redirects=True)
    
    created = Post.query.filter_by(title='').first()

    assert created is None
    assert response.request.path == url_for('posts.add_post')
    assert 'Title is required' in response.get_data(as_text=True)


#  --- Post update ---

def test_update_post(client, init_database, logged_in_user, posts, tags):
    to_update = posts[1]
    data = {
        'title' : to_update.title,
        'text' : to_update.text,
        'type' : to_update.type.value,
        'enabled' : True,
        'categories' : to_update.category_id,
        'tags' : [tags[0].id],
    }

    response = client.post(url_for('posts.update_post', id=to_update.id), data=data ,follow_redirects=True)
    
    updated = Post.query.filter_by(id=to_update.id).first()

    assert updated is not None
    assert len(updated.tags) == 1
    assert updated.enabled == True
    assert response.request.path == url_for('posts.post_page', id=updated.id)
    assert f'Post ({updated.title}) updated!' in response.get_data(as_text=True)

#  --- Post delete ---

def test_delete_post(client, init_database, logged_in_user, posts):
    post = posts[1]

    response = client.post(url_for('posts.delete_post', id=post.id), follow_redirects=True)
    
    deleted = Post.query.filter_by(id=post.id).first()

    assert deleted is None
    assert response.request.path == url_for('posts.posts_page')
    assert f'Post ({post.title}) deleted!' in response.get_data(as_text=True)

def test_delete_not_my_post(client, init_database, logged_in_user, posts):
    post = posts[2]

    response = client.post(url_for('posts.delete_post', id=post.id), follow_redirects=True)
    
    deleted = Post.query.filter_by(id=post.id).first()

    assert deleted is not None
    assert response.request.path == url_for('posts.posts_page')
