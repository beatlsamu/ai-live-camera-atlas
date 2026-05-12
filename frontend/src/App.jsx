
import React, { useEffect, useMemo, useState } from 'react'
import { ArrowLeft, ArrowRight, Pause, Play } from 'lucide-react'
import { api } from './services/api'
import HeaderBar from './components/HeaderBar'
import ChannelHero from './components/ChannelHero'
import ChannelStrip from './components/ChannelStrip'
import SummaryPanel from './components/SummaryPanel'
import ContextPanel from './components/ContextPanel'
import TimelinePanel from './components/TimelinePanel'
import { useAutoRotate } from './hooks/useAutoRotate'

function formatTimestamp() {
  return new Date().toLocaleString('es-CL', {
    hour: '2-digit',
    minute: '2-digit',
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  })
}

export default function App() {
  const [channels, setChannels] = useState([])
  const [activeIndex, setActiveIndex] = useState(0)
  const [isPlaying, setIsPlaying] = useState(true)
  const [globalSummary, setGlobalSummary] = useState([])
  const [loading, setLoading] = useState(true)
  const [activeObservation, setActiveObservation] = useState(null)

  const activeChannel = channels[activeIndex]

  const currentMetrics = useMemo(() => {
    const obs = activeObservation
    return {
      traffic: obs?.traffic || 'medium',
      pedestrians: obs?.pedestrians || 'medium',
      weather: obs?.weather || 'unknown',
      lighting: obs?.lighting || 'unknown',
      anomalies: obs?.anomalies?.length ? obs.anomalies.join(', ') : 'sin anomalías',
    }
  }, [activeObservation])

  const fetchData = async () => {
    try {
      const [channelsRes, summaryRes, activeRes] = await Promise.all([
        api.channels(),
        api.globalSummary(),
        api.activeChannel(),
      ])

      const items = (channelsRes.items || []).map((c, idx) => ({
        ...c,
        summary: c.summary || `${c.city} · ${c.place}`,
        index: String(idx + 1).padStart(2, '0'),
        imageUrl: c.image_url || c.imageUrl,
      }))

      setChannels(items)

      const activeId = activeRes?.channel?.id || summaryRes?.active_channel?.id
      if (activeId) {
        const idx = items.findIndex((item) => item.id === activeId)
        if (idx >= 0) setActiveIndex(idx)
      }

      setActiveObservation(activeRes?.latest_observation || summaryRes?.active_channel?.latest_observation || null)

      const recents = Object.values(summaryRes.recent_by_channel || {}).flat().slice(-5)
      setGlobalSummary([
        summaryRes.summary?.text || 'Sin resumen global todavía.',
        ...recents.map((o) => `${o.channel_id}: ${o.short_narrative}`),
      ].slice(0, 5))
    } catch (error) {
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
    const timer = setInterval(fetchData, 15000)
    return () => clearInterval(timer)
  }, [])

  useAutoRotate(isPlaying && channels.length > 0, async () => {
    try {
      const res = await api.rotate()
      const activeId = res.active_channel?.id
      const idx = channels.findIndex((c) => c.id === activeId)
      if (idx >= 0) setActiveIndex(idx)
      await fetchData()
    } catch (error) {
      console.error(error)
    }
  }, 30000)

  const handleSelect = async (idx) => {
    if (!channels[idx]) return
    setActiveIndex(idx)
    try {
      const response = await api.observeChannel(channels[idx].id)
      setActiveObservation(response?.observation || null)
      await fetchData()
    } catch (error) {
      console.error(error)
    }
  }

  const narrative = activeObservation?.short_narrative || 'Esperando primera observación.'
  const sourceLabel = activeChannel
    ? `${activeChannel.city}, ${activeChannel.country} · ${activeChannel.place} · ${activeChannel.provider}`
    : 'Cargando canales...'

  const timeline = activeObservation
    ? [
        { title: 'Estado actual', body: activeObservation.short_narrative },
        { title: 'Contexto', body: `${activeChannel?.city || '—'} · ${activeChannel?.place || '—'}` },
      ]
    : [{ title: 'Inicialización', body: 'Cargando canales y resúmenes...' }]

  return (
    <div className="app-shell">
      <div className="bg-grid" />
      <div className="container">
        <HeaderBar
          title="AI Live Camera Atlas"
          subtitle="Observación global por canales con memoria, rotación y narrativa contextual."
          timestamp={formatTimestamp()}
          activeCount={channels.length}
        />

        <div className="toolbar glass">
          <div className="toolbar-left">
            <button className="icon-btn" onClick={() => setActiveIndex((v) => (v - 1 + channels.length) % channels.length)} disabled={!channels.length}>
              <ArrowLeft size={16} />
            </button>
            <button className="toggle-btn" onClick={() => setIsPlaying((v) => !v)} disabled={!channels.length}>
              {isPlaying ? <Pause size={16} /> : <Play size={16} />}
              {isPlaying ? 'Pausar' : 'Reanudar'}
            </button>
            <button className="icon-btn" onClick={() => setActiveIndex((v) => (v + 1) % channels.length)} disabled={!channels.length}>
              <ArrowRight size={16} />
            </button>
          </div>
          <div className="toolbar-right">
            <span className="pill">Rotación: 30s</span>
            <span className="pill">{loading ? 'Sincronizando...' : 'Listo'}</span>
          </div>
        </div>

        <main className="layout">
          <section className="main-col">
            {activeChannel ? (
              <ChannelHero
                channel={{
                  city: activeChannel.city,
                  country: activeChannel.country,
                  place: activeChannel.place,
                  timezone: activeChannel.timezone,
                  imageUrl: activeChannel.image_url || activeChannel.imageUrl,
                  id: activeChannel.id,
                }}
                liveText={narrative}
                metrics={currentMetrics}
                sourceLabel={sourceLabel}
                mode={isPlaying ? 'Automático' : 'Pausado'}
              />
            ) : (
              <div className="glass empty-state">Cargando canales...</div>
            )}

            <ChannelStrip channels={channels.map((c) => ({
              ...c,
              imageUrl: c.image_url || c.imageUrl,
              summary: c.summary,
            }))} activeIndex={activeIndex} onSelect={handleSelect} />
          </section>

          <aside className="side-col">
            <SummaryPanel title="Resumen global" items={globalSummary.length ? globalSummary : ['Sin datos aún.']} />
            <ContextPanel data={{
              city: activeChannel?.city || '—',
              place: activeChannel?.place || '—',
              narrative,
              timezone: activeChannel?.timezone || '—',
            }} />
            <TimelinePanel events={timeline} />
          </aside>
        </main>
      </div>
    </div>
  )
}
