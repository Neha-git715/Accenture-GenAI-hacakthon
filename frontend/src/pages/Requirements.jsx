import { useState } from 'react'
import {
  PlusIcon,
  PencilSquareIcon,
  TrashIcon,
} from '@heroicons/react/24/outline'

const requirements = [
  {
    id: 1,
    name: 'Customer Profile',
    description: 'Basic customer information and demographics',
    status: 'Active',
    priority: 'High',
    lastUpdated: '2 hours ago',
  },
  {
    id: 2,
    name: 'Transaction Data',
    description: 'Detailed transaction records and history',
    status: 'Active',
    priority: 'High',
    lastUpdated: '4 hours ago',
  },
  {
    id: 3,
    name: 'Account Details',
    description: 'Account information and balances',
    status: 'Draft',
    priority: 'Medium',
    lastUpdated: '1 day ago',
  },
]

export default function Requirements() {
  const [selectedRequirement, setSelectedRequirement] = useState(null)

  const handleEdit = (requirement) => {
    // TODO: Implement edit functionality
    console.log('Edit requirement:', requirement)
  }

  const handleDelete = (requirement) => {
    // TODO: Implement delete functionality
    console.log('Delete requirement:', requirement)
  }

  return (
    <div className="container mx-auto px-4">
      <div className="card">
        <h1 className="text-2xl font-semibold text-gray-900 mb-6">Requirements Analysis</h1>
        <p className="text-gray-600 mb-4">
          This page will allow you to analyze and track requirements for data products.
        </p>
        <div className="bg-primary-50 border border-primary-200 rounded-lg p-4">
          <p className="text-primary-700">
            Feature coming soon! This page will include:
          </p>
          <ul className="list-disc list-inside mt-2 text-primary-600">
            <li>Requirements gathering and analysis</li>
            <li>Automated requirement validation</li>
            <li>Requirement tracking and versioning</li>
            <li>Integration with data product design</li>
          </ul>
        </div>
      </div>
    </div>
  )
} 