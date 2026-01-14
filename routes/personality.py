from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from modals.schemas import PersonalityInstructionCreate, PersonalityInstructionResponse
from database.connection import get_db
from modals.database_models import PersonalityInstruction

router = APIRouter(prefix="/personality", tags=["Personality Management"])


@router.post(
    "/instructions", response_model=PersonalityInstructionResponse, status_code=201
)
def add_personality_instruction(
    instruction: PersonalityInstructionCreate, db: Session = Depends(get_db)
):
    """
    Add a new personality instruction to shape how EMO behaves!

    This is powerful - it directly influences EMO's core personality.

    - **instruction_type**: Type of instruction (tone, expression, emotion, etc.)
    - **instruction_text**: The actual instruction
    - **priority**: How important this is (1-10, higher = more important)
    - **weight**: How strongly to apply this (0.1-2.0)
    """

    db_instruction = PersonalityInstruction(
        instruction_type=instruction.instruction_type,
        instruction_text=instruction.instruction_text,
        priority=instruction.priority,
        weight=instruction.weight,
    )

    db.add(db_instruction)
    db.commit()
    db.refresh(db_instruction)

    return db_instruction


@router.get("/instructions", response_model=List[PersonalityInstructionResponse])
def get_personality_instructions(
    instruction_type: Optional[str] = Query(
        None, description="Filter by instruction type"
    ),
    active_only: bool = Query(True, description="Only show active instructions"),
    db: Session = Depends(get_db),
):
    """
    Get all personality instructions that shape EMO's behavior.

    See exactly what makes EMO... EMO! 🤖💕
    """

    query = db.query(PersonalityInstruction)

    if active_only:
        query = query.filter(PersonalityInstruction.is_active == True)

    if instruction_type:
        query = query.filter(
            PersonalityInstruction.instruction_type == instruction_type
        )

    instructions = query.order_by(PersonalityInstruction.priority.desc()).all()

    return instructions


@router.get(
    "/instructions/{instruction_id}", response_model=PersonalityInstructionResponse
)
def get_personality_instruction(instruction_id: int, db: Session = Depends(get_db)):
    """Get a specific personality instruction by ID"""

    instruction = (
        db.query(PersonalityInstruction)
        .filter(PersonalityInstruction.id == instruction_id)
        .first()
    )

    if not instruction:
        raise HTTPException(status_code=404, detail="Instruction not found! 🥺")

    return instruction


@router.put(
    "/instructions/{instruction_id}", response_model=PersonalityInstructionResponse
)
def update_personality_instruction(
    instruction_id: int,
    instruction_update: PersonalityInstructionCreate,
    db: Session = Depends(get_db),
):
    """
    Update a personality instruction.

    Fine-tune EMO's personality by adjusting instructions!
    """

    instruction = (
        db.query(PersonalityInstruction)
        .filter(PersonalityInstruction.id == instruction_id)
        .first()
    )

    if not instruction:
        raise HTTPException(status_code=404, detail="Instruction not found! 🥺")

    instruction.instruction_type = instruction_update.instruction_type
    instruction.instruction_text = instruction_update.instruction_text
    instruction.priority = instruction_update.priority
    instruction.weight = instruction_update.weight

    db.commit()
    db.refresh(instruction)

    return instruction


@router.delete("/instructions/{instruction_id}")
def delete_personality_instruction(
    instruction_id: int,
    hard_delete: bool = Query(
        False, description="Permanently delete instead of deactivating"
    ),
    db: Session = Depends(get_db),
):
    """
    Delete or deactivate a personality instruction.

    Be careful - this changes EMO's core behavior!
    """

    instruction = (
        db.query(PersonalityInstruction)
        .filter(PersonalityInstruction.id == instruction_id)
        .first()
    )

    if not instruction:
        raise HTTPException(status_code=404, detail="Instruction not found! 🥺")

    if hard_delete:
        db.delete(instruction)
        message = "Instruction permanently deleted!"
    else:
        instruction.is_active = False
        message = "Instruction deactivated! EMO's behavior may change."

    db.commit()

    return {"message": message, "instruction_id": instruction_id}


@router.get("/types")
def get_instruction_types(db: Session = Depends(get_db)):
    """
    Get all personality instruction types.

    See what aspects of EMO's personality you can control!
    """

    types = (
        db.query(PersonalityInstruction.instruction_type)
        .filter(PersonalityInstruction.is_active == True)
        .distinct()
        .all()
    )

    type_list = [t[0] for t in types]

    return {"instruction_types": type_list, "count": len(type_list)}
