from typing import List, Optional

from customapi.database import session
from customapi.models import User, Image, Follow
from customapi.schemas import Register, User as UserSchema


def get_user(username: str) -> Optional[User]:
    with session() as db:
        return db.query(User).filter(User.username == username).one_or_none()


def add_user(user: Register) -> Optional[User]:
    db_user = User(**user.dict())
    with session() as db:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return db_user

def get_images(user: UserSchema) -> List[Image]:
    with session() as db:
        return db.query(Image).filter(Image.userID == user.id).all()
    
def add_image(image: Image, user: User) -> Optional[Image]:
    db_image = Image(
        imageURL=image.imageURL,
        share=image.share,
        userID=user.id
    )
    with session() as db:
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
    return db_image

def add_follow(follow: Follow, user: User) -> Optional[Follow]:
    with session() as db:
        db_follow = db.query(Follow).filter(Follow.imageID == follow.imageID).one_or_none()
        followCnt = 0
        if db_follow != None:
            followCnt = db_follow.followCnt
            db_follow.followCnt=followCnt+1
        else:
            db_follow = Follow(
                imageID=follow.imageID,
                followCnt=followCnt+1,
                followedBy=str(user.id)
            )
            db.add(db_follow)
        db.commit()
        db.refresh(db_follow)
    return db_follow

def get_follows(user: User) -> List[Image]:
    with session() as db:
        return db.query(Follow).filter(Follow.followedBy.in_([str(user.id)])).all()