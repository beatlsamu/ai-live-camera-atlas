import { useEffect } from 'react'

export function useAutoRotate(isPlaying, onTick, delay = 30000) {
  useEffect(() => {
    if (!isPlaying) return
    const id = setInterval(onTick, delay)
    return () => clearInterval(id)
  }, [isPlaying, onTick, delay])
}
