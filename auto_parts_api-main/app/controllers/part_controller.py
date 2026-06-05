from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.part_service import PartService
from app.schemas.part import PartCreate, PartUpdate, PartPatch, PartResponse, PartsListResponse

router = APIRouter(prefix="/parts", tags=["Auto Parts"])


@router.get("", response_model=PartsListResponse)
async def get_all_parts(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    service = PartService(db)
    parts, meta = await service.get_parts(page, limit)
    return {"data": parts, "meta": meta}


@router.get("/{part_id}", response_model=PartResponse)
async def get_part(part_id: int, db: AsyncSession = Depends(get_db)):
    service = PartService(db)
    part = await service.get_part_by_id(part_id)
    if not part:
        raise HTTPException(status_code=404, detail="Part not found or deleted")
    return part


@router.post("", response_model=PartResponse, status_code=201)
async def create_part(part: PartCreate, db: AsyncSession = Depends(get_db)):
    service = PartService(db)
    try:
        return await service.create_part(part)
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail=f"Part with part_number '{part.part_number}' already exists"
        )


@router.put("/{part_id}", response_model=PartResponse)
async def update_part(part_id: int, part: PartUpdate, db: AsyncSession = Depends(get_db)):
    service = PartService(db)
    try:
        updated = await service.update_part(part_id, part)
        if not updated:
            raise HTTPException(status_code=404, detail="Part not found")
        return updated
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail=f"Part with part_number '{part.part_number}' already exists"
        )


@router.patch("/{part_id}", response_model=PartResponse)
async def patch_part(part_id: int, part: PartPatch, db: AsyncSession = Depends(get_db)):
    service = PartService(db)
    try:
        updated = await service.patch_part(part_id, part)
        if not updated:
            raise HTTPException(status_code=404, detail="Part not found")
        return updated
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail=f"Part with part_number '{part.part_number}' already exists"
        )


@router.delete("/{part_id}", status_code=204)
async def delete_part(part_id: int, db: AsyncSession = Depends(get_db)):
    service = PartService(db)
    success = await service.delete_part(part_id)
    if not success:
        raise HTTPException(status_code=404, detail="Part not found")
    return None
