import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

function ImpactDashboard({ results }) {
  if (!results) return null

  const {
    zoning,
    school_impact,
    traffic_impact,
    transit_access,
    infrastructure,
    economic_impact,
    bottlenecks,
    ai_report
  } = results

  // Prepare school capacity data for chart
  const schoolData = school_impact.schools.map(school => ({
    name: school.name.split(' ')[0], // First word only
    capacity: school.capacity_pct
  }))

  return (
    <div className="p-6 space-y-6">
      <div className="border-b pb-4">
        <h2 className="text-2xl font-bold">Impact Analysis Results</h2>
        <p className="text-sm text-gray-500 mt-1">Comprehensive development impact assessment</p>
      </div>

      {/* Bottleneck Alerts */}
      {bottlenecks && bottlenecks.length > 0 && (
        <div className="space-y-2">
          <h3 className="font-bold text-lg">⚠️ Critical Issues</h3>
          {bottlenecks.map((bottleneck, index) => (
            <div
              key={index}
              className={`p-4 rounded-lg border-l-4 ${
                bottleneck.severity === 'HIGH'
                  ? 'bg-red-50 border-red-500'
                  : bottleneck.severity === 'MEDIUM'
                  ? 'bg-yellow-50 border-yellow-500'
                  : 'bg-blue-50 border-blue-500'
              }`}
            >
              <div className="flex items-start justify-between">
                <div>
                  <p className="font-medium text-sm text-gray-900">{bottleneck.type.replace('_', ' ')}</p>
                  <p className="text-sm text-gray-700 mt-1">{bottleneck.message}</p>
                </div>
                <span
                  className={`px-2 py-1 text-xs font-semibold rounded ${
                    bottleneck.severity === 'HIGH'
                      ? 'bg-red-100 text-red-800'
                      : bottleneck.severity === 'MEDIUM'
                      ? 'bg-yellow-100 text-yellow-800'
                      : 'bg-blue-100 text-blue-800'
                  }`}
                >
                  {bottleneck.severity}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Metric Cards */}
      <div className="grid grid-cols-3 gap-4">
        <MetricCard
          title="School Impact"
          value={`${school_impact.students_generated.toFixed(0)} students`}
          status={school_impact.bottlenecks.length > 0 ? 'critical' : 'good'}
          subtitle={`${school_impact.schools.length} schools nearby`}
        />
        <MetricCard
          title="Daily Trips"
          value={traffic_impact.daily_trips.toLocaleString()}
          status={traffic_impact.los_impacts.length > 0 ? 'warning' : 'good'}
          subtitle={`${traffic_impact.peak_trips.pm} PM peak`}
        />
        <div className="bg-yellow-50 rounded-lg p-4 border border-yellow-200">
          <p className="text-sm text-gray-600 mb-1">Transit Access</p>
          <p className="text-2xl font-bold text-gray-900">{transit_access.transit_score}</p>
          <div className="mt-2 space-y-1">
            <p className="text-xs text-gray-700">
              <span className="font-medium">Nearest:</span> {transit_access.nearest_station.name}
            </p>
            <p className="text-xs text-gray-600">
              {transit_access.nearest_station.line} Line • {transit_access.walk_time_minutes} min walk
            </p>
          </div>
        </div>
      </div>

      {/* School Capacity Chart */}
      {schoolData.length > 0 && (
        <div>
          <h3 className="font-bold text-lg mb-4">School Capacity Impact</h3>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={schoolData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="capacity" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
          <div className="flex items-center gap-2 mt-2 text-sm text-gray-600">
            <div className="w-3 h-3 bg-red-500 rounded"></div>
            <span>Over 100% = Overcapacity</span>
          </div>
        </div>
      )}

      {/* Nearby Transit Stations */}
      <div>
        <h3 className="font-bold text-lg mb-4">🚇 Nearby MARTA Stations</h3>
        
        <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Station</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Line</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Distance</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Walk Time</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {transit_access.nearby_stations.map((station, idx) => (
                <tr key={idx} className={idx === 0 ? 'bg-blue-50' : ''}>
                  <td className="px-4 py-3 whitespace-nowrap">
                    <div className="flex items-center">
                      {idx === 0 && <span className="mr-2">⭐</span>}
                      <span className={`text-sm font-medium ${idx === 0 ? 'text-blue-900' : 'text-gray-900'}`}>
                        {station.name}
                      </span>
                    </div>
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap">
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                      station.line.includes('Red') ? 'bg-red-100 text-red-800' :
                      station.line.includes('Gold') ? 'bg-yellow-100 text-yellow-800' :
                      station.line.includes('Green') ? 'bg-green-100 text-green-800' :
                      station.line.includes('Blue') ? 'bg-blue-100 text-blue-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {station.line}
                    </span>
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-600">
                    {(station.distance / 1000).toFixed(2)} km
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-600">
                    {((station.distance / 1.4) / 60).toFixed(1)} min
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        
        <p className="text-xs text-gray-500 mt-2">
          ⭐ Nearest station highlighted. Using real MARTA GTFS data (38 rail stations).
        </p>
      </div>

      {/* Infrastructure */}
      <div className="bg-gray-50 rounded-lg p-4">
        <h3 className="font-bold text-lg mb-3">Infrastructure</h3>
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <p className="text-gray-600">Water Demand</p>
            <p className="font-semibold">{infrastructure.water_demand.toLocaleString()} gpd</p>
          </div>
          <div>
            <p className="text-gray-600">Power Demand</p>
            <p className="font-semibold">{infrastructure.power_demand.toFixed(1)} kW</p>
          </div>
          <div className="col-span-2">
            <p className="text-gray-600">Upgrades Needed</p>
            <p className="font-semibold">
              {infrastructure.upgrades_needed.length > 0
                ? infrastructure.upgrades_needed.join(', ')
                : 'None - Infrastructure adequate'}
            </p>
            {infrastructure.estimated_cost > 0 && (
              <p className="text-red-600 font-bold mt-1">
                Est. Cost: ${infrastructure.estimated_cost.toLocaleString()}
              </p>
            )}
          </div>
        </div>
      </div>

      {/* Economic Impact */}
      <div className="bg-green-50 rounded-lg p-4">
        <h3 className="font-bold text-lg mb-3">Economic Impact</h3>
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <p className="text-gray-600">Annual Tax Revenue</p>
            <p className="font-semibold text-green-700">
              ${economic_impact.annual_tax_revenue.toLocaleString()}
            </p>
          </div>
          <div>
            <p className="text-gray-600">Infrastructure Cost</p>
            <p className="font-semibold text-red-700">
              ${economic_impact.infrastructure_cost.toLocaleString()}
            </p>
          </div>
          <div>
            <p className="text-gray-600">Break-even</p>
            <p className="font-semibold">{economic_impact.years_to_breakeven} years</p>
          </div>
          <div>
            <p className="text-gray-600">Jobs Created</p>
            <p className="font-semibold">
              {economic_impact.construction_jobs} construction, {economic_impact.permanent_jobs} permanent
            </p>
          </div>
        </div>
      </div>

      {/* AI Summary */}
      {ai_report && (
        <div className="bg-blue-50 rounded-lg p-6 border border-blue-200">
          <h3 className="font-bold text-lg mb-3 flex items-center gap-2">
            <span>🤖</span>
            AI Analysis
          </h3>
          <div className="prose prose-sm max-w-none">
            <pre className="whitespace-pre-wrap font-sans text-sm text-gray-700">
              {ai_report.ai_summary}
            </pre>
          </div>
          <p className="text-xs text-gray-500 mt-4">
            Generated at {new Date(ai_report.timestamp).toLocaleString()}
          </p>
        </div>
      )}
    </div>
  )
}

function MetricCard({ title, value, status, subtitle }) {
  const statusColors = {
    good: 'bg-green-50 border-green-200',
    warning: 'bg-yellow-50 border-yellow-200',
    critical: 'bg-red-50 border-red-200'
  }

  return (
    <div className={`p-4 rounded-lg border ${statusColors[status]}`}>
      <p className="text-sm text-gray-600 mb-1">{title}</p>
      <p className="text-2xl font-bold text-gray-900">{value}</p>
      {subtitle && <p className="text-xs text-gray-500 mt-1">{subtitle}</p>}
    </div>
  )
}

export default ImpactDashboard
