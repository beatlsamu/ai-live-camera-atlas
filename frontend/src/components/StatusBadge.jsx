import React from 'react'

export default function StatusBadge({ label, tone = 'default' }) {
  return <span className={`status status-${tone}`}>{label}</span>
}
