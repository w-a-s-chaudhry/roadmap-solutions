// Author:      Wajid Ali Chaudhry
// Description: Expenses page — full filterable, sortable, paginated
//              list of all expenses with range presets and totals.

import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import api from '@/api/api'

// --- Types ---

interface ExpenseItem {
    id: number
    title: string
    amount: number
    category: string
    date: string
}

interface PaginatedExpenses {
    items: ExpenseItem[]
    total: number
    page: number
    size: number
    pages: number
}

// --- Constants ---

const RANGE_PRESETS = [
    { label: 'Past week', value: 'past_week' },
    { label: 'Past month', value: 'past_month' },
    { label: 'Last 3 months', value: 'last_3_months' },
    { label: 'Custom', value: 'custom' },
] as const

const CATEGORIES = [
    'food', 'transport', 'entertainment',
    'housing', 'healthcare', 'other',
] as const

// --- Component ---

// Full expenses list with filters, sort, and pagination
export default function ExpensesPage() {
    const navigate = useNavigate()

    const [range, setRange] = useState('past_month')
    const [customStart, setCustomStart] = useState('')
    const [customEnd, setCustomEnd] = useState('')
    const [category, setCategory] = useState('')
    const [sort, setSort] = useState('date')
    const [order, setOrder] = useState('desc')
    const [page, setPage] = useState(1)

    // Fetch expenses with all active filters applied
    const query = useQuery<PaginatedExpenses>({
        queryKey: [
            'expenses-page', range, customStart, customEnd,
            category, sort, order, page,
        ],
        queryFn: async (): Promise<PaginatedExpenses> => {
            const params: Record<string, string | number> = {
                range, sort, order, page, size: 20,
            }
            if (category) params.category = category
            if (range === 'custom') {
                params.start_date = customStart
                params.end_date = customEnd
            }
            const res = await api.get('/expenses', { params })
            return res.data
        },
    })


    // Derived totals for the "Showing N · $total" line
    const items = query.data?.items ?? []
    const periodTotal =
        '£' + items
            .reduce((acc, item) => acc + Number(item.amount), 0)
            .toFixed(2)

    // --- Render ---

    return (
        <div className="expenses-page">

            {/* Header */}
            <div className="expenses-header">
                <h1 className="expenses-title">Expenses</h1>
            </div>

            {/* Range preset buttons */}
            <div className="range-buttons">
                {RANGE_PRESETS.map(({ label, value }) => (
                    <button
                        key={value}
                        className={
                            `range-btn${range === value ? ' active' : ''}`
                        }
                        onClick={() => {
                            setRange(value)
                            setPage(1)
                        }}
                    >
                        {label}
                    </button>
                ))}
            </div>

            {/* Custom date inputs — only visible when range is "custom" */}
            {range === 'custom' && (
                <div className="expenses-custom-dates">
                    <div className="form-field">
                        <label htmlFor="start">From</label>
                        <input
                            id="start"
                            type="date"
                            value={customStart}
                            onChange={(e) => {
                                setCustomStart(e.target.value)
                                setPage(1)
                            }}
                        />
                    </div>
                    <div className="form-field">
                        <label htmlFor="end">To</label>
                        <input
                            id="end"
                            type="date"
                            value={customEnd}
                            onChange={(e) => {
                                setCustomEnd(e.target.value)
                                setPage(1)
                            }}
                        />
                    </div>
                </div>
            )}

            {/* Filter / sort controls */}
            <div className="expenses-filters">
                <select
                    className="filter-select"
                    value={category}
                    onChange={(e) => {
                        setCategory(e.target.value)
                        setPage(1)
                    }}
                >
                    <option value="">All categories</option>
                    {CATEGORIES.map((cat) => (
                        <option key={cat} value={cat}>
                            {cat.charAt(0).toUpperCase() + cat.slice(1)}
                        </option>
                    ))}
                </select>

                <select
                    className="filter-select"
                    value={`${sort}-${order}`}
                    onChange={(e) => {
                        const [s, o] = e.target.value.split('-')
                        setSort(s)
                        setOrder(o)
                        setPage(1)
                    }}
                >
                    <option value="date-desc">Date (newest)</option>
                    <option value="date-asc">Date (oldest)</option>
                    <option value="amount-desc">Amount (high)</option>
                    <option value="amount-asc">Amount (low)</option>
                </select>
            </div>

            {/* Summary line */}
            {query.data && (
                <p className="expenses-summary">
                    {query.data.total} expense
                    {query.data.total !== 1 ? 's' : ''} found
                    &nbsp;·&nbsp;
                    page total: {periodTotal}
                </p>
            )}

            {/* Expense list */}
            <div className="expense-list">
                {query.isLoading && (
                    <p className="page-loading">Loading…</p>
                )}
                {query.isError && (
                    <p className="page-error">Failed to load expenses.</p>
                )}
                {!query.isLoading && !query.isError && items.map((expense) => (
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
                                {`£${Number(expense.amount).toFixed(2)}`}
                            </p>
                        </div>
                    </div>
                ))}
                {!query.isLoading && !query.isError && items.length === 0 && (
                    <p className="expense-empty">No expenses in this period.</p>
                )}
            </div>

            {/* Pagination */}
            {query.data && query.data.pages > 1 && (
                <div className="expenses-pagination">
                    <button
                        className="page-btn"
                        disabled={page === 1}
                        onClick={() => setPage(page - 1)}
                    >
                        ← Prev
                    </button>
                    <span className="page-info">
                        {page} / {query.data.pages}
                    </span>
                    <button
                        className="page-btn"
                        disabled={page === query.data.pages}
                        onClick={() => setPage(page + 1)}
                    >
                        Next →
                    </button>
                </div>
            )}

        </div>
    )
}
