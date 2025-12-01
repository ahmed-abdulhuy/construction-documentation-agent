from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.models import Discipline
from app.db.main import getAsyncDB
import uuid
from sqlmodel import select


router = APIRouter(prefix="/discipline", tags=["discipline"])

@router.get("/")
def disciplineInit():
    return {"Message": "Discipline End Point"}

# GET Discipline
@router.get("/{disciplineID}")
async def getDisciplineByID(disciplineID: uuid.UUID, session: AsyncSession = Depends(getAsyncDB)):
    print("Fetch By ID")
    disciplineInstant = await selectDisciplineByID(disciplineID, session)
    if not disciplineInstant:
        return {"message": "Discipline not found"}
    return disciplineInstant


# CREATE Discipline
@router.post("/create")
async def createDiscipline(discipline: Discipline, session: AsyncSession = Depends(getAsyncDB)):
    session.add(discipline)
    await session.commit()
    await session.refresh(discipline)
    return discipline

# UPDATE Discipline
@router.put("/update/{disciplineID}/")
async def updateDiscipline(disciplineID: uuid.UUID, discipline: Discipline, session: AsyncSession = Depends(getAsyncDB)):
    disciplineInstant = await selectDisciplineByID(disciplineID, session)
    if not disciplineInstant:
        return {"message": "Discipline not found"}
    disciplineUpdate = discipline.dict(exclude_unset=True)
    for key, value in disciplineUpdate.items():
        setattr(disciplineInstant, key, value)
    
    await session.commit()
    await session.refresh(disciplineInstant)
    return disciplineInstant


# DELETE Discipline
@router.delete("/delete/{disciplineID}/")
async def deleteDiscipline(disciplineID: uuid.UUID, session: AsyncSession = Depends(getAsyncDB)):
    disciplineInstant = await selectDisciplineByID(disciplineID, session)
    if not disciplineInstant:
        return {"message": "Discipline not found"}
    await session.delete(disciplineInstant)
    await session.commit()
    return {"message": "Discipline deleted successfully"}


async def selectDisciplineByID(disciplineID: uuid.UUID, session: AsyncSession):
    disciplineResult = await session.execute(select(Discipline).where(Discipline.id == disciplineID))
    disciplineInstant = disciplineResult.scalar_one_or_none()
    return disciplineInstant