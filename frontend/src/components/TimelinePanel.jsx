import React from 'react'

export default function TimelinePanel({ events }) {
  return (
    <section className="glass panel">
      <h3>Línea de observación</h3>
      <div className="stack">
        {events.map((event, idx) => (
          <div key={idx} className="timeline-item">
            <strong>{event.title}</strong>
            <p>{event.body}</p>
          </div>
        ))}
      </div>
    </section>
  )
}
