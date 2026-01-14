from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from modals.schemas import HumorPhraseCreate, HumorPhraseResponse
from database.connection import get_db
from modals.database_models import HumorPhrase

router = APIRouter(prefix="/humor", tags=["Humor Management"])


@router.post("/phrases", response_model=HumorPhraseResponse, status_code=201)
def add_humor_phrase(phrase: HumorPhraseCreate, db: Session = Depends(get_db)):
    """
    Add a new humor phrase to shape EMO's personality!

    This lets you teach EMO new cute phrases and expressions.

    - **category**: Type of phrase (greeting, goodbye, thanks, excited, confused, error, etc.)
    - **phrase**: The actual cute phrase EMO should use
    - **context**: When EMO should use this phrase
    - **cuteness_level**: How cute is this phrase? (1-10)
    """

    db_phrase = HumorPhrase(
        category=phrase.category,
        phrase=phrase.phrase,
        context=phrase.context,
        cuteness_level=phrase.cuteness_level,
    )

    db.add(db_phrase)
    db.commit()
    db.refresh(db_phrase)

    return db_phrase


@router.get("/phrases", response_model=List[HumorPhraseResponse])
def get_humor_phrases(
    category: Optional[str] = Query(None, description="Filter by category"),
    active_only: bool = Query(True, description="Only show active phrases"),
    limit: int = Query(
        50, ge=1, le=200, description="Maximum number of phrases to return"
    ),
    db: Session = Depends(get_db),
):
    """
    Get all humor phrases, optionally filtered by category.

    Use this to see what phrases EMO knows!
    """

    query = db.query(HumorPhrase)

    if active_only:
        query = query.filter(HumorPhrase.is_active == True)

    if category:
        query = query.filter(HumorPhrase.category == category)

    phrases = query.order_by(HumorPhrase.cuteness_level.desc()).limit(limit).all()

    return phrases


@router.get("/phrases/{phrase_id}", response_model=HumorPhraseResponse)
def get_humor_phrase(phrase_id: int, db: Session = Depends(get_db)):
    """Get a specific humor phrase by ID"""

    phrase = db.query(HumorPhrase).filter(HumorPhrase.id == phrase_id).first()

    if not phrase:
        raise HTTPException(status_code=404, detail="Phrase not found! 🥺")

    return phrase


@router.put("/phrases/{phrase_id}", response_model=HumorPhraseResponse)
def update_humor_phrase(
    phrase_id: int, phrase_update: HumorPhraseCreate, db: Session = Depends(get_db)
):
    """
    Update an existing humor phrase.

    Use this to refine EMO's personality over time!
    """

    phrase = db.query(HumorPhrase).filter(HumorPhrase.id == phrase_id).first()

    if not phrase:
        raise HTTPException(status_code=404, detail="Phrase not found! 🥺")

    phrase.category = phrase_update.category
    phrase.phrase = phrase_update.phrase
    phrase.context = phrase_update.context
    phrase.cuteness_level = phrase_update.cuteness_level

    db.commit()
    db.refresh(phrase)

    return phrase


@router.delete("/phrases/{phrase_id}")
def delete_humor_phrase(
    phrase_id: int,
    hard_delete: bool = Query(
        False, description="Permanently delete instead of deactivating"
    ),
    db: Session = Depends(get_db),
):
    """
    Delete or deactivate a humor phrase.

    By default, phrases are just deactivated (soft delete).
    Set hard_delete=true to permanently remove them.
    """

    phrase = db.query(HumorPhrase).filter(HumorPhrase.id == phrase_id).first()

    if not phrase:
        raise HTTPException(status_code=404, detail="Phrase not found! 🥺")

    if hard_delete:
        db.delete(phrase)
        message = "Phrase permanently deleted! *sad beep*"
    else:
        phrase.is_active = False
        message = "Phrase deactivated! EMO won't use it anymore."

    db.commit()

    return {"message": message, "phrase_id": phrase_id}


@router.get("/categories")
def get_phrase_categories(db: Session = Depends(get_db)):
    """
    Get all available phrase categories.

    Useful for seeing what types of phrases EMO knows!
    """

    categories = (
        db.query(HumorPhrase.category)
        .filter(HumorPhrase.is_active == True)
        .distinct()
        .all()
    )

    category_list = [cat[0] for cat in categories]

    return {"categories": category_list, "count": len(category_list)}


@router.get("/stats")
def get_humor_stats(db: Session = Depends(get_db)):
    """
    Get statistics about EMO's humor database.

    See how many phrases EMO knows and which are most popular!
    """

    total_phrases = db.query(HumorPhrase).count()
    active_phrases = db.query(HumorPhrase).filter(HumorPhrase.is_active == True).count()

    # Get most used phrase
    most_used = db.query(HumorPhrase).order_by(HumorPhrase.usage_count.desc()).first()

    # Get cutest phrase
    cutest = (
        db.query(HumorPhrase)
        .filter(HumorPhrase.is_active == True)
        .order_by(HumorPhrase.cuteness_level.desc())
        .first()
    )

    # Category breakdown
    category_counts = {}
    categories = (
        db.query(HumorPhrase.category)
        .filter(HumorPhrase.is_active == True)
        .distinct()
        .all()
    )

    for cat in categories:
        count = (
            db.query(HumorPhrase)
            .filter(HumorPhrase.category == cat[0], HumorPhrase.is_active == True)
            .count()
        )
        category_counts[cat[0]] = count

    return {
        "total_phrases": total_phrases,
        "active_phrases": active_phrases,
        "inactive_phrases": total_phrases - active_phrases,
        "most_used_phrase": most_used.phrase if most_used else None,
        "most_used_count": most_used.usage_count if most_used else 0,
        "cutest_phrase": cutest.phrase if cutest else None,
        "cutest_level": cutest.cuteness_level if cutest else 0,
        "phrases_by_category": category_counts,
    }
