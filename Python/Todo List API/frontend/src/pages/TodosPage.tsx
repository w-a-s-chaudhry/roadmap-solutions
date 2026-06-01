// Author:      Wajid Ali Chaudhry
// Description: Todos page — list, create, toggle done, delete.

import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import {
  useQuery, useMutation, useQueryClient,
} from '@tanstack/react-query'
import { useAuth } from '../context/AuthContext'
import api from '../api/api'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Label } from '../components/ui/label'
import {
  Card, CardContent, CardHeader, CardTitle,
} from '../components/ui/card'

// --- Types ---
interface Todo {
  id: number
  title: string
  description: string | null
  done: boolean
  priority: number
  created_at: string
  updated_at: string
  owner_id: number
}

// --- Validation schema ---
const createTodoSchema = z.object({
  title: z.string().min(1, "Title is required")
})
type CreateTodoFormData = z.infer<typeof createTodoSchema>

// --- API calls ---

async function fetchTodos(): Promise<Todo[]> {
  const res = await api.get("/todos")

  return res.data.items

}

// --- Component ---

// Renders the todo list and the create-todo form
export default function TodosPage() {
  const { logout } = useAuth()
  const queryClient = useQueryClient()

  const {
    register, handleSubmit, reset,
    formState: { errors },
  } = useForm<CreateTodoFormData>({
    resolver: zodResolver(createTodoSchema),
  })

  const { data: todos, isLoading, isError } = useQuery({
    queryKey: ['todos'],
    queryFn: fetchTodos,
  })

  const createMutation = useMutation({
    mutationFn: async (data: CreateTodoFormData) => await api.post("/todos", data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["todos"] })
      reset()
    }
  })
  const toggleMutation = useMutation({
    mutationFn: (todo: Todo) => api.patch(`/todos/${todo.id}`, { done: !todo.done }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["todos"] })
    }
  })

  const deleteMutation = useMutation({
    mutationFn: (id: number) => api.delete(`/todos/${id}`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['todos'] })
  })


  async function onSubmit(data: CreateTodoFormData) {
    createMutation.mutate(data)
  }

  // --- Render ---

  return (
    <div className="max-w-xl mx-auto p-6 flex flex-col gap-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">My Todos</h1>
        <Button variant="outline" onClick={logout}>
          Log out
        </Button>
      </div>

      <Card>
        <CardHeader><CardTitle>Add a todo</CardTitle></CardHeader>
        <CardContent>
          <form
            onSubmit={handleSubmit(onSubmit)}
            className="flex flex-col gap-3"
          >
            <div className="flex flex-col gap-1">
              <Label htmlFor="title">Title</Label>
              <Input
                id="title"
                placeholder="What needs doing?"
                {...register('title')}
              />
              {errors.title?.message && (
                <p className="text-sm text-red-500">
                  {errors.title.message}
                </p>
              )}
            </div>
            <Button type="submit" disabled={createMutation.isPending}>
              {createMutation.isPending ? 'Adding...' : 'Add'}
            </Button>
            {createMutation.isError && (
              <p className="text-sm text-red-500">
                Failed to create todo. Try again.
              </p>
            )}
          </form>
        </CardContent>
      </Card>
      {isLoading && <p>Loading...</p>}
      {isError && <p className='text-red-500'>Failed to load todos</p>}
      {todos && todos.length === 0 && (
        <p className='text-muted-foreground'>No Todos Yet</p>
      )}
      {todos && todos.map((todo) => (
        <Card key={todo.id}>
          <CardContent className="flex items-center gap-3 py-3">
            <span className={
              todo.done
                ? 'line-through text-muted-foreground flex-1'
                : 'flex-1'
            }>
              {todo.title}
            </span>
            <input
              type="checkbox"
              checked={todo.done}
              onChange={() => toggleMutation.mutate(todo)}
              disabled={toggleMutation.isPending}
            />
            <Button
              variant="ghost"
              onClick={() => deleteMutation.mutate(todo.id)}
              disabled={deleteMutation.isPending}
            >
              Delete
            </Button>
          </CardContent>
        </Card>
      ))
      }


    </div >
  )
}
