// Author:      Wajid Ali Chaudhry
// Description: Dashboard — summary cards, range presets, recent
//              expenses list. Clicking a row opens the edit form.

import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import api from '@/api/api'

// --- Types ---

interface SummaryData {
    total_spent: number
    count: number
    top_category: string | null
}

interface ExpenseItem {
    id: number
    title: string
    amount: number
    category: string
    date: string
}

// --- Constants ---

const RANGE_PRESETS = [
    { label: 'Past week', value: 'past_week' },
    { label: 'Past month', value: 'past_month' },
    { label: 'Last 3 months', value: 'last_3_months' },
] as const

// --- Component ---

// Main dashboard view — summary cards + recent expenses
export default function DashboardPage() {
    const navigate = useNavigate()
    const [range, setRange] = useState<string>('past_month')

    // Fetch the three dashboard card values for the selected range
    const summaryQuery = useQuery<SummaryData>({
        queryKey: ['summary', range],
        queryFn: async () => {
            const res = await api.get(
                '/expenses/summary', { params: { range } }
            )
            return res.data
        },
    })

    // Fetch the five most recent expenses for the selected range
    const expensesQuery = useQuery<ExpenseItem[]>({
        queryKey: ['expenses', range],
        queryFn: async () => {
            const res = await api.get(
                '/expenses', { params: { range, size: 5 } }
            )
            return res.data.items
        },
    })

    if (summaryQuery.isLoading || expensesQuery.isLoading) return <p className="page-loading">Loading…</p>
    if (summaryQuery.isError || expensesQuery.isError) return <p className="page-error">Failed to load expenses.</p>

    // --- Render ---

    return (
        <div className="dashboard-page">

            {/* Header row */}
            <div className="dashboard-header">
                <h1 className="dashboard-title">Dashboard</h1>
                <button
                    className="dashboard-add-btn"
                    onClick={() => navigate('/app/expenses/new')}
                >
                    + Add expense
                </button>
            </div>

            {/* Range preset buttons */}
            <div className="range-buttons">
                {RANGE_PRESETS.map(({ label, value }) => (
                    <button
                        key={value}
                        className={
                            `range-btn${range === value ? ' active' : ''}`
                        }
                        onClick={() => setRange(value)}
                    >
                        {label}
                    </button>
                ))}
            </div>

            {/* Summary cards */}
            <div className="dashboard-cards">

                <div className="dashboard-card">
                    <p className="card-label">Total Spent</p>
                    <p className="card-value">
                        {summaryQuery.data != null
                            ? `£${Number(summaryQuery.data.total_spent).toFixed(2)}`
                            : '—'}
                    </p>
                </div>

                <div className="dashboard-card">
                    <p className="card-label">Top Category</p>
                    <p className="card-value">
                        {summaryQuery.data?.top_category ?? '—'}
                    </p>
                </div>

                <div className="dashboard-card">
                    <p className="card-label">Expenses</p>
                    <p className="card-value">
                        {summaryQuery.data?.count ?? '—'}
                    </p>
                </div>

            </div>

            {/* Recent expenses */}
            <div className="expense-list">
                <h2 className="expense-list-title">Recent expenses</h2>

                {(expensesQuery.data ?? []).map((expense) => (
                    <div
                        key={expense.id}
                        className="expense-row"
                        onClick={
                            () => navigate(`/app/expenses/${expense.id}`)
                        }
                    >
                        <div className="expense-row-left">
                            <p className="expense-title">
                                {expense.title}
                            </p>
                            <p className="expense-meta">
                                {expense.category} · {expense.date}
                            </p>
                        </div>
                        <div className="expense-row-right">
                            <p className="expense-amount">
                                {expense.amount != null
                                    ? `£${Number(expense.amount).toFixed(2)}` : '—'}
                            </p>
                        </div>
                    </div>
                ))}

                {expensesQuery.data?.length === 0 && (
                    <p className="expense-empty">
                        No expenses in this period.
                    </p>
                )}

            </div>

        </div>
    )
}
