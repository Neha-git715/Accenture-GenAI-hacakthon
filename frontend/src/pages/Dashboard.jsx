import {
  ChartBarIcon,
  DocumentTextIcon,
  ClipboardDocumentListIcon,
  CheckCircleIcon,
} from '@heroicons/react/24/outline'

const stats = [
  { name: 'Total Data Products', value: '12', icon: DocumentTextIcon },
  { name: 'Active Requirements', value: '8', icon: ClipboardDocumentListIcon },
  { name: 'Validation Rules', value: '24', icon: CheckCircleIcon },
  { name: 'Data Quality Score', value: '98%', icon: ChartBarIcon },
]

const recentActivity = [
  {
    id: 1,
    type: 'Data Product Created',
    name: 'Customer 360 View',
    date: '2 hours ago',
  },
  {
    id: 2,
    type: 'Requirement Updated',
    name: 'Transaction History',
    date: '4 hours ago',
  },
  {
    id: 3,
    type: 'Validation Rule Added',
    name: 'Balance Validation',
    date: '6 hours ago',
  },
]

export default function Dashboard() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-gray-900">Dashboard</h1>
        <button className="btn-primary">
          Create New Data Product
        </button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((item) => (
          <div key={item.name} className="card">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <item.icon className="h-6 w-6 text-gray-400" aria-hidden="true" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">{item.name}</dt>
                  <dd className="text-lg font-semibold text-gray-900">{item.value}</dd>
                </dl>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Recent Activity */}
      <div className="card">
        <h2 className="text-lg font-medium text-gray-900 mb-4">Recent Activity</h2>
        <div className="flow-root">
          <ul role="list" className="-mb-8">
            {recentActivity.map((item, itemIdx) => (
              <li key={item.id}>
                <div className="relative pb-8">
                  {itemIdx !== recentActivity.length - 1 ? (
                    <span className="absolute left-4 top-4 -ml-px h-full w-0.5 bg-gray-200" aria-hidden="true" />
                  ) : null}
                  <div className="relative flex space-x-3">
                    <div>
                      <span className="h-8 w-8 rounded-full bg-primary-500 flex items-center justify-center ring-8 ring-white">
                        <CheckCircleIcon className="h-5 w-5 text-white" aria-hidden="true" />
                      </span>
                    </div>
                    <div className="min-w-0 flex-1 pt-1.5 flex justify-between space-x-4">
                      <div>
                        <p className="text-sm text-gray-500">
                          {item.type}{' '}
                          <span className="font-medium text-gray-900">{item.name}</span>
                        </p>
                      </div>
                      <div className="text-right text-sm whitespace-nowrap text-gray-500">
                        <time dateTime={item.date}>{item.date}</time>
                      </div>
                    </div>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  )
} 