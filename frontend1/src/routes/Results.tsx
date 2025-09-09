import React, { useMemo, useState } from 'react'

type ResultItem = {
  id: string
  title: string
  company: string
  location: string
  stipend: number
  duration: string
  type: 'Work From Home' | 'Hybrid' | 'On-site' | 'Part-time'
}

const MOCK: ResultItem[] = Array.from({ length: 28 }).map((_, i) => ({
  id: String(i + 1),
  title: `Software Intern ${i + 1}`,
  company: 'Acme Corp',
  location: ['Remote', 'Mumbai', 'Bengaluru', 'Delhi'][i % 4],
  stipend: 5000 + (i % 20) * 500,
  duration: ['1 month', '3 months', '6 months'][i % 3],
  type: (['Work From Home', 'Hybrid', 'On-site', 'Part-time'] as const)[i % 4],
}))

const Results: React.FC = () => {
  const [query, setQuery] = useState({
    profile: '',
    location: '',
    stipend: 5000,
    duration: '',
    wfh: false,
    hybrid: false,
    onsite: false,
    parttime: false,
  })

  const filtered = useMemo(() => {
    return MOCK.filter((r) => {
      if (query.location && !r.location.toLowerCase().includes(query.location.toLowerCase())) return false
      if (query.profile && !r.title.toLowerCase().includes(query.profile.toLowerCase())) return false
      if (r.stipend < query.stipend) return false
      if (query.duration && r.duration !== query.duration) return false
      if (query.wfh && r.type !== 'Work From Home') return false
      if (query.hybrid && r.type !== 'Hybrid') return false
      if (query.onsite && r.type !== 'On-site') return false
      if (query.parttime && r.type !== 'Part-time') return false
      return true
    })
  }, [query])

  const [page, setPage] = useState(1)
  const pageSize = 10
  const totalPages = Math.max(1, Math.ceil(filtered.length / pageSize))
  const pageItems = useMemo(() => {
    const start = (page - 1) * pageSize
    return filtered.slice(start, start + pageSize)
  }, [filtered, page])

  return (
    <div className="section">
      <div className="results-count">{filtered.length} Internships Found</div>
      <div className="layout">
        <aside className="card sidebar" aria-label="Filters">
          <div style={{ padding: 16 }}>
            <div className="filter-header">
              <strong>Filters</strong>
              <button className="clear-btn" onClick={() => { setQuery({ profile: '', location: '', stipend: 5000, duration: '', wfh: false, hybrid: false, onsite: false, parttime: false }); setPage(1); }}>Clear all</button>
            </div>

            <div className="filter-group">
              <div className="field">
                <label className="label">Profile</label>
                <input className="input" placeholder="e.g. Software, Data, UI/UX" value={query.profile} onChange={(e) => setQuery({ ...query, profile: e.target.value })} />
              </div>
            </div>

            <div className="filter-group">
              <div className="field">
                <label className="label">Location</label>
                <input className="input" placeholder="Any city or Remote" value={query.location} onChange={(e) => setQuery({ ...query, location: e.target.value })} />
              </div>
            </div>

            <div className="filter-group">
              <div className="field">
                <label className="label">Minimum Monthly Stipend</label>
                <input type="range" min={0} max={30000} step={500} value={query.stipend} onChange={(e) => setQuery({ ...query, stipend: Number(e.target.value) })} />
                <div style={{ color: 'var(--muted)' }}>₹{query.stipend.toLocaleString()}</div>
              </div>
            </div>

            <div className="filter-group">
              <div className="field">
                <label className="label">Duration</label>
                <select className="select" value={query.duration} onChange={(e) => setQuery({ ...query, duration: e.target.value })}>
                  <option value="">Any</option>
                  <option value="1 month">1 month</option>
                  <option value="3 months">3 months</option>
                  <option value="6 months">6 months</option>
                </select>
              </div>
            </div>

            <div className="filter-group">
              <label className="checkbox"><input type="checkbox" checked={query.wfh} onChange={(e) => setQuery({ ...query, wfh: e.target.checked })} /> Work From Home</label>
              <label className="checkbox"><input type="checkbox" checked={query.hybrid} onChange={(e) => setQuery({ ...query, hybrid: e.target.checked })} /> Hybrid</label>
              <label className="checkbox"><input type="checkbox" checked={query.onsite} onChange={(e) => setQuery({ ...query, onsite: e.target.checked })} /> On-site</label>
              <label className="checkbox"><input type="checkbox" checked={query.parttime} onChange={(e) => setQuery({ ...query, parttime: e.target.checked })} /> Part-time</label>
            </div>
          </div>
        </aside>

        <section className="results">
          {pageItems.map((r) => (
            <div className="card-item" key={r.id}>
              <div>
                <div style={{ fontWeight: 900 }}>{r.title}</div>
                <div style={{ color: 'var(--muted)' }}>{r.company} • {r.location} • {r.duration} • ₹{r.stipend.toLocaleString()}</div>
              </div>
              <button className="apply-btn">Apply Now</button>
            </div>
          ))}
        </section>
      </div>
      {filtered.length > pageSize && (
        <div className="pager">
          <button className="pager-btn" disabled={page <= 1} onClick={() => setPage((p) => Math.max(1, p - 1))}>← Prev</button>
          <span className="pager-info">Page {page} / {totalPages}</span>
          <button className="pager-btn" disabled={page >= totalPages} onClick={() => setPage((p) => Math.min(totalPages, p + 1))}>Next →</button>
        </div>
      )}
    </div>
  )
}

export default Results


