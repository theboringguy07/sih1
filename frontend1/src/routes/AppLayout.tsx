import React from 'react'
import { Link, NavLink, Outlet, useNavigate } from 'react-router-dom'
import { useTheme } from '../theme/ThemeContext'

const AppLayout: React.FC = () => {
  const { mode, toggle } = useTheme()
  const navigate = useNavigate()

  return (
    <div className={mode === 'dark' ? 'dark' : ''}>
      <nav className={`fixed top-0 inset-x-0 z-50 border-b backdrop-blur-md transition-colors duration-300 ${mode === 'light' ? 'bg-white/95 border-slate-200' : 'bg-slate-900/80 border-white/10'}`}>
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <Link to="/" className={`font-black tracking-tight transition-colors duration-300 ${mode === 'light' ? 'text-slate-900' : 'text-white'}`}>AI Internship Engine</Link>
          <div className="flex items-center gap-6">
            {['/', '/about', '/faqs'].map((to, i) => {
              const label = i === 0 ? 'Home' : i === 1 ? 'About' : 'FAQs'
              return (
                <NavLink key={to} to={to} className={({isActive}) => `relative transition-colors duration-300 ${mode === 'light' ? 'text-slate-900 hover:text-indigo-600' : 'text-white hover:text-indigo-400'} ${isActive ? 'font-semibold' : ''}`}>
                  <span className="after:absolute after:left-0 after:-bottom-1 after:h-[2px] after:w-0 after:bg-gradient-to-r after:from-indigo-500 after:to-purple-600 after:transition-all after:duration-300 hover:after:w-full">{label}</span>
                </NavLink>
              )
            })}
            <Link to="/filter/about" className="hidden sm:inline-flex items-center gap-2 bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-semibold px-4 py-2 rounded-xl shadow-lg shadow-indigo-900/20 transition-colors duration-300">Find Internships</Link>
            <button className={`rounded-xl px-3 py-2 transition-colors duration-300 ${mode === 'light' ? 'bg-slate-100 text-slate-900' : 'bg-white/10 text-white'}`} onClick={toggle} aria-label="Toggle theme">
              {mode === 'light' ? 'Dark' : 'Light'}
            </button>
          </div>
        </div>
      </nav>
      <main className="max-w-6xl mx-auto px-6 pt-20">
        <Outlet />
      </main>
    </div>
  )
}

export default AppLayout


