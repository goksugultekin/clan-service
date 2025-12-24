from sqlalchemy.orm import Session
from app.models.clan import Clan
from app.schemas.clan import ClanCreate


def create_clan(db: Session, payload: ClanCreate) -> Clan:
    
    c = Clan(
        name=payload.name.strip(),
        description=payload.description.strip(),
        region=payload.region
    )
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


def list_clans(db: Session, limit: int = 100, offset: int = 0):
   
    return (
        db.query(Clan)
        .order_by(Clan.created_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )


def search_clans(db: Session, name: str):
   
    if len(name.strip()) < 3:
        raise ValueError("name en az 3 harf olmalı")
    pattern = f"%{name.strip()}%"
    return (
        db.query(Clan)
        .filter(Clan.name.ilike(pattern))
        .order_by(Clan.created_at.desc())
        .all()
    )


def delete_clan(db: Session, clan_id: str) -> bool:
   
    obj = db.get(Clan, clan_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
