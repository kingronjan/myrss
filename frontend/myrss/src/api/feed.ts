import request from '@/utils/request'

export interface FeedSource {
  id: number
  description: string
  url: string
  updated_at: string
  created_at: string
  deleted: boolean
}

export interface FeedItem {
  id: string
  title: string
  summary: string
  published: string
  link: string
  source_id: number
  is_read: boolean
  updated_at: string
  created_at: string
  deleted: boolean
  is_sent: boolean
}

/**
 * 获取所有的订阅源列表
 * @returns {Promise<FeedSource[]>}
 */
export const getFeedSources = (): Promise<FeedSource[]> => {
  return request.get('/feed/sources')
}

/**
 * 获取指定订阅源的 feed 列表
 * @param sourceId 订阅源 ID
 * @returns {Promise<FeedItem[]>}
 */
export const getFeeds = (sourceId: number): Promise<FeedItem[]> => {
  return request.get('/feed/', { params: { source_id: sourceId } })
}
