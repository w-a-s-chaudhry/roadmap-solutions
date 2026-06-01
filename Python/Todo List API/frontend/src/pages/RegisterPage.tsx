// Author:      Wajid Ali Chaudhry
// Description: Register page — email + password form, posts to
//              /auth/register then redirects to /.

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { useNavigate, Link } from 'react-router-dom'
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

const registerSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  confirmPassword: z.string(),
}).refine(
  (data) => data.password === data.confirmPassword,
  { message: "Passwords don't match", path: ['confirmPassword'] }
)

type RegisterFormData = z.infer<typeof registerSchema>

// --- Component ---

// Renders the register form and handles submission
export default function RegisterPage() {
  const navigate = useNavigate()
  const [serverError, setServerError] = useState('')
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormData>({ resolver: zodResolver(registerSchema) })

  // Submits new account details to the backend, redirects to login on success
  async function onSubmit(data: RegisterFormData) {
    setServerError('')

    try {
      await api.post('/auth/register', {
        email: data.email,
        password: data.password
      })
      navigate('/')
    } catch (err: any) {
      const msg = err?.response?.data?.detail ?? 'Registration Failed'
      setServerError(msg)
    }
  }

  // --- Render ---

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <Card className="w-full max-w-sm">
        <CardHeader>
          <CardTitle>Create account</CardTitle>
        </CardHeader>
        <CardContent>
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

            <div className="flex flex-col gap-1">
              <Label htmlFor="confirmPassword">Confirm password</Label>
              <Input
                id="confirmPassword"
                type="password"
                placeholder="••••••••"
                {...register("confirmPassword")}
              />
              {errors.confirmPassword?.message && (
                <p className="text-sm text-red-500">
                  {errors.confirmPassword.message}
                </p>
              )}
            </div>

            {serverError && (
              <p className="text-sm text-red-500">{serverError}</p>
            )}

            <Button type="submit" className="w-full">
              Create account
            </Button>
          </form>

          <p className="mt-4 text-sm text-center">
            Already have an account?{' '}
            <Link to="/" className="underline">
              Log in
            </Link>
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
