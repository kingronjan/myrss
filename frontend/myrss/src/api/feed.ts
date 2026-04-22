import request from '@/utils/request'

export interface FeedSource {
  id: number
  description: string
  url: string
  updated_at: string
  created_at: string
  deleted: boolean
  sync_status?: number
  sync_msg?: string
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
  return request.get('/feed-source')
}

/**
 * 获取指定订阅源的 feed 列表
 * @param sourceId 订阅源 ID
 * @returns {Promise<FeedItem[]>}
 */
export const getFeeds = (sourceId: number): Promise<FeedItem[]> => {
  return request.get('/feed/', { params: { source_id: sourceId } })
}

/**
 * 更新订阅源信息
 * @param sourceId 订阅源 ID
 * @param data 更新的数据
 */
export const updateFeedSource = (sourceId: number, data: { description: string, url: string }): Promise<any> => {
  return request.put(`/feed-source/${sourceId}`, data)
}

/**
 * 删除订阅源
 * @param sourceId 订阅源 ID
 */
export const deleteFeedSource = (sourceId: number): Promise<any> => {
  return request.delete(`/feed-source/${sourceId}`)
}

/**
 * 同步指定订阅源的 feed
 */
export const syncFeed = (sourceId: number): Promise<any> => {
  return request.post('/feed-source/sync', null, { params: { source_id: sourceId } })
}

/**
 * 获取同步状态
 * @param sourceId 订阅源 ID
 */
export const getSyncStatus = (sourceId: number): Promise<FeedSource> => {
  return request.get('/feed-source/sync-status', { params: { source_id: sourceId } })
}

/**
 * 新增订阅源
 * @param data 订阅源数据
 */
export const addFeedSource = (data: { description: string, url: string }): Promise<FeedSource> => {
  return request.post('/feed-source/add', data)
}
