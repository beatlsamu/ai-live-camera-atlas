import React from 'react'

export default function ContextPanel({ data }) {
  return (
    <section className="glass panel">
      <h3>Contexto de la transmisión</h3>
      <div className="context-grid">
        <div><span>Ciudad</span><strong>{data.city}</strong></div>
        <div><span>Lugar</span><strong>{data.place}</strong></div>
        <div><span>Lectura IA</span><strong>{data.narrative}</strong></div>
        <div><span>Zona horaria</span><strong>{data.timezone}</strong></div>
      </div>
    </section>
  )
}
