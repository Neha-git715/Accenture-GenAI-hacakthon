import { useState } from 'react'
import {
  PencilSquareIcon,
  TrashIcon,
  EyeIcon,
} from '@heroicons/react/24/outline'

const products = [
  {
    id: 1,
    name: 'Customer 360 View',
    description: 'Comprehensive view of customer data across all systems',
    status: 'Active',
    lastUpdated: '2 hours ago',
    refreshFrequency: 'Daily',
  },
  {
    id: 2,
    name: 'Transaction History',
    description: 'Detailed transaction records and analytics',
    status: 'Active',
    lastUpdated: '4 hours ago',
    refreshFrequency: 'Real-time',
  },
  {
    id: 3,
    name: 'Account Balance',
    description: 'Current account balances and historical trends',
    status: 'Draft',
    lastUpdated: '1 day ago',
    refreshFrequency: 'Daily',
  },
]

export default function DataProducts() {
  const [selectedProduct, setSelectedProduct] = useState(null)

  const handleView = (product) => {
    setSelectedProduct(product)
  }

  const handleEdit = (product) => {
    // TODO: Implement edit functionality
    console.log('Edit product:', product)
  }

  const handleDelete = (product) => {
    // TODO: Implement delete functionality
    console.log('Delete product:', product)
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-gray-900">Data Products</h1>
        <button className="btn-primary">
          Create New Data Product
        </button>
      </div>

      {/* Products Table */}
      <div className="card">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead>
              <tr>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Name
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Description
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Last Updated
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Refresh Frequency
                </th>
                <th scope="col" className="relative px-6 py-3">
                  <span className="sr-only">Actions</span>
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {products.map((product) => (
                <tr key={product.id}>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">{product.name}</div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="text-sm text-gray-500">{product.description}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                      product.status === 'Active' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {product.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {product.lastUpdated}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {product.refreshFrequency}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <div className="flex items-center space-x-3">
                      <button
                        onClick={() => handleView(product)}
                        className="text-primary-600 hover:text-primary-900"
                      >
                        <EyeIcon className="h-5 w-5" />
                      </button>
                      <button
                        onClick={() => handleEdit(product)}
                        className="text-primary-600 hover:text-primary-900"
                      >
                        <PencilSquareIcon className="h-5 w-5" />
                      </button>
                      <button
                        onClick={() => handleDelete(product)}
                        className="text-red-600 hover:text-red-900"
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
  )
} 