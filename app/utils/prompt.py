import yaml
import os.path as op

from html2text import HTML2Text
from langchain_core.prompts import PromptTemplate

from app.core.config import BASE_DIR


def load_prompt(file):
    # 手动读取你的 YAML 配置文件
    with open(op.join(BASE_DIR, 'app/prompts', file), 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    # 手动构建 PromptTemplate
    return PromptTemplate(
        input_variables=config['input_variables'],
        template=config['template'],
        template_format='jinja2',  # 依然保留你的核心诉求
    )


def html2text(html):
    h = HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    h.ignore_emphasis = True
    return h.handle(html)
