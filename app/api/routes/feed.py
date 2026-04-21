from app.api.routes.route import APIRouter
from app.db.session import SessionDep
from app.models.feed import Feed

router = APIRouter(
    prefix='/feed',
)


@router.get('/')
async def get_source_feeds(db: SessionDep, source_id: int):
    stmt = Feed.stmt().select().where(Feed.source_id == source_id)
    result = await db.execute(stmt)
    return result.scalars().all()
