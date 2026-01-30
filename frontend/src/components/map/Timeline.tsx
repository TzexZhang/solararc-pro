import React, { useEffect, useState } from 'react'
import { Slider, Button, Space, DatePicker, Switch, Select } from 'antd'
import {
  PlayCircleOutlined,
  PauseCircleOutlined,
  FastForwardOutlined,
  SunOutlined,
  MoonOutlined
} from '@ant-design/icons'
import { useMapStore } from '@/store'
import dayjs from 'dayjs'
import './Timeline.css'

export const Timeline: React.FC = () => {
  const {
    currentHour,
    isPlaying,
    playbackSpeed,
    currentDate,
    setCurrentHour,
    setIsPlaying,
    setPlaybackSpeed,
    setCurrentDate
  } = useMapStore()

  const [localDate, setLocalDate] = useState(dayjs(currentDate))

  useEffect(() => {
    let interval: NodeJS.Timeout | null = null

    if (isPlaying) {
      interval = setInterval(() => {
        setCurrentHour((currentHour + 1) % 24)
      }, 1000 / playbackSpeed)
    }

    return () => {
      if (interval) clearInterval(interval)
    }
  }, [isPlaying, currentHour, playbackSpeed, setCurrentHour])

  const handleDateChange = (date: any) => {
    if (date) {
      const newDate = date.format('YYYY-MM-DD')
      setLocalDate(date)
      setCurrentDate(newDate)
    }
  }

  const handleSpeedChange = (speed: number) => {
    setPlaybackSpeed(speed)
  }

  const speedOptions = [
    { label: '1x', value: 1 },
    { label: '2x', value: 2 },
    { label: '5x', value: 5 },
    { label: '10x', value: 10 }
  ]

  const formatHour = (hour: number) => {
    return `${String(hour).padStart(2, '0')}:00`
  }

  const timeMarks = {
    0: '00:00',
    6: '06:00',
    12: '12:00',
    18: '18:00',
    23: '23:00'
  }

  const isNight = currentHour < 6 || currentHour > 18

  return (
    <div className="timeline-container">
      <div className="timeline-header">
        <Space>
          <DatePicker
            value={localDate}
            onChange={handleDateChange}
            format="YYYY-MM-DD"
            allowClear={false}
          />
          <Select
            value={playbackSpeed}
            onChange={handleSpeedChange}
            options={speedOptions}
            style={{ width: 80 }}
          />
        </Space>
        <Button
          type="primary"
          icon={isPlaying ? <PauseCircleOutlined /> : <PlayCircleOutlined />}
          onClick={() => setIsPlaying(!isPlaying)}
        >
          {isPlaying ? '暂停' : '播放'}
        </Button>
      </div>

      <div className="timeline-slider">
        <div className="time-display">
          {isNight ? <MoonOutlined /> : <SunOutlined />}
          <span className="current-time">{formatHour(currentHour)}</span>
        </div>
        <Slider
          min={0}
          max={23}
          value={currentHour}
          onChange={setCurrentHour}
          marks={timeMarks}
          tooltip={{ formatter: formatHour }}
          className="hour-slider"
        />
      </div>
    </div>
  )
}

export default Timeline
