import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import DataProducts from './pages/DataProducts'
import Requirements from './pages/Requirements'
import Validation from './pages/Validation'

// Import CSS
import './index.css'

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to="/data-products" replace />} />
          <Route path="data-products" element={<DataProducts />} />
          <Route path="requirements" element={<Requirements />} />
          <Route path="validation" element={<Validation />} />
        </Route>
      </Routes>
    </Router>
  )
}
