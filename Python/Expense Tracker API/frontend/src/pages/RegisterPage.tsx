// Author:      Wajid Ali Chaudhry
// Description: Register page — name + email + password form, posts to
//              /auth/register and redirects to login on success.

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { useNavigate, Link } from 'react-router-dom'
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

const registerSchema = z.object({
    name: z.string().min(2, 'Name must be at least 2 characters').max(50, 'Name must be at most 50 characters'),
    email: z.string().email('Invalid email address'),
    password: z.string().min(8, 'Password must be at least 8 characters'),

    confirmPassword: z.string(),
}).refine(
    (data) => data.password === data.confirmPassword,
    { message: 'Passwords do not match', path: ['confirmPassword'] }
)

type RegisterFormData = z.infer<typeof registerSchema>

// --- Component ---

// Renders the registration form and handles submission
export default function RegisterPage() {
    const navigate = useNavigate()
    const [serverError, setServerError] = useState('')
    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<RegisterFormData>({
        resolver: zodResolver(registerSchema),
    })

    // Posts new user to /auth/register; redirects to login on success
    async function onSubmit(data: RegisterFormData) {
        setServerError('')
        try {
            await api.post('/auth/register', {
                name: data.name,
                email: data.email,
                password: data.password
            })

            navigate('/')
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
                        : 'Registration Failed'
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
                    <CardTitle>Create account</CardTitle>
                    <p className="login-subtitle">
                        Track your spending in seconds.
                    </p>
                </CardHeader>
                <CardContent>
                    <form
                        onSubmit={handleSubmit(onSubmit)}
                        className="login-form"
                    >
                        <div className="login-field">
                            <Label htmlFor="name">Name</Label>
                            <Input
                                id="name"
                                type="text"
                                placeholder="Your name"
                                {...register('name')}
                            />
                            {errors.name?.message && (
                                <p className="field-error">
                                    {errors.name.message}
                                </p>
                            )}
                        </div>

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

                        <div className="login-field">
                            <Label htmlFor="confirmPassword">
                                Confirm password
                            </Label>
                            <Input
                                id="confirmPassword"
                                type="password"
                                placeholder="••••••••"
                                {...register('confirmPassword')}
                            />
                            {errors.confirmPassword?.message && (
                                <p className="field-error">
                                    {errors.confirmPassword.message}
                                </p>
                            )}
                        </div>

                        {serverError && (
                            <p className="field-error">{serverError}</p>
                        )}

                        <Button type="submit">Create account</Button>
                    </form>

                    <p className="login-signup-prompt">
                        Already have an account?{' '}
                        <Link to="/" className="login-signup-link">
                            Log in
                        </Link>
                    </p>
                </CardContent>
            </Card>
        </div>
    )
}
