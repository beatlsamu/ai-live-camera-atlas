import React from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import { CloudRain, MoonStar, SunMedium, Wind, ZoomIn } from 'lucide-react'
import StatusBadge from './StatusBadge'

function Pill({ icon: Icon, label }) {
  return <span className="chip chip-wide"><Icon size={14} /> {label}</span>
}

export default function ChannelHero({ channel, liveText, metrics, sourceLabel, mode }) {
  if (!channel) return null

  return (
    <section className="hero glass">
      <div className="hero-head">
        <div>
          <div className="hero-location">{channel.city}, {channel.country}</div>
          <h2>{channel.place}</h2>
          <div className="hero-sub">{sourceLabel}</div>
        </div>
        <StatusBadge label={mode} tone={mode === 'Automático' ? 'success' : 'muted'} />
      </div>

      <div className="hero-grid">
        <div className="hero-media">
          <AnimatePresence mode="wait">
            <motion.img
              key={channel.id}
              src={channel.imageUrl}
              alt={`${channel.city} - ${channel.place}`}
              className="hero-image"
              initial={{ opacity: 0, scale: 1.02 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.35 }}
            />
          </AnimatePresence>
          <div className="hero-overlay" />
          <div className="hero-live">
            <span className="dot" />
            LIVE SNAPSHOT
          </div>
          <div className="hero-bottom">
            <div className="hero-pills">
              <Pill icon={Wind} label={metrics.traffic} />
              <Pill icon={CloudRain} label={metrics.weather} />
              <Pill icon={SunMedium} label={metrics.lighting} />
              <Pill icon={MoonStar} label={channel.timezone} />
            </div>
            <div className="hero-narrative">{liveText}</div>
          </div>
        </div>

        <div className="hero-side">
          <div className="metric"><span>Tráfico</span><strong>{metrics.traffic}</strong></div>
          <div className="metric"><span>Peatones</span><strong>{metrics.pedestrians}</strong></div>
          <div className="metric"><span>Clima</span><strong>{metrics.weather}</strong></div>
          <div className="metric"><span>Iluminación</span><strong>{metrics.lighting}</strong></div>
          <div className="metric"><span>Anomalías</span><strong>{metrics.anomalies}</strong></div>
          <div className="metric"><span>Captura</span><strong>cada 30s</strong></div>
        </div>
      </div>
    </section>
  )
}
