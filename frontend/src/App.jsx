import React, { useEffect, useMemo, useRef, useState } from 'react'
import { Activity, ArrowLeft, ArrowRight, Globe2, MapPin, Mic, Pause, Play, RefreshCw, Sparkles, SunMedium, Volume2, Waves, WifiOff } from 'lucide-react'
import { demoChannels } from './data'
import { formatLocalTime, pickNarrative, resolveUrl, safeText, speak } from './lib'

const rotationSeconds = Number(import.meta.env.VITE_ROTATION_SECONDS || 30)

const badgeColors = {
  traffic: 'chip-chip-blue',
  city: 'chip-chip-violet',
  airport: 'chip-chip-cyan',
  coast: 'chip-chip-teal',
  weather: 'chip-chip-amber',
}

function cx(...classes) {
  return classes.filter(Boolean).join(' ')
}

function Pill({ children, tone = 'default' }) {
  return <span className={cx('pill', tone === 'accent' && 'pill-accent')}>{children}</span>
}

function MetricCard({ label, value, hint }) {
  return (
    <div className="metric-card">
      <div className="metric-label">{label}</div>
      <div className="metric-value">{value}</div>
      {hint ? <div className="metric-hint">{hint}</div> : null}
    </div>
  )
}

function ChannelCard({ channel, active, onClick }) {
  return (
    <button className={cx('channel-card', active && 'channel-card-active')} onClick={onClick}>
      <div className="channel-card-top">
        <div>
          <div className="channel-card-city">{channel.city}</div>
          <div className="channel-card-place">{channel.place}</div>
        </div>
        <span className={cx('type-badge', badgeColors[channel.type] || 'chip-chip-blue')}>{channel.type}</span>
      </div>
      <div className="channel-card-sub">{channel.country} · {channel.timezone}</div>
    </button>
  )
}

