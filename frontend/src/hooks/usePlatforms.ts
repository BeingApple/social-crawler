import { useEffect, useState } from 'react'
import { fetchPlatforms } from '../api/platforms'
import type { SocialPlatform } from '../api/platforms'

interface UsePlatformsResult {
  platforms:      SocialPlatform[]
  platformLabels: Record<string, string>
  loading:        boolean
}

export function usePlatforms(): UsePlatformsResult {
  const [platforms, setPlatforms] = useState<SocialPlatform[]>([])
  const [loading, setLoading]     = useState(true)

  useEffect(() => {
    fetchPlatforms()
      .then(setPlatforms)
      .finally(() => setLoading(false))
  }, [])

  const platformLabels = Object.fromEntries(
    platforms.map((p) => [p.platformId, p.platformName])
  )

  return { platforms, platformLabels, loading }
}
