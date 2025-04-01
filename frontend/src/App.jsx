import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import DataProducts from './pages/DataProducts'
import Requirements from './pages/Requirements'
import Validation from './pages/Validation'

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/data-products" element={<DataProducts />} />
          <Route path="/requirements" element={<Requirements />} />
          <Route path="/validation" element={<Validation />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App
