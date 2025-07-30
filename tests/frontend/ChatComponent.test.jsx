// ChatComponent.test.jsx
// Documentación y casos de prueba para los componentes ChatMessage y ChatInput
// Autor: Ignacio Devita
// Fecha: 6 de julio de 2025

import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import '@testing-library/jest-dom'
import ChatMessage from '../../frontend/src/components/ChatMessage'
import ChatInput from '../../frontend/src/components/ChatInput'

// Plan de pruebas: ChatMessage
// 1. Debe renderizar el mensaje del usuario con los estilos correctos
// 2. Debe copiar el texto del mensaje al portapapeles al hacer clic en el botón de copiar

describe('ChatMessage', () => {
  it('renderiza un mensaje de usuario con el estilo correcto', () => {
    render(<ChatMessage message={{ text: '¡Hola!', isUser: true }} isUser={true} />)
    expect(screen.getByText('¡Hola!')).toBeInTheDocument()
  })
  it('copia el texto del mensaje al portapapeles al hacer clic en el botón de copiar', () => {
    // Mock del portapapeles
    Object.assign(navigator, {
      clipboard: { writeText: jest.fn() }
    })
    render(<ChatMessage message={{ text: '¡Cópia esto!' }} isUser={true} />)
    const copyBtn = screen.getByLabelText('Copiar mensaje')
    fireEvent.click(copyBtn)
    expect(navigator.clipboard.writeText).toHaveBeenCalledWith('¡Cópia esto!')
  })
})

// Plan de pruebas: ChatInput
// 1. Debe permitir escribir y enviar un mensaje
// 2. Debe limpiar el input después de enviar
// 3. Debe deshabilitar el input y el botón durante la carga
// 4. Debe mostrar el contador de caracteres si está habilitado

describe('ChatInput', () => {
  it('permite escribir y enviar un mensaje', () => {
    const onSendMessage = jest.fn()
    render(<ChatInput onSendMessage={onSendMessage} isLoading={false} />)
    const input = screen.getByPlaceholderText('Escribe tu consulta...')
    fireEvent.change(input, { target: { value: 'Mensaje de prueba' } })
    fireEvent.submit(input)
    expect(onSendMessage).toHaveBeenCalledWith('Mensaje de prueba')
  })

  it('limpia el input después de enviar', () => {
    const onSendMessage = jest.fn()
    render(<ChatInput onSendMessage={onSendMessage} isLoading={false} />)
    const input = screen.getByPlaceholderText('Escribe tu consulta...')
    fireEvent.change(input, { target: { value: 'Límpiame' } })
    fireEvent.submit(input)
    expect(input.value).toBe('')
  })

  it('deshabilita el input y el botón durante la carga', () => {
    render(<ChatInput onSendMessage={() => {}} isLoading={true} />)
    const input = screen.getByPlaceholderText('Escribe tu consulta...')
    expect(input).toBeDisabled()
    const button = screen.getByRole('button')
    expect(button).toBeDisabled()
  })

  it('muestra el contador de caracteres si está habilitado', () => {
    render(<ChatInput onSendMessage={() => {}} isLoading={false} showCounter={true} />)
    expect(screen.getByText('0/300')).toBeInTheDocument()
  })
})
