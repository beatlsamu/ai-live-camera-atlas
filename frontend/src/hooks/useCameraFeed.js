import { useMemo } from 'react'

export function useCameraFeed(channel) {
  return useMemo(() => {
    if (!channel) return null
    return {
      ...channel,
      displayLabel: `${channel.city}, ${channel.country}`,
    }
  }, [channel])
}
