import React from 'react'

export default function SummaryPanel({ title, items }) {
  return (
    <section className="glass panel">
      <h3>{title}</h3>
      <div className="stack">
        {items.map((item, idx) => (
          <div key={idx} className="summary-item">{item}</div>
        ))}
      </div>
    </section>
  )
}
