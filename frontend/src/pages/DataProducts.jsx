import { useState, useEffect } from 'react'
import {
  PlusIcon,
  EyeIcon,
  PencilSquareIcon,
  TrashIcon,
  XMarkIcon,
  ArrowPathIcon
} from '@heroicons/react/24/outline'
import { bankGenApi } from '../services/api'

export default function DataProducts() {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [modals, setModals] = useState({
    create: false,
    attributes: false,
    design: false,
    validate: false
  })
  const [currentProduct, setCurrentProduct] = useState(null)
  const [modalData, setModalData] = useState({
    attributes: [],
    design: null,
    validation: null
  })
  const [newProduct, setNewProduct] = useState({
    name: '',
    description: '',
    refresh_frequency: 'Daily',
    use_case: ''
  })

  // Fetch data products on mount
  useEffect(() => {
    fetchDataProducts()
  }, [])

  const fetchDataProducts = async () => {
    try {
      setLoading(true)
      const response = await bankGenApi.get('/data-products')
      setProducts(response.data)
    } catch (err) {
      console.error('Fetch error:', err)
      setError(`Failed to load data products: ${err.response?.data?.detail || err.message}`)
    } finally {
      setLoading(false)
    }
  }

  // Product CRUD Operations
  const handleCreateProduct = async (e) => {
    e.preventDefault()
    try {
      setLoading(true)
      const response = await bankGenApi.post('/data-products', {
        ...newProduct,
        use_case: newProduct.use_case || undefined // Only send if exists
      })
      setProducts([...products, response.data])
      closeModal('create')
      resetForm()
    } catch (err) {
      setError(`Creation failed: ${err.response?.data?.detail || err.message}`)
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteProduct = async (id) => {
    if (!confirm('Delete this data product permanently?')) return
    try {
      await bankGenApi.delete(`/data-products/${id}`)
      setProducts(products.filter(p => p.id !== id))
    } catch (err) {
      setError(`Deletion failed: ${err.response?.data?.detail || err.message}`)
    }
  }

  // GenAI Integration Handlers
  const generateDataProductDesign = async (productId) => {
    try {
      setLoading(true)
      const response = await bankGenApi.post(
        `/data-products/${productId}/generate-mappings`
      )
      setModalData({ ...modalData, design: response.data })
      openModal('design')
    } catch (err) {
      setError(`AI generation failed: ${err.response?.data?.detail || err.message}`)
    } finally {
      setLoading(false)
    }
  }

  const validateDataProduct = async (productId) => {
    try {
      setLoading(true)
      const response = await bankGenApi.get(
        `/data-products/${productId}/validate`
      )
      setModalData({ ...modalData, validation: response.data })
      openModal('validate')
    } catch (err) {
      setError(`Validation failed: ${err.response?.data?.detail || err.message}`)
    } finally {
      setLoading(false)
    }
  }

  // Modal Management
  const openModal = (modalName, product = null) => {
    setCurrentProduct(product)
    setModals({ ...modals, [modalName]: true })
  }

  const closeModal = (modalName) => {
    setModals({ ...modals, [modalName]: false })
  }

  const resetForm = () => {
    setNewProduct({
      name: '',
      description: '',
      refresh_frequency: 'Daily',
      use_case: ''
    })
  }

  // Status Badge Component
  const StatusBadge = ({ status }) => (
    <span className={`inline-flex rounded-full px-2.5 py-0.5 text-xs font-medium ${
      status === 'Active' ? 'bg-green-100 text-green-800' :
      status === 'Draft' ? 'bg-yellow-100 text-yellow-800' :
      'bg-gray-100 text-gray-800'
    }`}>
      {status}
    </span>
  )

  return (
    <div className="p-6">
      {/* Header Section */}
      <div className="sm:flex sm:items-center mb-6">
        <div className="sm:flex-auto">
          <h1 className="text-2xl font-bold text-gray-900">BankGen360 Data Products</h1>
          <p className="mt-1 text-sm text-gray-600">
            AI-powered data product management for retail banking
          </p>
        </div>
        <div className="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
          <button
            onClick={() => openModal('create')}
            className="inline-flex items-center gap-x-1.5 rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
          >
            <PlusIcon className="-ml-0.5 h-5 w-5" />
            New Data Product
          </button>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="rounded-md bg-red-50 p-4 mb-6">
          <div className="flex">
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">{error}</h3>
              <button 
                onClick={() => setError(null)}
                className="mt-1 text-sm text-red-700 hover:text-red-600"
              >
                Dismiss
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Loading State */}
      {loading && !error && (
        <div className="flex justify-center py-12">
          <ArrowPathIcon className="h-8 w-8 text-blue-600 animate-spin" />
        </div>
      )}

      {/* Data Products Table */}
      {!loading && (
        <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 rounded-lg">
          <table className="min-w-full divide-y divide-gray-300">
            <thead className="bg-gray-50">
              <tr>
                <th scope="col" className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900">
                  Product Name
                </th>
                <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                  Status
                </th>
                <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                  Last Updated
                </th>
                <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                  Refresh
                </th>
                <th scope="col" className="relative py-3.5 pl-3 pr-4 sm:pr-6">
                  <span className="sr-only">Actions</span>
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 bg-white">
              {products.map((product) => (
                <tr key={product.id}>
                  <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900">
                    {product.name}
                    <p className="text-xs text-gray-500 mt-1 line-clamp-2">
                      {product.description}
                    </p>
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm">
                    <StatusBadge status={product.status} />
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                    {new Date(product.last_updated).toLocaleDateString()}
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                    {product.refresh_frequency}
                  </td>
                  <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                    <div className="flex justify-end space-x-2">
                      <button
                        onClick={() => {
                          setCurrentProduct(product)
                          openModal('attributes')
                        }}
                        className="text-blue-600 hover:text-blue-900"
                        title="View attributes"
                      >
                        <EyeIcon className="h-5 w-5" />
                      </button>
                      <button
                        onClick={() => generateDataProductDesign(product.id)}
                        className="text-green-600 hover:text-green-900"
                        title="Generate design"
                      >
                        <PencilSquareIcon className="h-5 w-5" />
                      </button>
                      <button
                        onClick={() => validateDataProduct(product.id)}
                        className="text-purple-600 hover:text-purple-900"
                        title="Validate"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                      </button>
                      <button
                        onClick={() => handleDeleteProduct(product.id)}
                        className="text-red-600 hover:text-red-900"
                        title="Delete"
                      >
                        <TrashIcon className="h-5 w-5" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Create Product Modal */}
      {modals.create && (
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full">
            <div className="p-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-medium text-gray-900">Create New Data Product</h2>
                <button
                  onClick={() => closeModal('create')}
                  className="text-gray-400 hover:text-gray-500"
                >
                  <XMarkIcon className="h-6 w-6" />
                </button>
              </div>
              
              <form onSubmit={handleCreateProduct} className="space-y-4">
                <div>
                  <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                    Product Name
                  </label>
                  <input
                    type="text"
                    id="name"
                    required
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                    value={newProduct.name}
                    onChange={(e) => setNewProduct({...newProduct, name: e.target.value})}
                  />
                </div>

                <div>
                  <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                    Description
                  </label>
                  <textarea
                    id="description"
                    rows={3}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                    value={newProduct.description}
                    onChange={(e) => setNewProduct({...newProduct, description: e.target.value})}
                  />
                </div>

                <div>
                  <label htmlFor="use_case" className="block text-sm font-medium text-gray-700">
                    Use Case Description (Optional for AI Design)
                  </label>
                  <textarea
                    id="use_case"
                    rows={2}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                    value={newProduct.use_case}
                    onChange={(e) => setNewProduct({...newProduct, use_case: e.target.value})}
                    placeholder="Describe the banking use case for AI-assisted design"
                  />
                </div>

                <div>
                  <label htmlFor="refresh_frequency" className="block text-sm font-medium text-gray-700">
                    Refresh Frequency
                  </label>
                  <select
                    id="refresh_frequency"
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                    value={newProduct.refresh_frequency}
                    onChange={(e) => setNewProduct({...newProduct, refresh_frequency: e.target.value})}
                  >
                    <option value="Real-time">Real-time</option>
                    <option value="Daily">Daily</option>
                    <option value="Weekly">Weekly</option>
                    <option value="Monthly">Monthly</option>
                  </select>
                </div>

                <div className="flex justify-end space-x-3 pt-4">
                  <button
                    type="button"
                    onClick={() => closeModal('create')}
                    className="inline-flex justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={loading}
                    className="inline-flex justify-center rounded-md border border-transparent bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
                  >
                    {loading ? 'Creating...' : 'Create Data Product'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Design Modal */}
      {modals.design && currentProduct && modalData.design && (
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-medium text-gray-900">
                  AI-Generated Design for {currentProduct.name}
                </h2>
                <button
                  onClick={() => closeModal('design')}
                  className="text-gray-400 hover:text-gray-500"
                >
                  <XMarkIcon className="h-6 w-6" />
                </button>
              </div>

              <div className="space-y-6">
                <div>
                  <h3 className="text-md font-medium text-gray-900 mb-2">Recommended Structure</h3>
                  <div className="bg-gray-50 p-4 rounded-md overflow-x-auto">
                    <pre className="text-xs">
                      {JSON.stringify(modalData.design, null, 2)}
                    </pre>
                  </div>
                </div>

                <div className="flex justify-end space-x-3">
                  <button
                    onClick={() => closeModal('design')}
                    className="inline-flex justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    Close
                  </button>
                  <button
                    onClick={() => {
                      // Implement save logic here
                      closeModal('design')
                    }}
                    className="inline-flex justify-center rounded-md border border-transparent bg-green-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500"
                  >
                    Save Design
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}