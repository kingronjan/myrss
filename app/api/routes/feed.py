from app.api.routes.route import APIRouter
from app.db.session import SessionDep
from app.models.feed import Feed

router = APIRouter(
    prefix='/feed',
)


@router.get('/')
async def get_source_feeds(db: SessionDep, source_id: int):
    stmt = db.dialect.select(Feed).where(Feed.source_id == source_id)
    result = await db.scalars(stmt)
    return result.all()
