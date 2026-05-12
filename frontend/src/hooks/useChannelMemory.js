import { useEffect, useState } from 'react'

export function useChannelMemory(activeChannel, summaries = []) {
  const [memory, setMemory] = useState([])

  useEffect(() => {
    if (!activeChannel) return
    const next = [
      activeChannel.summary || `${activeChannel.city} · ${activeChannel.place}`,
      ...summaries.filter(Boolean),
    ]
    setMemory(Array.from(new Set(next)).slice(0, 6))
  }, [activeChannel, summaries])

  return { memory, setMemory }
}
