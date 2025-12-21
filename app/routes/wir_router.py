from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.models import WIR, WIRCreate
from app.db.main import getAsyncDB
import uuid
from typing import Annotated
from sqlmodel import select
from app.utils.user_utils import get_current_user
from app.db.models import UserPublic

wirRouter = APIRouter(prefix="/wir", tags=["wir"])

@wirRouter.get(
        "/",
        dependencies=[Depends(get_current_user)],
)
async def getWIRByUser(
    session: Annotated[AsyncSession, Depends(getAsyncDB)],
    current_user: Annotated[UserPublic, Depends(get_current_user)]
    
    ):
    statement = select(WIR).where(WIR.createdBy == current_user.id)
    results = await session.exec(statement)
    wir_list = results.all()
    return wir_list


# get WIR documents
@wirRouter.get("/{wirID}")
async def getWIRByID(wirID: uuid.UUID, session: AsyncSession = Depends(getAsyncDB)):
    wirInstant = await selectWIRByID(wirID, session)
    if not wirInstant:
        return {"message": "WIR Document not found"}
    return wirInstant


# create WIR document
@wirRouter.post("/create")
async def createWIR(
    current_user: Annotated[UserPublic, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(getAsyncDB)],
    wirData: WIRCreate, 
    ):
    wir_dump = wirData.model_dump()
    wir_dump["createdBy"] = current_user.id
    wir = WIR(**wir_dump)
    # print("type issuingDate:", type(wir.plannedInspDate))
    session.add(wir)
    await session.commit()
    await session.refresh(wir)
    return wir


# update WIR document
@wirRouter.put("/update/{wirID}/")
async def updateWIR(wirID: uuid.UUID, wir: WIR, session: AsyncSession = Depends(getAsyncDB)):
    wirInstant = await selectWIRByID(wir.id, session)
    if not wirInstant:
        return {"message": "WIR Document not found"}
        
    wirUpdate = wir.dict(exclude_unset=True)
    for key, value in wirUpdate.items():
        setattr(wirInstant, key, value)
    await session.commit()
    await session.refresh(wirInstant)
    return wirInstant


# delete WIR document
@wirRouter.delete("/delete/{wirID}/")
async def deleteWIR(wirID: uuid.UUID, session: AsyncSession = Depends(getAsyncDB)):
    wirInstant = await selectWIRByID(wirID, session)
    if not wirInstant:
        return {"message": "WIR Document not found"}
    await session.delete(wirInstant)
    await session.commit()
    return {"message": "WIR Document deleted successfully"}





#! Should be abstracted to db operations
async def selectWIRByID(wirID: uuid.UUID, session: AsyncSession):
    wirResult = await session.execute(select(WIR).where(WIR.id == wirID))
    wirInstant = wirResult.scalar_one_or_none()
    return wirInstant