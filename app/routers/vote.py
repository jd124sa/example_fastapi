from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

# from sqlalchemy.sql.functions import current_user
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/vote", tags=["Vote"])

# ===========================   Votes =======================================================

#
# @router.get("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Vote)
# # def get_post(id: int, db: Session = Depends(get_db)): -> dict:
# def get_post(id: int, db: Session = Depends(get_db)):
#     post = db.query(models.Post).filter(models.Post.id == id).first()
#     if post is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post with id: {id} was not found",
#         )
#     return post


# vote post
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(
    vote: schemas.Vote,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {vote.post_id} was not found",
        )

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                detail=f"user {current_user.id} has already voted on post {vote.post_id}",
            )

        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}
