# import jwt
# import pytest
# from app.config import settings
import pytest
from app import schemas


def test_get_all_posts(client, test_posts):
    res = client.get("/posts/")

    # def validate(post):
    #     return schemas.PostOut(post)

    # posts_map = map(validate, res.json())
    # post_list = list(posts_map)
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content
    assert res.status_code == 200


@pytest.mark.parametrize(
    "title, content, published",
    [
        ("awesome new title", "awesome new content", True),
        ("new post", "new post content with test_create_posts", False),
    ],
)
def test_create_posts(
    authorized_client, test_user, test_posts, title, content, published
):
    res = authorized_client.post(
        "/posts/",
        json={"title": title, "content": content, "published": published},
    )

    created_post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published


def test_create_post_default_published_true(authorized_client):
    res = authorized_client.post(
        "/posts/",
        json={
            "title": "default published",
            "content": "content default published",
        },
    )
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "default published"
    assert created_post.content == "content default published"
    assert created_post.published == True


def test_unauthorized_user_create_posts(client, test_posts):
    res = client.post(
        "/posts/",
        json={"title": "unauth user", "content": "cant create post not authorized"},
    )

    assert res.json().get("detail") == "Not authenticated"
    assert res.status_code == 401
    # "detail": "Not authenticated"


def test_get_one_posts_not_exist(client, test_posts):
    post_id = 88888
    res = client.get(f"/posts/{post_id}")
    # "detail": "Post with id: 343243 was not found"
    assert res.json().get("detail") == f"Post with id: {post_id} was not found"
    assert res.status_code == 404


def test_unauthorized_user_delete_posts(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")

    assert res.json().get("detail") == "Not authenticated"
    assert res.status_code == 401
    # "detail": "Not authenticated"


def test_delete_posts_success(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_posts_post_not_found(authorized_client):
    post_id = 33423
    res = authorized_client.delete(f"/posts/{post_id}")
    assert res.json().get("detail") == f"Post with id: {post_id} was not found"
    assert res.status_code == 404


def test_delete_posts_not_owner(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.json().get("detail") == "Not autorized to perfom requested action"
    assert res.status_code == 403


def test_update_posts_success(authorized_client, test_user, test_posts):

    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id,
    }

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]


def test_update_other_user_posts(authorized_client, test_user, test_user2, test_posts):

    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id,
    }

    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    # updated_post = schemas.Post(**res.json())
    assert res.status_code == 403
    # assert updated_post.title == data["title"]
    # assert updated_post.content == data["content"]


def test_unauthorized_user_update_posts(client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id,
    }
    res = client.put(f"/posts/{test_posts[0].id}", json=data)

    assert res.json().get("detail") == "Not authenticated"
    assert res.status_code == 401
    # "detail": "Not authenticated"


def test_update_posts_not_exist(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id,
    }
    post_id = 88888
    res = authorized_client.put(f"/posts/{post_id}", json=data)
    # "detail": "Post with id: 343243 was not found"
    assert res.json().get("detail") == f"Post with id: {post_id} was not found"
    assert res.status_code == 404
