import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import DataProducts from './pages/DataProducts'

// Import CSS
import './index.css'

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to="/data-products" replace />} />
          <Route path="data-products" element={<DataProducts />} />
          <Route path="requirements" element={<div className="text-center py-12">Requirements page coming soon...</div>} />
          <Route path="validation" element={<div className="text-center py-12">Validation page coming soon...</div>} />
        </Route>
      </Routes>
    </Router>
  )
}
