## API 数据获取

涉及到数据获取的逻辑，优先查看 docs/api.md 中与需求相关的接口定义，数据返回格式，请求参数等信息。

请求 API 时总是使用 src/utils/request.ts 中的 request 对象。

对于数据的获取逻辑统一放到 src/api 目录下，src/components 下主要存放数据渲染逻辑即可。
