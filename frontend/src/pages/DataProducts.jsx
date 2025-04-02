import { useState, useEffect } from 'react'
import {
  PlusIcon,
  EyeIcon,
  PencilSquareIcon,
  TrashIcon,
  XMarkIcon,
} from '@heroicons/react/24/outline'
import { bankGenApi } from '../services/api.js'

export default function DataProducts() {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [showAttributesModal, setShowAttributesModal] = useState(false)
  const [showDesignModal, setShowDesignModal] = useState(false)
  const [showValidationModal, setShowValidationModal] = useState(false)
  const [currentProduct, setCurrentProduct] = useState(null)
  const [attributes, setAttributes] = useState([])
  const [designResult, setDesignResult] = useState(null)
  const [validationResult, setValidationResult] = useState(null)
  const [newProductData, setNewProductData] = useState({
    name: '',
    description: '',
    refresh_frequency: 'Daily',
    use_case_description: ''
  })

  useEffect(() => {
    fetchDataProducts()
  }, [])

  const fetchDataProducts = async () => {
    try {
      setLoading(true)
      const response = await bankGenApi.getDataProducts()
      setProducts(response.data)
    } catch (err) {
      console.error('Detailed error:', {
        message: err.message,
        response: err.response?.data,
        status: err.response?.status
      })
      setError(`Failed to fetch data products: ${err.response?.data?.detail || err.message}`)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateProduct = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      setError(null);
      
      // Create the data product
      const response = await bankGenApi.createDataProduct({
        name: newProductData.name,
        description: newProductData.description,
        refresh_frequency: newProductData.refresh_frequency,
        status: 'Draft'
      });
      
      // Refresh the list and close modal
      await fetchDataProducts();
      setShowCreateModal(false);
      
      // Reset form
      setNewProductData({
        name: '',
        description: '',
        refresh_frequency: 'Daily',
        use_case_description: ''
      });
    } catch (err) {
      console.error('Error creating product:', err);
      setError(`Failed to create data product: ${err.response?.data?.detail || err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleView = async (product) => {
    try {
      setCurrentProduct(product)
      const response = await bankGenApi.recommendAttributes({ use_case: product.name })
      setAttributes(response.data)
      setShowAttributesModal(true)
    } catch (err) {
      console.error('Error getting recommendations:', err)
      setError(`Failed to get recommended attributes: ${err.response?.data?.detail || err.message}`)
    }
  }

  const handleEdit = async (product) => {
    try {
      setCurrentProduct(product)
      const response = await bankGenApi.designDataProduct({
        use_case_description: `Design data product for ${product.name}`,
        product_id: product.id,
        name: product.name,
        description: product.description
      })
      setDesignResult(response.data)
      setShowDesignModal(true)
    } catch (err) {
      console.error('Error designing data product:', err)
      setError(`Failed to design data product: ${err.response?.data?.detail || err.message}`)
    }
  }

  const handleValidate = async (product) => {
    try {
      setCurrentProduct(product)
      const response = await bankGenApi.validateDataProduct({
        id: product.id,
        name: product.name,
        description: product.description,
        status: product.status,
        refresh_frequency: product.refresh_frequency
      })
      setValidationResult(response.data)
      setShowValidationModal(true)
    } catch (err) {
      console.error('Error validating product:', err)
      setError(`Failed to validate data product: ${err.response?.data?.detail || err.message}`)
    }
  }

  const handleSaveDesign = async () => {
    try {
      await bankGenApi.updateDataProduct(currentProduct.id, {
        ...currentProduct,
        ...designResult,
        status: 'Active'
      })
      fetchDataProducts()
      setShowDesignModal(false)
    } catch (err) {
      console.error('Error saving design:', err)
      setError(`Failed to save design: ${err.response?.data?.detail || err.message}`)
    }
  }

  const handleDeleteProduct = async (product) => {
    if (confirm(`Are you sure you want to delete "${product.name}"?`)) {
      try {
        await bankGenApi.deleteDataProduct(product.id)
        fetchDataProducts()
      } catch (err) {
        console.error('Error deleting product:', err)
        setError(`Failed to delete data product: ${err.response?.data?.detail || err.message}`)
      }
    }
  }

  const renderCreateModal = () => {
    if (!showCreateModal) return null;
    
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white p-6 rounded-lg shadow-lg max-w-2xl w-full">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Design New Data Product</h2>
            <button 
              onClick={() => setShowCreateModal(false)}
              className="text-gray-500 hover:text-gray-700"
            >
              <XMarkIcon className="h-5 w-5" />
            </button>
          </div>
          
          <form onSubmit={handleCreateProduct} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Name</label>
              <input
                type="text"
                required
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                value={newProductData.name}
                onChange={(e) => setNewProductData({...newProductData, name: e.target.value})}
                placeholder="Enter product name"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700">Description</label>
              <textarea
                required
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                rows={3}
                value={newProductData.description}
                onChange={(e) => setNewProductData({...newProductData, description: e.target.value})}
                placeholder="Enter product description"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700">Refresh Frequency</label>
              <select
                required
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                value={newProductData.refresh_frequency}
                onChange={(e) => setNewProductData({...newProductData, refresh_frequency: e.target.value})}
              >
                <option value="Real-time">Real-time</option>
                <option value="Hourly">Hourly</option>
                <option value="Daily">Daily</option>
                <option value="Weekly">Weekly</option>
                <option value="Monthly">Monthly</option>
              </select>
            </div>

            {error && (
              <div className="text-red-500 text-sm mt-2">
                {error}
              </div>
            )}

            <div className="flex justify-end space-x-3 mt-6">
              <button
                type="button"
                onClick={() => setShowCreateModal(false)}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={loading}
                className="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
              >
                {loading ? 'Creating...' : 'Create Data Product'}
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  };

  const renderAttributesModal = () => {
    if (!currentProduct) return null
    
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white p-6 rounded-lg shadow-lg max-w-3xl w-full">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Recommended Attributes: {currentProduct.name}</h2>
            <button onClick={() => setShowAttributesModal(false)}>
              <XMarkIcon className="h-5 w-5" />
            </button>
          </div>
          <div className="overflow-y-auto max-h-96">
            <table className="min-w-full divide-y divide-gray-300">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900">Name</th>
                  <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Type</th>
                  <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Source</th>
                  <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Description</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 bg-white">
                {attributes.map((attr, index) => (
                  <tr key={index}>
                    <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900">{attr.name}</td>
                    <td className="px-3 py-4 text-sm text-gray-500">{attr.type}</td>
                    <td className="px-3 py-4 text-sm text-gray-500">{attr.source}</td>
                    <td className="px-3 py-4 text-sm text-gray-500">{attr.description}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="flex justify-end mt-4">
            <button
              onClick={() => setShowAttributesModal(false)}
              className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    )
  }

  const renderDesignModal = () => {
    if (!currentProduct || !designResult) return null
    
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white p-6 rounded-lg shadow-lg max-w-3xl w-full">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Design Data Product: {currentProduct.name}</h2>
            <button onClick={() => setShowDesignModal(false)}>
              <XMarkIcon className="h-5 w-5" />
            </button>
          </div>
          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-medium">Design Recommendations</h3>
              <p className="text-sm text-gray-500">{designResult.summary || "No summary available"}</p>
            </div>
            <div>
              <h3 className="text-lg font-medium">Proposed Schema</h3>
              <pre className="mt-2 p-3 bg-gray-100 rounded-md overflow-x-auto text-xs">
                {JSON.stringify(designResult.schema || {}, null, 2)}
              </pre>
            </div>
            <div>
              <h3 className="text-lg font-medium">Data Sources</h3>
              <ul className="mt-2 list-disc list-inside">
                {(designResult.data_sources || []).map((source, index) => (
                  <li key={index} className="text-sm">{source}</li>
                ))}
              </ul>
            </div>
          </div>
          <div className="flex justify-end space-x-3 pt-4">
            <button
              onClick={() => setShowDesignModal(false)}
              className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              onClick={handleSaveDesign}
              className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700"
            >
              Save Design
            </button>
          </div>
        </div>
      </div>
    )
  }

  const renderValidationModal = () => {
    if (!currentProduct || !validationResult) return null
    
    const isValid = validationResult.is_valid === true

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white p-6 rounded-lg shadow-lg max-w-2xl w-full">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Validation Results: {currentProduct.name}</h2>
            <button onClick={() => setShowValidationModal(false)}>
              <XMarkIcon className="h-5 w-5" />
            </button>
          </div>
          <div>
            <div className={`rounded-md ${isValid ? 'bg-green-50' : 'bg-red-50'} p-4 mb-4`}>
              <div className="flex">
                <div className="flex-shrink-0">
                  {isValid ? (
                    <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                  ) : (
                    <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                    </svg>
                  )}
                </div>
                <div className="ml-3">
                  <h3 className={`text-sm font-medium ${isValid ? 'text-green-800' : 'text-red-800'}`}>
                    {isValid ? 'Validation Passed' : 'Validation Failed'}
                  </h3>
                </div>
              </div>
            </div>
            
            <div className="space-y-4">
              <div>
                <h3 className="text-lg font-medium">Validation Summary</h3>
                <p className="text-sm text-gray-700 mt-1">{validationResult.summary || "No summary available"}</p>
              </div>
              
              {validationResult.issues && validationResult.issues.length > 0 && (
                <div>
                  <h3 className="text-lg font-medium">Issues Found</h3>
                  <ul className="mt-2 space-y-2">
                    {validationResult.issues.map((issue, index) => (
                      <li key={index} className="text-sm text-red-600">{issue}</li>
                    ))}
                  </ul>
                </div>
              )}
              
              {validationResult.recommendations && validationResult.recommendations.length > 0 && (
                <div>
                  <h3 className="text-lg font-medium">Recommendations</h3>
                  <ul className="mt-2 space-y-2">
                    {validationResult.recommendations.map((rec, index) => (
                      <li key={index} className="text-sm text-gray-700">{rec}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
          <div className="flex justify-end mt-4">
            <button
              onClick={() => setShowValidationModal(false)}
              className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    )
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
          onClick={() => {
            setError(null)
            fetchDataProducts()
          }}
          className="mt-4 px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700"
        >
          Retry
        </button>
      </div>
    )
  }

  return (
    <div className="p-6">
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-xl font-semibold text-gray-900">Data Products</h1>
          <p className="mt-2 text-sm text-gray-700">
            A list of all data products including their name, description, status, and other details.
          </p>
        </div>
        <div className="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
          <button
            onClick={() => setShowCreateModal(true)}
            className="inline-flex items-center justify-center rounded-md border border-transparent bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 sm:w-auto"
          >
            <PlusIcon className="h-4 w-4 mr-2" />
            Design New Data Product
          </button>
        </div>
      </div>

      {loading && (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
      )}

      {error && !loading && (
        <div className="mt-6 flex items-center justify-center">
          <div className="rounded-md bg-red-50 p-4">
            <div className="flex">
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">{error}</h3>
              </div>
            </div>
          </div>
        </div>
      )}

      {!loading && !error && (
        <div className="mt-8 flex flex-col">
          <div className="-my-2 -mx-4 overflow-x-auto sm:-mx-6 lg:-mx-8">
            <div className="inline-block min-w-full py-2 align-middle md:px-6 lg:px-8">
              <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
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
                        <td className="px-3 py-4 text-sm text-gray-500 max-w-md truncate">
                          {product.description}
                        </td>
                        <td className="px-3 py-4 text-sm">
                          <span className={`inline-flex rounded-full px-2 text-xs font-semibold leading-5 ${
                            product.status === 'Active'
                              ? 'bg-green-100 text-green-800'
                              : 'bg-yellow-100 text-yellow-800'
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
                              className="text-blue-600 hover:text-blue-900"
                              title="View Details"
                            >
                              <EyeIcon className="h-5 w-5" />
                            </button>
                            <button
                              onClick={() => handleEdit(product)}
                              className="text-blue-600 hover:text-blue-900"
                              title="Edit"
                            >
                              <PencilSquareIcon className="h-5 w-5" />
                            </button>
                            <button
                              onClick={() => handleDeleteProduct(product)}
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
            </div>
          </div>
        </div>
      )}

      {showCreateModal && renderCreateModal()}
      {showAttributesModal && renderAttributesModal()}
      {showDesignModal && renderDesignModal()}
      {showValidationModal && renderValidationModal()}
    </div>
  )
}