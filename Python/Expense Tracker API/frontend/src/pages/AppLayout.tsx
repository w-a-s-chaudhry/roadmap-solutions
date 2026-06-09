// Author:      Wajid Ali Chaudhry
// Description: App shell — sidebar navigation + page outlet.
//              All private pages are rendered inside <main> via <Outlet>.

import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { useAuth } from '@/context/AuthContext'
import api from '@/api/api'

// --- Types ---

interface UserProfile {
    id: number
    name: string
    email: string
}

// --- Constants ---

const NAV_ITEMS = [
    { label: 'Dashboard', to: '/app' },
    { label: 'Expenses', to: '/app/expenses' },
    { label: 'Add expense', to: '/app/expenses/new' },
]

const DISABLED_NAV = ['Summary', 'Settings']

// --- Component ---

// Sidebar shell — fetches current user, renders nav, wraps pages
export default function AppLayout() {
    const { logout } = useAuth()
    const navigate = useNavigate()

    // Fetches the logged-in user's profile for the sidebar footer
    const { data: user } = useQuery<UserProfile>({
        queryKey: ['me'],
        queryFn: async () => {
            const res = await api.get('/auth/me')
            return res.data
        },
    })

    // Clears the token and sends the user back to login
    function handleLogout() {
        logout()
        navigate('/')
    }

    // --- Render ---

    return (
        <div className="app-layout">
            <aside className="sidebar">

                {/* Logo */}
                <div className="sidebar-logo">
                    <div className="login-logo-dot" />
                    <span className="login-logo-text">Expensr</span>
                </div>

                {/* Primary nav */}
                <nav className="sidebar-nav">
                    {NAV_ITEMS.map(({ label, to }) => (
                        <NavLink
                            key={to}
                            to={to}
                            end
                            className={({ isActive }) =>
                                `sidebar-link${isActive ? ' active' : ''}`
                            }
                        >
                            {label}
                        </NavLink>
                    ))}

                    {/* Out-of-scope items — visible but disabled */}
                    {DISABLED_NAV.map((label) => (
                        <span key={label} className="sidebar-link disabled">
                            {label}
                            <span className="sidebar-soon">soon</span>
                        </span>
                    ))}
                </nav>

                {/* User footer */}
                <div className="sidebar-footer">
                    <div className="sidebar-user">
                        <p className="sidebar-user-name">
                            {user?.name ?? '...'}
                        </p>
                        <p className="sidebar-user-email">
                            {user?.email ?? '...'}
                        </p>
                    </div>
                    <button
                        className="sidebar-logout"
                        onClick={handleLogout}
                    >
                        Log out
                    </button>
                </div>

            </aside>

            {/* Active page renders here */}
            <main className="app-main">
                <Outlet />
            </main>
        </div>
    )
}
