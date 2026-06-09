// Author:      Wajid Ali Chaudhry
// Description: Stores the access token in memory and exposes
//              login / logout helpers to the whole app.

import { setToken } from '@/api/api'
import { createContext, useState, useContext, type ReactNode } from 'react'

// --- Types ---

interface AuthContextType {
  accessToken: string | null
  login: (token: string) => void
  logout: () => void
}

// --- Context ---

const AuthContext = createContext<AuthContextType | null>(null)

// --- Provider ---

// Wraps the app and makes auth state available everywhere
export function AuthProvider({ children }: { children: ReactNode }) {
  const [accessToken, setAccessToken] = useState<string | null>(null)

  function login(token: string) {
    setAccessToken(token)
    setToken(token)
  }

  function logout() {
    setAccessToken(null)
    setToken(null)
  }

  return (
    <AuthContext.Provider value={{ accessToken, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

// --- Hook ---

// Any component can call useAuth() to read the token or call login/logout
// eslint-disable-next-line react-refresh/only-export-components
export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used inside AuthProvider')
  return ctx
}
