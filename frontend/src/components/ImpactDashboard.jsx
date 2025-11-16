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
  const schoolData = school_impact.schools.slice(0, 8).map(school => ({
    name: school.name.split(' ')[0], // First word only
    capacity: school.capacity_pct
  }))

  return (
    <div className="h-full overflow-y-auto">
      {/* Header */}
      <div className="sticky top-0 bg-white border-b border-gray-200 p-4 z-10">
        <h2 className="text-xl font-bold text-gray-900">Impact Analysis</h2>
        <p className="text-xs text-gray-500 mt-1">Comprehensive development assessment</p>
      </div>

      <div className="p-4 space-y-4">
        {/* Bottleneck Alerts */}
        {bottlenecks && bottlenecks.length > 0 && (
          <div className="space-y-2">
            <h3 className="font-semibold text-sm text-gray-900">⚠️ Critical Issues</h3>
            <div className="space-y-2 max-h-48 overflow-y-auto">
              {bottlenecks.slice(0, 5).map((bottleneck, index) => (
                <div
                  key={index}
                  className={`p-3 rounded-md border-l-4 text-sm ${
                    bottleneck.severity === 'HIGH'
                      ? 'bg-red-50 border-red-500'
                      : bottleneck.severity === 'MEDIUM'
                      ? 'bg-yellow-50 border-yellow-500'
                      : 'bg-blue-50 border-blue-500'
                  }`}
                >
                  <div className="flex items-start justify-between gap-2">
                    <p className="text-gray-900 text-xs flex-1">{bottleneck.message}</p>
                    <span
                      className={`px-2 py-0.5 text-xs font-semibold rounded whitespace-nowrap ${
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
            {bottlenecks.length > 5 && (
              <p className="text-xs text-gray-500 text-center">
                +{bottlenecks.length - 5} more issues
              </p>
            )}
          </div>
        )}

        {/* Metric Cards - Compact Grid */}
        <div className="grid grid-cols-2 gap-3">
          <MetricCard
            title="School Impact"
            value={`${school_impact.students_generated.toFixed(0)}`}
            unit="students"
            status={school_impact.bottlenecks.length > 0 ? 'critical' : 'good'}
            subtitle={`${school_impact.schools.length} schools`}
          />
          <MetricCard
            title="Daily Trips"
            value={traffic_impact.daily_trips.toLocaleString()}
            status={traffic_impact.los_impacts.length > 0 ? 'warning' : 'good'}
            subtitle={`${traffic_impact.peak_trips.pm} PM peak`}
          />
        </div>

        {/* Transit Access - Full Width */}
        <div className="bg-yellow-50 rounded-lg p-3 border border-yellow-200">
          <p className="text-xs font-medium text-gray-700 mb-1">Transit Access</p>
          <p className="text-xl font-bold text-gray-900">{transit_access.transit_score}</p>
          <div className="mt-2 space-y-0.5">
            <p className="text-xs text-gray-700">
              <span className="font-medium">Nearest:</span> {transit_access.nearest_station.name}
            </p>
            <p className="text-xs text-gray-600">
              {transit_access.nearest_station.line} • {transit_access.walk_time_minutes} min walk
            </p>
          </div>
        </div>

        {/* School Capacity Chart - Collapsible */}
        {schoolData.length > 0 && (
          <details open className="bg-gray-50 rounded-lg border border-gray-200">
            <summary className="cursor-pointer p-3 font-semibold text-sm text-gray-900 hover:bg-gray-100 rounded-t-lg">
              📊 School Capacity Impact
            </summary>
            <div className="p-3">
              <ResponsiveContainer width="100%" height={180}>
                <BarChart data={schoolData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" tick={{ fontSize: 10 }} />
                  <YAxis tick={{ fontSize: 10 }} />
                  <Tooltip />
                  <Bar dataKey="capacity" fill="#3b82f6" />
                </BarChart>
              </ResponsiveContainer>
              <div className="flex items-center gap-2 mt-2 text-xs text-gray-600">
                <div className="w-2 h-2 bg-red-500 rounded"></div>
                <span>Over 100% = Overcapacity</span>
              </div>
            </div>
          </details>
        )}

        {/* Nearby Transit Stations - Collapsible */}
        <details className="bg-white rounded-lg border border-gray-200">
          <summary className="cursor-pointer p-3 font-semibold text-sm text-gray-900 hover:bg-gray-50 rounded-t-lg">
            🚇 Nearby MARTA Stations ({transit_access.nearby_stations.length})
          </summary>
          <div className="overflow-x-auto">
            <table className="min-w-full text-xs">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-3 py-2 text-left font-medium text-gray-500">Station</th>
                  <th className="px-3 py-2 text-left font-medium text-gray-500">Line</th>
                  <th className="px-3 py-2 text-left font-medium text-gray-500">Walk</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {transit_access.nearby_stations.map((station, idx) => (
                  <tr key={idx} className={idx === 0 ? 'bg-blue-50' : 'bg-white'}>
                    <td className="px-3 py-2">
                      <div className="flex items-center gap-1">
                        {idx === 0 && <span className="text-xs">⭐</span>}
                        <span className={idx === 0 ? 'font-medium text-blue-900' : 'text-gray-900'}>
                          {station.name}
                        </span>
                      </div>
                    </td>
                    <td className="px-3 py-2">
                      <span className={`px-2 py-0.5 text-xs font-medium rounded-full ${
                        station.line.includes('Red') ? 'bg-red-100 text-red-800' :
                        station.line.includes('Gold') ? 'bg-yellow-100 text-yellow-800' :
                        station.line.includes('Green') ? 'bg-green-100 text-green-800' :
                        station.line.includes('Blue') ? 'bg-blue-100 text-blue-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {station.line}
                      </span>
                    </td>
                    <td className="px-3 py-2 text-gray-600">
                      {((station.distance / 1.4) / 60).toFixed(1)} min
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </details>

        {/* Infrastructure - Collapsible */}
        <details className="bg-gray-50 rounded-lg border border-gray-200">
          <summary className="cursor-pointer p-3 font-semibold text-sm text-gray-900 hover:bg-gray-100 rounded-t-lg">
            🏗️ Infrastructure
          </summary>
          <div className="p-3 space-y-2 text-xs">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <p className="text-gray-600">Water Demand</p>
                <p className="font-semibold text-gray-900">{infrastructure.water_demand.toLocaleString()} gpd</p>
              </div>
              <div>
                <p className="text-gray-600">Power Demand</p>
                <p className="font-semibold text-gray-900">{infrastructure.power_demand.toFixed(1)} kW</p>
              </div>
            </div>
            <div>
              <p className="text-gray-600 mb-1">Upgrades Needed</p>
              <p className="font-semibold text-gray-900">
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
        </details>

        {/* Economic Impact - Collapsible */}
        <details className="bg-green-50 rounded-lg border border-green-200">
          <summary className="cursor-pointer p-3 font-semibold text-sm text-gray-900 hover:bg-green-100 rounded-t-lg">
            💰 Economic Impact
          </summary>
          <div className="p-3 grid grid-cols-2 gap-3 text-xs">
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
              <p className="font-semibold text-gray-900">{economic_impact.years_to_breakeven} years</p>
            </div>
            <div>
              <p className="text-gray-600">Jobs Created</p>
              <p className="font-semibold text-gray-900">
                {economic_impact.construction_jobs} construction
              </p>
              <p className="text-xs text-gray-600">
                {economic_impact.permanent_jobs} permanent
              </p>
            </div>
          </div>
        </details>

        {/* AI Summary - Collapsible */}
        {ai_report && (
          <details className="bg-blue-50 rounded-lg border border-blue-200">
            <summary className="cursor-pointer p-3 font-semibold text-sm text-gray-900 hover:bg-blue-100 rounded-t-lg">
              🤖 AI Analysis
            </summary>
            <div className="p-3">
              <pre className="whitespace-pre-wrap font-sans text-xs text-gray-700 leading-relaxed">
                {ai_report.ai_summary}
              </pre>
            </div>
          </details>
        )}
      </div>

      {/* Bottom Tip */}
      <div className="sticky bottom-0 bg-blue-50 border-t border-blue-100 p-3">
        <p className="text-xs text-blue-800 text-center">
          💡 Drag marker or adjust parameters to re-analyze
        </p>
      </div>
    </div>
  )
}

function MetricCard({ title, value, unit, status, subtitle }) {
  const statusColors = {
    good: 'bg-green-50 border-green-200',
    warning: 'bg-yellow-50 border-yellow-200',
    critical: 'bg-red-50 border-red-200'
  }

  return (
    <div className={`p-3 rounded-lg border ${statusColors[status]}`}>
      <p className="text-xs text-gray-600 mb-1">{title}</p>
      <div className="flex items-baseline gap-1">
        <p className="text-xl font-bold text-gray-900">{value}</p>
        {unit && <p className="text-xs text-gray-600">{unit}</p>}
      </div>
      {subtitle && <p className="text-xs text-gray-500 mt-1">{subtitle}</p>}
    </div>
  )
}

export default ImpactDashboard