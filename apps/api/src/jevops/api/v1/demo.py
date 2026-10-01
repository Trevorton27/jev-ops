from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from jevops.database.seed import seed_demo_data
from jevops.database.session import get_db

router = APIRouter(prefix="/demo", tags=["demo"])


@router.post("/reset")
async def reset_demo(db: AsyncSession = Depends(get_db)):
    """Clear and re-seed demo data."""
    # Delete all data in reverse dependency order
    from jevops.models import (
        Agent,
        APIKey,
        AuditEvent,
        Decision,
        DecisionOutcome,
        Judgment,
        Organization,
        Policy,
        PolicyVersion,
        Project,
        ReplayRun,
        Review,
    )

    from sqlalchemy import delete, update

    # Break circular FK: policies.active_version_id -> policy_versions
    await db.execute(update(Policy).values(active_version_id=None))
    await db.flush()

    for model in [
        AuditEvent,
        DecisionOutcome,
        Judgment,
        Review,
        ReplayRun,
        Decision,
        PolicyVersion,
        Policy,
        Agent,
        APIKey,
        Project,
        Organization,
    ]:
        await db.execute(delete(model))
    await db.commit()

    result = await seed_demo_data(db)
    return {"status": "reset", "api_key": result["api_key"], "details": result}
