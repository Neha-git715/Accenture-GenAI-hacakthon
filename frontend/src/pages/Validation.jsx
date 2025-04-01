import { useState } from 'react'
import {
  PlusIcon,
  PencilSquareIcon,
  TrashIcon,
  CheckCircleIcon,
  ExclamationCircleIcon,
} from '@heroicons/react/24/outline'

const validationRules = [
  {
    id: 1,
    name: 'Balance Validation',
    description: 'Ensure account balance is not negative',
    type: 'Business Rule',
    status: 'Active',
    lastRun: '2 hours ago',
    successRate: '99.9%',
  },
  {
    id: 2,
    name: 'Email Format',
    description: 'Validate email address format',
    type: 'Format Rule',
    status: 'Active',
    lastRun: '4 hours ago',
    successRate: '100%',
  },
  {
    id: 3,
    name: 'Required Fields',
    description: 'Check all required fields are populated',
    type: 'Data Quality',
    status: 'Draft',
    lastRun: '1 day ago',
    successRate: '98.5%',
  },
]

export default function Validation() {
  const [selectedRule, setSelectedRule] = useState(null)

  const handleEdit = (rule) => {
    // TODO: Implement edit functionality
    console.log('Edit rule:', rule)
  }

  const handleDelete = (rule) => {
    // TODO: Implement delete functionality
    console.log('Delete rule:', rule)
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-gray-900">Validation Rules</h1>
        <button className="btn-primary flex items-center">
          <PlusIcon className="h-5 w-5 mr-2" />
          Add Rule
        </button>
      </div>

      {/* Validation Rules List */}
      <div className="grid gap-6">
        {validationRules.map((rule) => (
          <div key={rule.id} className="card">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center">
                  <h3 className="text-lg font-medium text-gray-900">{rule.name}</h3>
                  <span className={`ml-2 px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                    rule.status === 'Active' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {rule.status}
                  </span>
                </div>
                <p className="mt-1 text-sm text-gray-500">{rule.description}</p>
                <div className="mt-4 flex items-center space-x-4">
                  <span className="text-sm text-gray-500">
                    Type: {rule.type}
                  </span>
                  <span className="text-sm text-gray-500">
                    Last run: {rule.lastRun}
                  </span>
                  <span className="text-sm text-gray-500">
                    Success rate: {rule.successRate}
                  </span>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <button
                  onClick={() => handleEdit(rule)}
                  className="text-primary-600 hover:text-primary-900"
                >
                  <PencilSquareIcon className="h-5 w-5" />
                </button>
                <button
                  onClick={() => handleDelete(rule)}
                  className="text-red-600 hover:text-red-900"
                >
                  <TrashIcon className="h-5 w-5" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Validation Summary */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <CheckCircleIcon className="h-6 w-6 text-green-500" aria-hidden="true" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">Active Rules</dt>
                <dd className="text-lg font-semibold text-gray-900">8</dd>
              </dl>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <ExclamationCircleIcon className="h-6 w-6 text-yellow-500" aria-hidden="true" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">Failed Validations</dt>
                <dd className="text-lg font-semibold text-gray-900">12</dd>
              </dl>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <CheckCircleIcon className="h-6 w-6 text-blue-500" aria-hidden="true" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">Success Rate</dt>
                <dd className="text-lg font-semibold text-gray-900">99.5%</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 