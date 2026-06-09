// Author:      Wajid Ali Chaudhry
// Description: Add Expense page — posts a new expense via
//              POST /expenses then returns to the dashboard.

import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useMutation, useQueryClient } from '@tanstack/react-query'
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

// Post a new expense; returns the created expense object
async function createExpense(data: ExpenseFormData) {
    const res = await api.post('/expenses', {
        title: data.title,
        amount: Number(data.amount),
        category: data.category,
        date: data.date,
    })
    return res.data
}

// --- Component ---

// Add Expense page — wraps ExpenseForm in create mode
export default function AddExpensePage() {
    const navigate = useNavigate()
    const queryClient = useQueryClient()
    const [mutationError, setMutationError] = useState('')

    const mutation = useMutation({
        mutationFn: createExpense,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['expenses'] })
            queryClient.invalidateQueries({ queryKey: ['summary'] })
            navigate('/app')
        },
        onError: (err: unknown) => {
            setMutationError(extractError(err))
        },
    })

    // --- Render ---

    return (
        <div className="expense-page">
            <h1 className="expense-page-title">Add Expense</h1>
            <ExpenseForm
                isPending={mutation.isPending}
                error={mutationError}
                onSubmit={(data) => {
                    setMutationError('')
                    mutation.mutate(data)
                }}
            />
        </div>
    )
}
