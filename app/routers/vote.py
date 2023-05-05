from fastapi import FastAPI,Response,status,HTTPException,Depends, APIRouter
from ..import schemas, database, models, auth2
from sqlalchemy.orm import Session


router=APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote, db:Session=Depends(database.get_db),current_user:int=Depends(auth2.get_current_user)):

    post=db.query(models.Post).filter(models.Post.id== vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post with {vote.post_id} doea not exist")
    vote_query=db.query(models.Vote).filter(models.Vote.post_id==vote.post_id, models.Vote.user_id==current_user.id)
    
    found_vot= vote_query.first()
    if (vote.dir==1):
        if found_vot:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user{current_user.id} have already voted on post")
        new_id=models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_id)
        db.commit()
        return{"message":"added"}
    else:
        if not found_vot:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exict")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return{"message":"vote was deleted"}
