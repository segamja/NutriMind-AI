import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Layout } from './components/Layout'
import { HomePage } from './pages/HomePage'
import { CameraPage } from './pages/CameraPage'
import { ResultPage } from './pages/ResultPage'
import { DashboardPage } from './pages/DashboardPage'
import { HistoryPage } from './pages/HistoryPage'
import { CoachPage } from './pages/CoachPage'
import { WeeklyReportPage } from './pages/WeeklyReportPage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/camera" element={<CameraPage />} />
          <Route path="/result" element={<ResultPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/report" element={<WeeklyReportPage />} />
          <Route path="/history" element={<HistoryPage />} />
          <Route path="/coach" element={<CoachPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
