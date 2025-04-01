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
    <div className="container mx-auto px-4">
      <div className="card">
        <h1 className="text-2xl font-semibold text-gray-900 mb-6">Data Product Validation</h1>
        <p className="text-gray-600 mb-4">
          This page will provide tools for validating your data products against requirements and quality standards.
        </p>
        <div className="bg-primary-50 border border-primary-200 rounded-lg p-4">
          <p className="text-primary-700">
            Feature coming soon! This page will include:
          </p>
          <ul className="list-disc list-inside mt-2 text-primary-600">
            <li>Data quality validation</li>
            <li>Schema validation</li>
            <li>Requirement compliance checking</li>
            <li>Validation reports and analytics</li>
          </ul>
        </div>
      </div>
    </div>
  )
} 