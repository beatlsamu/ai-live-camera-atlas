import React from 'react'
import { CalendarDays, Globe2 } from 'lucide-react'

export default function HeaderBar({ title, subtitle, timestamp, activeCount }) {
  return (
    <header className="glass header">
      <div>
        <div className="chips">
          <span className="chip"><Globe2 size={14} /> Global live observer</span>
          <span className="chip"><CalendarDays size={14} /> {timestamp}</span>
        </div>
        <h1>{title}</h1>
        <p>{subtitle}</p>
      </div>
      <div className="header-meta">
        <span className="pill">{activeCount} canales</span>
      </div>
    </header>
  )
}
