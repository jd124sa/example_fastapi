from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])

# ===========================   Posts =======================================================


# get all post
@router.get("/", response_model=list[schemas.PostOut])
# @router.get("/")
def get_posts(
    db: Session = Depends(get_db),
    ## query parameters
    limit: int = 10,
    skip: int = 0,
    search: str | None = "",
):
    # print("limit", limit)

    # posts = (
    #     db.query(models.Post)
    #     .filter(models.Post.title.contains(search))
    #     .limit(limit)
    #     .offset(skip)
    #     .all()
    # )

    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )

    return posts


## get individual post by id
@router.get("/{id}", response_model=schemas.PostOut)
# def get_post(id: int, db: Session = Depends(get_db)): -> dict:
def get_post(id: int, db: Session = Depends(get_db)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found",
        )
    return post


# create post
# data
# title str
# contetn str
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):

    # print(type(post))
    new_post = models.Post(**post.model_dump())
    new_post.owner_id = current_user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# delete post, delete request should retung nothing only the 204 no content header
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    # cursor.execute("DELETE FROM posts WHERE id = %(id)s RETURNING *", {"id": id})
    # deleted = cursor.fetchone()
    # print(current_user.email)

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found",
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not autorized to perfom requested action",
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update a post by id
@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    updated_post: schemas.PostUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found",
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not autorized to perfom requested action",
        )

    post_query.update(
        updated_post.model_dump(),
        synchronize_session=False,
    )
    db.commit()
    updated = post_query.first()
    return updated
