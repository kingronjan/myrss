import request from '@/utils/request'

export interface FeedSource {
  id: number
  description: string
  url: string
  updated_at: string
  created_at: string
  deleted: boolean
}

/**
 * 获取所有的订阅源列表
 * @returns {Promise<FeedSource[]>}
 */
export const getFeedSources = (): Promise<FeedSource[]> => {
  return request.get('/feed/sources')
}
