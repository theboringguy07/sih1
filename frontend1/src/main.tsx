import React from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { ThemeProvider } from './theme/ThemeContext'
import './styles.css'
import AppLayout from './routes/AppLayout'
import Home from './routes/Home'
import About from './routes/About'
import Faqs from './routes/Faqs'
import FilterAbout from './routes/FilterAbout'
import FilterInterests from './routes/FilterInterests'
import LoadingPage from './routes/LoadingPage'
import Results from './routes/Results'

const router = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,
    children: [
      { index: true, element: <Home /> },
      { path: 'about', element: <About /> },
      { path: 'faqs', element: <Faqs /> },
      { path: 'filter/about', element: <FilterAbout /> },
      { path: 'filter/interests', element: <FilterInterests /> },
      { path: 'loading', element: <LoadingPage /> },
      { path: 'results', element: <Results /> },
    ],
  },
])

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ThemeProvider>
      <RouterProvider router={router} />
    </ThemeProvider>
  </React.StrictMode>
)


