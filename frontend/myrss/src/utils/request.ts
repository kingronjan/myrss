import axios from 'axios'
import type { AxiosInstance, AxiosResponse, InternalAxiosRequestConfig } from 'axios'
import { ElMessage } from 'element-plus'

// 从环境变量读取，Vite 默认使用 import.meta.env
// 优先级：VITE_API_BASE_URL > http://127.0.0.1:8000
const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

const request: AxiosInstance = axios.create({
  baseURL,
  timeout: 10000,
  headers: {
    'Accept': 'application/json',
  },
})

// 请求拦截器
request.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // 可以在这里添加 token 等逻辑
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

// 响应拦截器
request.interceptors.response.use(
  (response: AxiosResponse) => {
    // 假设后端返回的数据结构中有一个 code 或 status 来判断业务成功
    // 这里可以根据实际业务进行调整
    return response.data
  },
  (error) => {
    // 统一处理错误
    const message = error.response?.data?.message || error.message || '请求失败'
    ElMessage.error(message)
    return Promise.reject(error)
  },
)

export default request
