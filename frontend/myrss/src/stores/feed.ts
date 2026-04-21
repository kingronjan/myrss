import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getFeeds, type FeedItem } from '@/api/feed'

export const useFeedStore = defineStore('feed', () => {
  const feeds = ref<FeedItem[]>([])
  const selectedFeed = ref<FeedItem | null>(null)
  const selectedFeedSourceId = ref<number | null>(null)
  const loading = ref(false)

  const fetchFeeds = async (sourceId: number) => {
    loading.value = true
    selectedFeed.value = null // Reset selection when switching sources
    selectedFeedSourceId.value = sourceId
    try {
      const data = await getFeeds(sourceId)
      feeds.value = Array.isArray(data) ? data : []
    } catch (error) {
      console.error('Failed to fetch feeds:', error)
      feeds.value = []
    } finally {
      loading.value = false
    }
  }

  return {
    feeds,
    selectedFeed,
    selectedFeedSourceId,
    loading,
    fetchFeeds
  }
})
