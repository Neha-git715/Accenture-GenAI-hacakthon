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
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-gray-900">Requirements</h1>
        <button className="btn-primary flex items-center">
          <PlusIcon className="h-5 w-5 mr-2" />
          Add Requirement
        </button>
      </div>

      {/* Requirements List */}
      <div className="grid gap-6">
        {requirements.map((requirement) => (
          <div key={requirement.id} className="card">
            <div className="flex items-start justify-between">
              <div>
                <h3 className="text-lg font-medium text-gray-900">{requirement.name}</h3>
                <p className="mt-1 text-sm text-gray-500">{requirement.description}</p>
                <div className="mt-4 flex items-center space-x-4">
                  <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                    requirement.status === 'Active' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {requirement.status}
                  </span>
                  <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                    requirement.priority === 'High' ? 'bg-red-100 text-red-800' : 'bg-blue-100 text-blue-800'
                  }`}>
                    {requirement.priority}
                  </span>
                  <span className="text-sm text-gray-500">
                    Last updated: {requirement.lastUpdated}
                  </span>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <button
                  onClick={() => handleEdit(requirement)}
                  className="text-primary-600 hover:text-primary-900"
                >
                  <PencilSquareIcon className="h-5 w-5" />
                </button>
                <button
                  onClick={() => handleDelete(requirement)}
                  className="text-red-600 hover:text-red-900"
                >
                  <TrashIcon className="h-5 w-5" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
} 