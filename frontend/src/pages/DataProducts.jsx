import { useState, useEffect } from 'react'
import {
  PlusIcon,
  EyeIcon,
  PencilSquareIcon,
  TrashIcon,
} from '@heroicons/react/24/outline'
import { bankGenApi } from '../services/api'

// Mock data while waiting for backend integration
const mockProducts = [
  {
    id: 1,
    name: 'Customer Profile Data',
    description: 'Comprehensive customer information including demographics and preferences',
    status: 'Active',
    last_updated: '2024-01-04T11:24:36',
    refresh_frequency: 'Daily'
  },
  {
    id: 2,
    name: 'Transaction History',
    description: 'Historical record of all customer transactions and account activities',
    status: 'Active',
    last_updated: '2024-01-04T11:24:36',
    refresh_frequency: 'Real-time'
  },
  {
    id: 3,
    name: 'Account Balance Analytics',
    description: 'Analytical insights into account balances and trends',
    status: 'Draft',
    last_updated: '2024-01-04T11:24:36',
    refresh_frequency: 'Hourly'
  }
]

export default function DataProducts() {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showCreateModal, setShowCreateModal] = useState(false)

  useEffect(() => {
    fetchSourceSystems()
  }, [])

  const fetchSourceSystems = async () => {
    try {
      setLoading(true)
      // For now, use mock data
      setProducts(mockProducts)
      // Once backend is ready:
      // const response = await bankGenApi.getSourceSystems()
      // setProducts(response.data)
    } catch (err) {
      console.error('Detailed error:', {
        message: err.message,
        response: err.response?.data,
        status: err.response?.status
      })
      setError(`Failed to fetch source systems: ${err.response?.data?.detail || err.message}`)
    } finally {
      setLoading(false)
    }
  }

  const handleView = async (product) => {
    try {
      const response = await bankGenApi.recommendAttributes()
      console.log('Recommended attributes:', response.data)
      // TODO: Show attributes in a modal
    } catch (err) {
      console.error('Error getting recommendations:', err)
    }
  }

  const handleEdit = async (product) => {
    try {
      const response = await bankGenApi.designDataProduct({
        source_system: product.name,
        // Add other required parameters
      })
      console.log('Design response:', response.data)
      // TODO: Show success message
    } catch (err) {
      console.error('Error designing data product:', err)
    }
  }

  const handleDelete = async (product) => {
    try {
      const response = await bankGenApi.validateDataProduct({
        product_id: product.id,
        // Add other required parameters
      })
      console.log('Validation response:', response.data)
      // TODO: Show validation results
    } catch (err) {
      console.error('Error validating product:', err)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-red-600 text-lg">{error}</div>
        <button 
          onClick={fetchSourceSystems}
          className="mt-4 btn-primary"
        >
          Retry
        </button>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-2xl font-semibold text-gray-900">Data Products</h1>
          <p className="mt-2 text-sm text-gray-700">
            A list of all data products including their name, description, status, and other details.
          </p>
        </div>
        <div className="mt-4 sm:ml-16 sm:mt-0 sm:flex-none">
          <button
            onClick={() => setShowCreateModal(true)}
            className="flex items-center justify-center rounded-md bg-primary-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600"
          >
            <PlusIcon className="h-5 w-5 mr-1.5" />
            Design New Data Product
          </button>
        </div>
      </div>

      <div className="mt-8 flow-root">
        <div className="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
          <div className="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
            <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 sm:rounded-lg">
              <table className="min-w-full divide-y divide-gray-300">
                <thead className="bg-gray-50">
                  <tr>
                    <th scope="col" className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6">
                      Name
                    </th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                      Description
                    </th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                      Status
                    </th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                      Last Updated
                    </th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                      Refresh Frequency
                    </th>
                    <th scope="col" className="relative py-3.5 pl-3 pr-4 sm:pr-6">
                      <span className="sr-only">Actions</span>
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 bg-white">
                  {products.map((product) => (
                    <tr key={product.id}>
                      <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-6">
                        {product.name}
                      </td>
                      <td className="px-3 py-4 text-sm text-gray-500">
                        {product.description}
                      </td>
                      <td className="px-3 py-4 text-sm">
                        <span className={`inline-flex items-center rounded-md px-2 py-1 text-xs font-medium ${
                          product.status === 'Active'
                            ? 'bg-green-50 text-green-700 ring-1 ring-inset ring-green-600/20'
                            : 'bg-yellow-50 text-yellow-700 ring-1 ring-inset ring-yellow-600/20'
                        }`}>
                          {product.status}
                        </span>
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                        {new Date(product.last_updated).toLocaleString()}
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                        {product.refresh_frequency}
                      </td>
                      <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                        <div className="flex justify-end gap-2">
                          <button
                            onClick={() => handleView(product)}
                            className="text-primary-600 hover:text-primary-900"
                            title="View Recommended Attributes"
                          >
                            <EyeIcon className="h-5 w-5" />
                          </button>
                          <button
                            onClick={() => handleEdit(product)}
                            className="text-primary-600 hover:text-primary-900"
                            title="Design Data Product"
                          >
                            <PencilSquareIcon className="h-5 w-5" />
                          </button>
                          <button
                            onClick={() => handleDelete(product)}
                            className="text-red-600 hover:text-red-900"
                            title="Validate Data Product"
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
          </div>
        </div>
      </div>
    </div>
  )
} 