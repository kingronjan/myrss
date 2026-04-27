from starlette.background import BackgroundTasks

from app.api import response
from app.api.routes.route import APIRouter
from app.db.session import SessionDep
from app.models.feed import Feed
from app.services.summary import summary_feeds

router = APIRouter(
    prefix='/feed',
)


@router.get('/')
async def get_source_feeds(db: SessionDep, source_id: int):
    stmt = db.dialect.select(Feed).where(Feed.source_id == source_id)
    result = await db.scalars(stmt)
    return result.all()


@router.post('/ai-summary/')
async def ai_summary_feeds(tasks: BackgroundTasks):
    tasks.add_task(summary_feeds)
    return response.success(message='task created')
