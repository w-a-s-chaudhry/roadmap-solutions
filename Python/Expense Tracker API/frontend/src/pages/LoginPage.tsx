// Author:      Wajid Ali Chaudhry
// Description: Login page — email + password form, posts to
//              /auth/login and stores the returned access token.

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import api from '../api/api'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
} from '@/components/ui/card'

// --- Validation schema ---

const loginSchema = z.object({
    email: z.string().email('Invalid email'),
    password: z.string().min(1, 'Password is required'),
})

type LoginFormData = z.infer<typeof loginSchema>

// --- Component ---

// Renders the login form and handles submission
export default function LoginPage() {
    const { login } = useAuth()
    const navigate = useNavigate()
    const [serverError, setServerError] = useState('')
    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<LoginFormData>({
        resolver: zodResolver(loginSchema),
    })

    // Submits credentials and stores the returned token on success
    async function onSubmit(data: LoginFormData) {
        setServerError('')
        try {
            const res = await api.post('/auth/login', {
                email: data.email,
                password: data.password,
            })
            login(res.data.access_token)
            navigate('/app')
        } catch (err: unknown) {
            const detail =
                (err as { response?: { data?: { detail?: unknown } } })
                    ?.response?.data?.detail
            const msg =
                typeof detail === 'string'
                    ? detail
                    : Array.isArray(detail)
                        ? (detail as { msg: string }[])
                            .map(e => e.msg).join(', ')
                        : 'Login failed'
            setServerError(msg)
        }
    }

    // --- Render ---

    return (
        <div className="login-page">
            <Card className="login-card">
                <CardHeader>
                    <div className="login-logo">
                        <div className="login-logo-dot" />
                        <span className="login-logo-text">Expensr</span>
                    </div>
                    <CardTitle>Welcome back</CardTitle>
                    <p className="login-subtitle">
                        Log in to see your expenses.
                    </p>
                </CardHeader>
                <CardContent>
                    <form
                        onSubmit={handleSubmit(onSubmit)}
                        className="login-form"
                    >
                        <div className="login-field">
                            <Label htmlFor="email">Email</Label>
                            <Input
                                id="email"
                                type="email"
                                placeholder="you@email.com"
                                {...register('email')}
                            />
                            {errors.email?.message && (
                                <p className="field-error">
                                    {errors.email.message}
                                </p>
                            )}
                        </div>

                        <div className="login-field">
                            <Label htmlFor="password">Password</Label>
                            <Input
                                id="password"
                                type="password"
                                placeholder="••••••••"
                                {...register('password')}
                            />
                            {errors.password?.message && (
                                <p className="field-error">
                                    {errors.password.message}
                                </p>
                            )}
                        </div>

                        {serverError && (
                            <p className="field-error">{serverError}</p>
                        )}

                        <Button type="submit">Log in</Button>
                    </form>

                    <p className="login-signup-prompt">
                        New here?{' '}
                        <Link
                            to="/register"
                            className="login-signup-link"
                        >
                            Sign up
                        </Link>
                    </p>
                </CardContent>
            </Card>
        </div>
    )
}
