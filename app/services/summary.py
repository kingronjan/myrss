import logging

from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import settings
from app.db.session import create_session
from app.models.feed import Feed
from app.utils.prompt import load_prompt, html2text

logger = logging.getLogger(__name__)


async def summary_feeds():
    async with create_session() as db:
        feeds = await load_feeds(db)
        for feed in feeds:
            logger.debug('Generating summary for feed %s', feed)
            params = await _summary_chunks(feed)
            ai_summary = await summary_by_text(params)
            logger.debug(f'Got AI summary for {feed.title}: {ai_summary}')
            await db.set_values(feed, ai_summary=ai_summary)


async def load_feeds(db):
    stmt = db.dialect.select(Feed).where(Feed.summary.is_(None))
    return await db.scalars(stmt)


async def _summary_chunks(feed):
    # 1. 初始化本地模型 (假设你已通过 ollama run qwen2.5:7b 启动)
    llm = init_chat_model('ollama:qwen2.5:7b')

    # 2. 从外部 YAML 加载 Prompt (已配置为 jinja2 模式)
    # 此时 content 中的 { code_block } 不会被 LangChain 误解析
    prompt = load_prompt('summary-chunk.yml')

    # 3. 使用 LCEL (LangChain Expression Language) 构建处理链
    chain = prompt | llm | StrOutputParser()

    text = html2text(feed.summary)
    chunks = split_rss_article(text)

    if len(chunks) > 1:
        prev_summary = None
        results = []

        for chunk in chunks:
            chunk['prev_summary'] = prev_summary
            chunk['title'] = feed.title
            response = await chain.ainvoke(chunk)
            logger.debug(
                f'digest for {feed.title} chunk {chunk["current"]}/{chunk["total"]}: {response}'
            )
            prev_summary = response
            results.append(response)

        content = '\n'.join(results)
    else:
        logger.debug(f'{feed.title} no chunks')
        content = text

    return {
        'title': feed.title,
        'content': content,
    }


async def summary_by_text(params):
    # 1. 初始化本地模型 (假设你已通过 ollama run qwen2.5:7b 启动)
    llm = init_chat_model(settings.MODEL)

    # 2. 从外部 YAML 加载 Prompt (已配置为 jinja2 模式)
    # 此时 content 中的 { code_block } 不会被 LangChain 误解析
    prompt = load_prompt('summary.yml')

    # 3. 使用 LCEL (LangChain Expression Language) 构建处理链
    chain = prompt | llm | StrOutputParser()

    # 流式输出
    return await chain.ainvoke(params)


def split_rss_article(
    md_text,
    chunk_size=settings.TEXT_CHUNK_SIZE,
    chunk_overlap=settings.TEXT_CHUNK_OVERLAP,
):
    # 1. 初始化切分器
    # 对于 html2text 后的 Markdown，这些分隔符能很好地保留结构
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=['\n\n', '\n', '。', '！', '？', ' ', ''],
    )

    # 2. 执行切分
    chunks = splitter.split_text(md_text)
    total_len = len(md_text)
    total_chunks = len(chunks)

    processed_chunks = []
    current_pos = 0

    for i, content in enumerate(chunks):
        # 3. 计算百分比范围
        # 注意：由于有 Overlap，计算百分比时用当前块在原文中的起始位置更准
        start_idx = md_text.find(content[:50], max(0, current_pos - chunk_overlap))
        end_idx = start_idx + len(content)

        start_pct = round((start_idx / total_len) * 100)
        end_pct = round((end_idx / total_len) * 100)

        # 更新位置指针（为下一次找索引做准备）
        current_pos = end_idx

        processed_chunks.append(
            {
                'current': i + 1,
                'total': total_chunks,
                'start_pct': start_pct,
                'end_pct': min(end_pct, 100),
                'text': content,
            }
        )

    return processed_chunks
