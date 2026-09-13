'use client';

import { useEnergyStore } from '../../store/useEnergyStore';

export default function ResiliencePanel() {
  const { activeScenario, community, houses } = useEnergyStore();

  const peak = activeScenario === 'peakDemand';
  const gridFailure = activeScenario === 'gridFailure';
  const stressed = peak || gridFailure || activeScenario === 'heatwave';

  const risk = gridFailure ? 96 : peak ? 82 : stressed ? 61 : 18;

  const riskLabel =
    risk >= 70 ? 'HIGH' :
    risk >= 40 ? 'MEDIUM' :
    'LOW';

  const sellers = Math.max(2, Math.floor(houses.length * 0.08));
  const buyers = Math.max(3, Math.floor(houses.length * 0.12));
  const traded = peak ? 6.4 : gridFailure ? 4.8 : 2.1;

  const actions = peak
    ? [
        'P2P surplus matching activated',
        'Flexible EV charging deferred',
        'Battery reserve prioritized',
      ]
    : gridFailure
    ? [
        'Island-mode resilience activated',
        'Local energy transfer prioritized',
        'Critical loads preserved',
      ]
    : [
        'Continuous risk monitoring active',
        'Local surplus scanning active',
        'Autonomous recovery standby',
      ];

  return (
    <div
      style={{
        margin: '12px 0',
        border: '2px solid #212121',
        background: '#FFFFFF',
      }}
    >
      <div
        style={{
          background: '#212121',
          color: '#FFFFFF',
          padding: '10px 14px',
          fontFamily: 'monospace',
          fontSize: '11px',
          fontWeight: 900,
          letterSpacing: '0.1em',
        }}
      >
        FlowState / AUTONOMOUS RESILIENCE
      </div>

      <div
        style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr 1fr',
          gap: '8px',
          padding: '12px',
        }}
      >
        <Metric label="FAILURE RISK" value={`${risk}%`} sub={riskLabel} />
        <Metric
          label="P2P ENERGY"
          value={`${traded}`}
          sub="kWh traded"
        />
        <Metric
          label="LOCAL ACTORS"
          value={`${sellers}/${buyers}`}
          sub="sellers / buyers"
        />
      </div>

      <div
        style={{
          borderTop: '1px solid #D1D5DB',
          padding: '10px 14px',
          fontFamily: 'monospace',
          fontSize: '10px',
        }}
      >
        <div
          style={{
            fontWeight: 900,
            marginBottom: '7px',
            textTransform: 'uppercase',
          }}
        >
          Autonomous actions
        </div>

        {actions.map((action) => (
          <div
            key={action}
            style={{
              padding: '5px 0',
              color: '#374151',
              display: 'flex',
              gap: '7px',
            }}
          >
            <span style={{ color: '#FF6600', fontWeight: 900 }}>›</span>
            {action}
          </div>
        ))}
      </div>
    </div>
  );
}

function Metric({
  label,
  value,
  sub,
}: {
  label: string;
  value: string;
  sub: string;
}) {
  return (
    <div
      style={{
        border: '1px solid #D1D5DB',
        padding: '9px',
      }}
    >
      <div
        style={{
          fontSize: '8px',
          color: '#6B7280',
          fontWeight: 900,
          marginBottom: '4px',
        }}
      >
        {label}
      </div>

      <div
        style={{
          fontSize: '22px',
          fontWeight: 900,
          lineHeight: 1,
        }}
      >
        {value}
      </div>

      <div
        style={{
          fontSize: '8px',
          color: '#6B7280',
          marginTop: '4px',
          textTransform: 'uppercase',
        }}
      >
        {sub}
      </div>
    </div>
  );
}