export default function App() {
  const [channels, setChannels] = useState([])
  const [active, setActive] = useState(null)
  const [globalSummary, setGlobalSummary] = useState('Cargando resumen global...')
  const [loading, setLoading] = useState(true)
  const [autoRotate, setAutoRotate] = useState(true)
  const [voiceOn, setVoiceOn] = useState(true)
  const [liveClock, setLiveClock] = useState(new Date().toLocaleString('es-CL'))
  const [lastError, setLastError] = useState('')
  const [lastSpoken, setLastSpoken] = useState('')
  const intervalRef = useRef(null)
  const clockRef = useRef(null)

  const currentChannel = active?.channel || channels[0] || demoChannels[0]
  const currentObservation = active?.latest_observation || null
  const narrative = pickNarrative(currentObservation)
  const localTime = formatLocalTime(currentObservation?.timestamp, currentChannel?.timezone || 'UTC')
  const imageUrl = currentChannel?.image_url || demoChannels[0].image_url

  const apiBase = useMemo(() => {
    const env = import.meta.env.VITE_API_BASE_URL?.trim()
    return env ? env.replace(/\/$/, '') : ''
  }, [])

  const api = (path, options = {}) => resolveUrl(path, apiBase)

  async function loadData() {
    setLastError('')
    try {
      const [channelsRes, activeRes, summaryRes] = await Promise.all([
        fetch(api('/api/channels')),
        fetch(api('/api/channels/active')),
        fetch(api('/api/summary/global')).catch(() => null),
      ])

      if (!channelsRes.ok) throw new Error(`channels ${channelsRes.status}`)
      const channelsJson = await channelsRes.json()
      setChannels(channelsJson.items || [])

      if (activeRes.ok) {
        const activeJson = await activeRes.json()
        setActive(activeJson)
      }

      if (summaryRes && summaryRes.ok) {
        const summaryJson = await summaryRes.json()
        const text = summaryJson?.summary?.text || summaryJson?.summary || ''
        if (text) setGlobalSummary(text)
      }

      setLoading(false)
    } catch (err) {
      setLastError('Backend no disponible; usando demo local.')
      setChannels(demoChannels)
      setActive({
        channel: demoChannels[0],
        latest_observation: {
          timestamp: new Date().toISOString(),
          narrative:
            'Tokyo presenta un flujo peatonal alto bajo iluminación nocturna. La escena mantiene energía urbana intensa y estable.',
        },
      })
      setGlobalSummary('Demostración local activa. Conecta el backend para mostrar observaciones reales.')
      setLoading(false)
    }
  }

  async function rotateNow() {
    try {
      const res = await fetch(api('/api/rotate'), { method: 'POST' })
      if (!res.ok) throw new Error(`rotate ${res.status}`)
      await loadData()
    } catch {
      const nextIndex = (channels.findIndex((c) => c.id === currentChannel?.id) + 1) % (channels.length || demoChannels.length)
      const fallbackChannel = (channels.length ? channels : demoChannels)[nextIndex]
      setActive({
        channel: fallbackChannel,
        latest_observation: {
          timestamp: new Date().toISOString(),
          narrative: `Demostración activa en ${fallbackChannel.city}.`,
        },
      })
    }
  }

  useEffect(() => { loadData() }, [])

  useEffect(() => {
    clockRef.current = setInterval(() => setLiveClock(new Date().toLocaleString('es-CL')), 1000)
    return () => clearInterval(clockRef.current)
  }, [])

  useEffect(() => {
    if (!autoRotate) {
      if (intervalRef.current) clearInterval(intervalRef.current)
      return
    }
    intervalRef.current = setInterval(() => {
      rotateNow()
    }, rotationSeconds * 1000)
    return () => clearInterval(intervalRef.current)
  }, [autoRotate, channels, currentChannel?.id])

  useEffect(() => {
    if (!voiceOn) return
    if (!narrative || narrative === lastSpoken) return
    const text = narrative.replace(/\*\*/g, '').slice(0, 600)
    if (text.length < 6) return
    const timer = setTimeout(() => {
      if (speak(text)) setLastSpoken(narrative)
    }, 250)
    return () => clearTimeout(timer)
  }, [narrative, voiceOn])

  const metrics = useMemo(() => {
    const c = currentChannel || demoChannels[0]
    const obs = currentObservation || {}
    return [
      { label: 'Ciudad', value: safeText(c.city), hint: c.country },
      { label: 'Lugar', value: safeText(c.place), hint: safeText(c.provider) },
      { label: 'Hora local', value: localTime, hint: safeText(c.timezone) },
      { label: 'Narración', value: voiceOn ? 'Voz activa' : 'Voz pausada', hint: 'Speech Synthesis' },
      { label: 'Estado', value: loading ? 'Cargando' : 'En línea', hint: lastError || 'Conectado al atlas' },
      { label: 'Actualización', value: `${rotationSeconds}s`, hint: 'Auto-rotación' },
    ]
  }, [currentChannel, currentObservation, localTime, voiceOn, loading, lastError])

  return (
    <div className="app-shell">
      <div className="bg-orb orb-a" />
      <div className="bg-orb orb-b" />
      <div className="bg-orb orb-c" />

      <header className="topbar">
        <div>
          <div className="brand-row">
            <span className="brand-dot" />
            <span className="brand-kicker">AI Live Camera Atlas</span>
          </div>
          <h1 className="hero-title">Observación visual global con narrativa IA</h1>
          <p className="hero-subtitle">
            Cámaras en vivo, contexto urbano, memoria temporal y voz automática en una sola interfaz.
          </p>
        </div>

        <div className="topbar-controls">
          <button className="control-btn" onClick={() => setAutoRotate((v) => !v)}>
            {autoRotate ? <Pause size={16} /> : <Play size={16} />}
            {autoRotate ? 'Pausar' : 'Reanudar'}
          </button>
          <button className="control-btn" onClick={() => setVoiceOn((v) => !v)}>
            <Volume2 size={16} />
            {voiceOn ? 'Voz ON' : 'Voz OFF'}
          </button>
          <button className="control-btn accent" onClick={rotateNow}>
            <RefreshCw size={16} />
            Cambiar cámara
          </button>
        </div>
      </header>

      <main className="layout">
        <section className="camera-stage">
          <div className="camera-frame">
            <div className="camera-image-wrap">
              <img
                className="camera-image"
                src={imageUrl}
                alt={`${currentChannel?.city || 'Camera'} live view`}
                onError={(e) => {
                  e.currentTarget.src = demoChannels[0].image_url
                }}
              />
              <div className="camera-overlay" />
              <div className="live-pill">
                <span className="live-dot" />
                LIVE OBSERVATION
              </div>

              <div className="camera-copy">
                <div className="location-row">
                  <MapPin size={16} />
                  <span>{safeText(currentChannel?.city)} · {safeText(currentChannel?.country)}</span>
                  <span className="sep">•</span>
                  <span>{safeText(currentChannel?.timezone)}</span>
                </div>
                <h2>{safeText(currentChannel?.place)}</h2>
                <p>{narrative}</p>
              </div>
            </div>

            <div className="camera-footer">
              <div className="footer-left">
                <Pill tone="accent"><Sparkles size={14} /> {safeText(currentChannel?.type).toUpperCase()}</Pill>
                <Pill><SunMedium size={14} /> {safeText(currentChannel?.provider)}</Pill>
                <Pill><Activity size={14} /> {safeText(localTime)}</Pill>
              </div>
              <div className="footer-right">
                <button className="mini-btn" onClick={() => setVoiceOn(true)}><Mic size={14} /> Narrar</button>
                <button className="mini-btn" onClick={loadData}><RefreshCw size={14} /> Actualizar</button>
                <button className="mini-btn" onClick={() => window.speechSynthesis?.cancel?.()}><Volume2 size={14} /> Silencio</button>
              </div>
            </div>
          </div>
        </section>

        <aside className="side-panel">
          <section className="panel-card summary-card">
            <div className="panel-header">
              <div>
                <div className="panel-kicker">Memoria global</div>
                <h3>Resumen acumulado</h3>
              </div>
              <Globe2 size={18} />
            </div>
            <div className="summary-text">{globalSummary}</div>
            <div className="summary-meta">
              <span>{channels.length || demoChannels.length} canales</span>
              <span>Última actualización · {liveClock}</span>
            </div>
          </section>

          <section className="panel-card metrics-grid">
            {metrics.map((m) => (
              <MetricCard key={m.label} {...m} />
            ))}
          </section>

          <section className="panel-card channels-card">
            <div className="panel-header">
              <div>
                <div className="panel-kicker">Canales</div>
                <h3>Fuentes activas</h3>
              </div>
              {lastError ? <WifiOff size={18} /> : <Activity size={18} />}
            </div>

            <div className="channels-list">
              {(channels.length ? channels : demoChannels).map((ch) => (
                <ChannelCard
                  key={ch.id}
                  channel={ch}
                  active={ch.id === currentChannel?.id}
                  onClick={() => setActive({ channel: ch, latest_observation: currentObservation })}
                />
              ))}
            </div>
          </section>
        </aside>
      </main>
    </div>
  )
}
