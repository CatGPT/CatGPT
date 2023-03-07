from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from customapi.schemas import Login, Refresh, Register, Token, User, Image, SaveImage, Follow, SaveFollow
from customapi.services import add_user, get_user, get_images, add_image, get_follows, add_follow, remove_follow, get_follows_by_image_id
from customapi.utils import verify_password

router = APIRouter()


@router.post("/auth/login", response_model=Login)
def login(user: Token, authorize: AuthJWT = Depends()):
    if user.username and user.password:
        db_user = get_user(user.username)
        if db_user and verify_password(user.password, db_user.password):
            access_token = authorize.create_access_token(subject=user.username)
            refresh_token = authorize.create_refresh_token(subject=user.username)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
            }
    raise HTTPException(status_code=401, detail="Bad username or password")


@router.post("/auth/refresh", response_model=Refresh)
def refresh(authorize: AuthJWT = Depends()):
    authorize.jwt_refresh_token_required()

    current_user = authorize.get_jwt_subject()
    new_access_token = authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token, "token_type": "bearer"}


@router.get("/auth/me", response_model=User)
def protected(authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    current_user = authorize.get_jwt_subject()
    user = get_user(current_user)
    return User(**user.__dict__)


@router.post("/auth/register", response_model=User)
def protected(user: Register):
    new_user = Register(
        username=user.username,
        password=user.password,
        email=user.email,
        firstName=user.firstName,
        lastName=user.lastName,
    )
    user = add_user(new_user)
    return User(**user.__dict__)



@router.post("/saveImage", response_model=Image)
def saveImage(image: SaveImage, authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    current_user = authorize.get_jwt_subject()
    user = get_user(current_user)

    new_image = SaveImage(
        imageURL=image.imageURL,
        share=image.share
    )
    image = add_image(new_image, user)
    return Image(**image.__dict__)


@router.get("/getImages")
def getImages(authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    current_user = authorize.get_jwt_subject()
    user = get_user(current_user)
    images = get_images(user)
    print("--------------------> ", images)
    return {"images": images}


@router.post("/follow", response_model=Follow)
def saveImage(image: SaveFollow, authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    current_user = authorize.get_jwt_subject()
    user = get_user(current_user)

    new_follow = SaveFollow(
        imageID=image.imageID
    )
    follow = add_follow(new_follow, user)
    return Follow(**follow.__dict__)


@router.post("/unfollow")
def saveImage(image: SaveFollow, authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    current_user = authorize.get_jwt_subject()
    user = get_user(current_user)

    un_follow = SaveFollow(
        imageID=image.imageID
    )
    follow = remove_follow(un_follow, user)
    if follow == None:
        return {"message": "No image to unfollow at this time!"}
    else:
        return {"message": "Successfully unfollowed image!", "follow": Follow(**follow.__dict__)}


@router.get("/getFollows")
def getFollows(authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    current_user = authorize.get_jwt_subject()
    user = get_user(current_user)
    follows = get_follows(user)

    return {"follows": follows}


@router.get("/getFollowsByImageId/{imageId}")
def getFollowsByImageId(imageId: int, authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    current_user = authorize.get_jwt_subject()
    user = get_user(current_user)
    follow = get_follows_by_image_id(user, imageId)

    return {"followCnt": follow.followCnt}

