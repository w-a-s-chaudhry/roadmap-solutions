// Author:      Wajid Ali Chaudhry
// Description: Shared form for creating and editing an expense.
//              Add passes no initialData; Edit passes prefilled values.

import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

// --- Types ---

export interface ExpenseFormData {
    title: string
    amount: string
    category: string
    date: string
}

interface ExpenseFormProps {
    initialData?: ExpenseFormData
    onSubmit: (data: ExpenseFormData) => void
    onDelete?: () => void
    isPending: boolean
    error?: string
}

// --- Constants ---

const CATEGORIES = [
    'food', 'transport', 'entertainment',
    'housing', 'healthcare', 'other',
] as const

// --- Component ---

// Controlled form shared by Add and Edit pages
export default function ExpenseForm({
    initialData,
    onSubmit,
    onDelete,
    isPending,
    error,
}: ExpenseFormProps) {
    const navigate = useNavigate()

    const [title, setTitle] = useState(initialData?.title ?? '')
    const [amount, setAmount] = useState(initialData?.amount ?? '')
    const [category, setCategory] = useState(
        initialData?.category ?? ''
    )
    const [date, setDate] = useState(initialData?.date ?? '')

    // Collect state into one object and hand off to the parent
    function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
        e.preventDefault()

        onSubmit({ title, amount, category, date })
    }

    // --- Render ---

    return (
        <form className="expense-form" onSubmit={handleSubmit}>

            {/* Title */}
            <div className="form-field">
                <label htmlFor="ef-title">Title</label>
                <input
                    id="ef-title"
                    type="text"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    required
                />
            </div>

            {/* Amount */}
            <div className="form-field">
                <label htmlFor="ef-amount">Amount (£)</label>
                <input
                    id="ef-amount"
                    type="number"
                    step="0.01"
                    min="0.01"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    required
                />
            </div>

            {/* Category chips */}
            <div className="form-field">
                <label>Category</label>
                <div className="category-chips">
                    {CATEGORIES.map((cat) => (
                        <button
                            key={cat}
                            type="button"
                            className={
                                `category-chip${category === cat ? ' active' : ''
                                }`
                            }
                            onClick={() => setCategory(cat)}

                        >
                            {cat.charAt(0).toUpperCase() + cat.slice(1)}
                        </button>
                    ))}
                </div>
            </div>

            {/* Date */}
            <div className="form-field">
                <label htmlFor="ef-date">Date</label>
                <input
                    id="ef-date"
                    type="date"
                    value={date}
                    onChange={(e) => setDate(e.target.value)}
                    required
                />
            </div>

            {/* Mutation error */}
            {error && (
                <p className="field-error">{error}</p>
            )}

            {/* Action buttons */}
            <div className="form-actions">
                <button
                    type="submit"
                    className="form-save-btn"
                    disabled={isPending || !category}
                >
                    {isPending ? 'Saving…' : 'Save'}
                </button>
                <button
                    type="button"
                    className="form-discard-btn"
                    onClick={() => navigate(-1)}
                >
                    Discard
                </button>
                {onDelete && (
                    <button
                        type="button"
                        className="form-delete-btn"
                        disabled={isPending}
                        onClick={() => onDelete()}
                    >
                        Delete
                    </button>
                )}
            </div>

        </form >
    )
}
