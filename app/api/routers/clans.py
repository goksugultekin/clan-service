from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.db import get_db
from app.models.clan import Clan
from app.schemas.clan import ClanCreate, ClanOut

router = APIRouter(prefix="/clans", tags=["clans"])


# 🟢 1. CREATE — Yeni clan oluştur
@router.post("", response_model=ClanOut)
def create_clan(payload: ClanCreate, db: Session = Depends(get_db)):
    """
    Yeni bir clan oluşturur.
    """
    clan = Clan(
        name=payload.name.strip(),
        region=payload.region.strip().upper(),
        description=payload.description.strip() if payload.description else "",
    )
    db.add(clan)
    db.commit()
    db.refresh(clan)
    return clan


# 🟣 2. LIST — Tüm clan’ları getir (pagination destekli)
@router.get("", response_model=list[ClanOut])
def list_clans(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    """
    Veritabanındaki tüm clan kayıtlarını döndürür.
    """
    return (
        db.query(Clan)
        .order_by(Clan.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


# 🔵 3. SEARCH — İsimle clan ara (min 3 harf, contains)
@router.get("/search", response_model=list[ClanOut])
def search_clans(
    name: str = Query(..., min_length=3, description="Clan name to search (min 3 chars)"),
    db: Session = Depends(get_db),
):
    """
    Clan ismine göre (case-insensitive, partial match) arama yapar.
    """
    results = (
        db.query(Clan)
        .filter(Clan.name.ilike(f"%{name}%"))
        .order_by(Clan.created_at.desc())
        .all()
    )
    return results


# 🔴 4. DELETE — ID’ye göre clan sil
@router.delete("/{clan_id}")
def delete_clan(clan_id: UUID, db: Session = Depends(get_db)):
    """
    Verilen clan_id'ye sahip kaydı siler.
    """
    clan = db.query(Clan).filter(Clan.id == clan_id).first()
    if not clan:
        raise HTTPException(status_code=404, detail="Clan not found")

    db.delete(clan)
    db.commit()
    return {"status": "deleted", "id": str(clan_id)}
