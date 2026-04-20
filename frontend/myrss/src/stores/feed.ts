import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getFeeds, type FeedItem } from '@/api/feed'

export const useFeedStore = defineStore('feed', () => {
  const feeds = ref<FeedItem[]>([])
  const loading = ref(false)

  const fetchFeeds = async (sourceId: number) => {
    loading.value = true
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
    loading,
    fetchFeeds
  }
})
