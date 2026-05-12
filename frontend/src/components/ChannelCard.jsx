import React from 'react'
import { MapPin } from 'lucide-react'

export default function ChannelCard({ channel, active, onClick }) {
  return (
    <button className={`channel-card ${active ? 'active' : ''}`} onClick={onClick}>
      <div className="channel-card-top">
        <div>
          <div className="channel-city">{channel.city}</div>
          <div className="channel-place"><MapPin size={14} /> {channel.place}</div>
        </div>
        <div className="channel-index">{channel.index}</div>
      </div>
      <div className="channel-summary">{channel.summary}</div>
    </button>
  )
}
