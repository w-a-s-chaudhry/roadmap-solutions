// Author:      Wajid Ali Chaudhry
// Description: Axios instance pointing at the FastAPI backend.

import axios from 'axios'

const api = axios.create({ baseURL: "http://localhost:8000" })

// Module-level token - updated by AuthContext on login/logout
let _token: string | null = null

// Call this whenever the token changes
export function setToken(token: string | null) {
    _token = token
}

// Attach Bearer token to every outgoing request if one is not set
api.interceptors.request.use((config) => {
    if (_token) {
        config.headers.Authorization = `Bearer ${_token}`
    }
    return config
})

export default api