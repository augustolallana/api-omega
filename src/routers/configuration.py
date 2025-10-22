from fastapi import APIRouter, HTTPException, status, Depends
from starlette import status
from src.schemas.base import BaseResponse
from src.models.configuration import ConfigSchema, Config
from sqlmodel import Session, select 
from src.database.config import get_current_user, get_session

router = APIRouter(prefix="/configuration", tags=["configuration"])


@router.post("/", response_model=BaseResponse)
def save_config(config: ConfigSchema, session: Session = Depends(get_session), auth=Depends(get_current_user)):
    new_config = Config(data=config.dict(exclude_unset=True))
    session.add(new_config)
    session.commit()
    session.refresh(new_config)
    return BaseResponse(
        message="Configuration endpoint reached.",
        status_code=status.HTTP_200_OK,
        detail={new_config.id: new_config.data},
    )
    

@router.get("/")
def get_latest_config(session: Session = Depends(get_session), auth=Depends(get_current_user)):
    statement = select(Config).order_by(Config.created_at.desc()).limit(1)
    config = session.exec(statement).first()
    if not config:
        raise HTTPException(status_code=404, detail="No configuration found")
    return {
        "id": config.id,
        "created_at": config.created_at,
        "data": config.data,
    }
