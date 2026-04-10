import type { ReactNode } from 'react'

interface ActionButtonProps {
  children: ReactNode
  onClick: () => void
  disabled?: boolean
}

// Componente de botão reutilizável.
// Isso evita repetir <button> com a mesma estrutura várias vezes.
export function ActionButton({
  children,
  onClick,
  disabled = false,
}: ActionButtonProps) {
  return (
    <button onClick={onClick} disabled={disabled}>
      {children}
    </button>
  )
}