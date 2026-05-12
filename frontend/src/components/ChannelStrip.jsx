import React from 'react'
import ChannelCard from './ChannelCard'

export default function ChannelStrip({ channels, activeIndex, onSelect }) {
  return (
    <div className="channel-strip">
      {channels.map((channel, idx) => (
        <ChannelCard
          key={channel.id}
          channel={{ ...channel, index: String(idx + 1).padStart(2, '0') }}
          active={idx === activeIndex}
          onClick={() => onSelect(idx)}
        />
      ))}
    </div>
  )
}
