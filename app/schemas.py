from datetime import datetime
from pydantic import BaseModel, EmailStr, conint


# ----- REQUEST SCHEMAS
## used to validate the data of the request
class PostBase(BaseModel):
    title: str  # validates that title is a string
    content: str
    published: bool = True  # validates published is a boolean  an sets True as default


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class UserBase(BaseModel):
    password: str
    email: EmailStr  # validates that title is a string
    # published: bool = True  # validates published is a boolean  an sets True as default


class UserCreate(UserBase):
    pass


class UserLogin(BaseModel):
    password: str
    email: EmailStr  # validates that title is a string


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)


# ----- RESPONSE SCHEMAS


class UserOut(BaseModel):

    id: int
    email: EmailStr  # validates that title is a string
    created_at: datetime

    class Config:
        # orm_mode = True
        from_attributes = True


class Post(PostBase):

    id: int
    # owner_id: int
    # published: bool
    created_at: datetime
    owner: UserOut

    class Config:
        # orm_mode = True
        from_attributes = True


#
# "Post": {
#            "content": "hello this is my edit",
#            "created_at": "2025-09-09T15:17:00.622492+00:00",
#            "id": 8,
#            "owner_id": 14,
#            "published": true,
#            "title": "update post by test 4"
#        },
#        "votes": 1
class PostOut(BaseModel):

    Post: Post
    votes: int

    class Config:
        # orm_mode = True
        from_attributes = True
