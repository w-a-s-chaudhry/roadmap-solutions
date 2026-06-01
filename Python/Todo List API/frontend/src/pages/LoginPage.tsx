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
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Label } from '../components/ui/label'
import {
	Card,
	CardContent,
	CardHeader,
	CardTitle,
} from '../components/ui/card'

// --- Validation schema ---


const loginSchema = z.object({
	email: z.string().email("Invalid email"),
	password: z.string().min(1, 'Password is required')
})

// Infer the TypeScript type from the schema so you never type it twice.
type LoginFormData = z.infer<typeof loginSchema>

// --- Component ---

// Renders the login form and handles submission
export default function LoginPage() {
	const { login } = useAuth()
	const navigate = useNavigate()
	const [serverError, setServerError] = useState('')
	const { register, handleSubmit, formState: { errors } } = useForm<LoginFormData>({ resolver: zodResolver(loginSchema) })

	// Submits credentials to the backend and stores the token on success
	async function onSubmit(data: LoginFormData) {
		setServerError('')

		try {
			const res = await api.post('/auth/login', {
				email: data.email,
				password: data.password,
			})

			login(res.data.access_token)
			navigate('/todos')
		} catch (err: any) {
			const detail = err?.response?.data?.detail
			const msg = typeof detail === 'string'
				? detail
				: Array.isArray(detail)
					? detail.map((e: any) => e.msg).join(', ')
					: 'Login failed'
			setServerError(msg)

		}
	}

	// --- Render ---

	return (
		<div className="min-h-screen flex items-center justify-center p-4">
			<Card className="w-full max-w-sm">
				<CardHeader>
					<CardTitle>Log in</CardTitle>
				</CardHeader>
				<CardContent>
					{/* handleSubmit validates first, then calls onSubmit */}
					<form
						onSubmit={handleSubmit(onSubmit)}
						className="flex flex-col gap-4"
					>
						<div className="flex flex-col gap-1">
							<Label htmlFor="email">Email</Label>
							<Input
								id="email"
								type="email"
								placeholder="you@example.com"
								{...register('email')}
							/>
							{errors.email?.message && (
								<p className="text-sm text-red-500">
									{errors.email.message}
								</p>
							)}
						</div>

						<div className="flex flex-col gap-1">
							<Label htmlFor="password">Password</Label>
							<Input
								id="password"
								type="password"
								placeholder="••••••••"
								{...register('password')}
							/>
							{errors.password?.message && (
								<p className="text-sm text-red-500">
									{errors.password.message}
								</p>
							)}
						</div>

						{/* Server-level error (wrong credentials, etc.) */}
						{serverError && (
							<p className="text-sm text-red-500">{serverError}</p>
						)}

						<Button type="submit" className="w-full">
							Log in
						</Button>
					</form>

					<p className="mt-4 text-sm text-center">
						No account?{' '}
						<Link to="/register" className="underline">
							Register
						</Link>
					</p>
				</CardContent>
			</Card>
		</div>
	)
}
