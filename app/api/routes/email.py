from fastapi import BackgroundTasks

from app.api.routes.route import APIRouter
from app.api import response
from app.services.mail import send_feeds

router = APIRouter(
    prefix='/email',
)


@router.post('/send-feeds')
async def send_email(tasks: BackgroundTasks):
    tasks.add_task(send_feeds)
    return response.success(message='Email sent!')
