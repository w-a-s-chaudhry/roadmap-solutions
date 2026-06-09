// Author:      Wajid Ali Chaudhry
// Description: Edit Expense page — prefills ExpenseForm from the
//              fetched expense; PATCH on save, DELETE on delete.

import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
    useQuery,
    useMutation,
    useQueryClient,
} from '@tanstack/react-query'
import api from '@/api/api'
import ExpenseForm, {
    type ExpenseFormData,
} from '@/components/ExpenseForm'

// --- Helpers ---

// Extract a readable message from an axios error response
function extractError(err: unknown): string {
    const detail = (err as any)?.response?.data?.detail
    if (typeof detail === 'string') return detail
    if (Array.isArray(detail)) return detail.map((e: any) => e.msg).join(', ')
    return 'Something went wrong'
}

// --- API ---

// Fetch a single expense by id
async function fetchExpense(id: string) {
    const res = await api.get(`/expenses/${id}`)
    return res.data
}

// Patch (partial update) an existing expense
async function updateExpense(id: string, data: ExpenseFormData) {
    const res = await api.patch(`/expenses/${id}`, {
        title: data.title,
        amount: Number(data.amount),
        category: data.category,
        date: data.date,
    })
    return res.data
}

// Delete an expense by id (returns 204 — no body)
async function deleteExpense(id: string) {
    const res = await api.delete(`/expenses/${id}`)
    return res.data
}

// --- Component ---

// Edit Expense page — wraps ExpenseForm in edit mode
export default function EditExpensePage() {
    const { id } = useParams<{ id: string }>()
    const navigate = useNavigate()
    const queryClient = useQueryClient()
    const [mutationError, setMutationError] = useState('')

    const expenseQuery = useQuery({
        queryKey: ['expense', id],
        queryFn: () => fetchExpense(id!),
    })

    const updateMutation = useMutation({
        mutationFn: (data: ExpenseFormData) => updateExpense(id!, data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['expenses'] })
            queryClient.invalidateQueries({ queryKey: ['summary'] })
            queryClient.invalidateQueries({ queryKey: ['expense', id] })
            navigate('/app')
        },
        onError: (err: unknown) => {
            setMutationError(extractError(err))
        },
    })

    const deleteMutation = useMutation({
        mutationFn: () => deleteExpense(id!),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['expenses'] })
            queryClient.invalidateQueries({ queryKey: ['summary'] })
            navigate('/app')
        },
        onError: (err: unknown) => {
            setMutationError(extractError(err))
        },
    })

    if (expenseQuery.isLoading) return (
        <p className="page-loading">Loading expense…</p>
    )
    if (expenseQuery.isError) return (
        <p className="page-error">Expense not found.</p>
    )

    const expense = expenseQuery.data

    // --- Render ---

    return (
        <div className="expense-page">
            <h1 className="expense-page-title">Edit Expense</h1>
            <ExpenseForm
                initialData={{
                    title: expense.title,
                    amount: String(expense.amount),
                    category: expense.category,
                    date: expense.date,
                }}
                isPending={
                    updateMutation.isPending || deleteMutation.isPending
                }
                error={mutationError}
                onSubmit={(data) => {
                    setMutationError('')
                    updateMutation.mutate(data)
                }}
                onDelete={() => {
                    setMutationError('')
                    deleteMutation.mutate()
                }}
            />
        </div>
    )
}
