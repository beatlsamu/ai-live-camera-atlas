export function getApiBase() {
  const fromEnv = import.meta.env.VITE_API_BASE_URL?.trim()
  if (fromEnv) return fromEnv.replace(/\/$/, '')
  return ''
}

export function resolveUrl(path) {
  const base = getApiBase()
  return `${base}${path}`
}

export function safeText(value, fallback = 'N/D') {
  if (value === null || value === undefined) return fallback
  const text = String(value).trim()
  return text.length ? text : fallback
}

export function formatLocalTime(isoString, timeZone) {
  try {
    const date = isoString ? new Date(isoString) : new Date()
    return new Intl.DateTimeFormat('es-CL', {
      hour: '2-digit',
      minute: '2-digit',
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      timeZone,
    }).format(date)
  } catch {
    const date = isoString ? new Date(isoString) : new Date()
    return date.toLocaleString('es-CL')
  }
}

export function pickNarrative(observation) {
  if (!observation) return 'Esperando primera observación.'
  if (typeof observation.narrative === 'string' && observation.narrative.trim()) return observation.narrative
  const raw = observation.llm_data || observation.vision_data || {}
  if (typeof raw === 'string') return raw
  return 'La cámara está siendo analizada.'
}

export function speak(text) {
  if (!('speechSynthesis' in window)) return false
  const utterance = new SpeechSynthesisUtterance(text)
  const voices = window.speechSynthesis.getVoices()
  const preferred =
    voices.find((v) => /spanish|es-|español/i.test(v.name + ' ' + v.lang)) ||
    voices.find((v) => /female|woman/i.test(v.name)) ||
    voices[0]
  if (preferred) utterance.voice = preferred
  utterance.lang = preferred?.lang || 'es-CL'
  utterance.rate = 1.0
  utterance.pitch = 1.0
  utterance.volume = 1
  window.speechSynthesis.cancel()
  window.speechSynthesis.speak(utterance)
  return true
}
