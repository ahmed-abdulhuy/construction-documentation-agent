from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from db.models import WIR, WIRCreate
from db.main import getAsyncDB
import uuid
from sqlmodel import select


wirRouter = APIRouter(prefix="/wir", tags=["wir"])

@wirRouter.get("/")
def wirInit():
    return {"Message": "WIR End Point"}

# get WIR documents
@wirRouter.get("/{wirID}")
async def getWIRByID(wirID: uuid.UUID, session: AsyncSession = Depends(getAsyncDB)):
    wirInstant = await selectWIRByID(wirID, session)
    if not wirInstant:
        return {"message": "WIR Document not found"}
    return wirInstant


# create WIR document
@wirRouter.post("/create")
async def createWIR(wirData: WIRCreate, session: AsyncSession = Depends(getAsyncDB)):
    wir = WIR(**wirData.model_dump())
    # print("type issuingDate:", type(wir.plannedInspDate))
    session.add(wir)
    await session.commit()
    await session.refresh(wir)
    return wir


# update WIR document
@wirRouter.put("/update/{wirID}/")
async def updateWIR(wirID: uuid.UUID, wir: WIR, session: AsyncSession = Depends(getAsyncDB)):
    wirInstant = await selectWIRByID(wirID, session)
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