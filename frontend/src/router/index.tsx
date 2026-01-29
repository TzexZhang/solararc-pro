import { Routes, Route, Navigate } from 'react-router-dom'
import HomePage from '@/pages/HomePage'

const Router = () => {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/analysis" element={<div>日照分析页（开发中）</div>} />
      <Route path="/settings" element={<div>设置页（开发中）</div>} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default Router
