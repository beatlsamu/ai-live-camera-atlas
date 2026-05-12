const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  })
  if (!response.ok) {
    const text = await response.text()
    throw new Error(text || `Request failed: ${response.status}`)
  }
  return response.json()
}

export const api = {
  health: () => request('/api/health'),
  channels: () => request('/api/channels'),
  activeChannel: () => request('/api/channels/active'),
  rotate: () => request('/api/rotate', { method: 'POST' }),
  reseed: () => request('/api/reseed', { method: 'POST' }),
  globalSummary: () => request('/api/summary/global'),
  channelSummary: (id) => request(`/api/channels/${id}/summary`),
  observeChannel: (id) => request(`/api/channels/${id}/observe`, { method: 'POST' }),
}
