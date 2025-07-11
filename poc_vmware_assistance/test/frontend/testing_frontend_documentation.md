# Documentación de Pruebas Frontend – VMware Assistant

## Descripción General

**Nombre del Proyecto:** VMware Assistant  
**Fecha de Pruebas:** 6 de julio de 2025  
**Autor:** Ignacio Devita  
**Versión:** 1.0 (MVP)

**Objetivo de la Prueba:**  
Validar las funcionalidades principales de la interfaz de chat, asegurando el renderizado correcto, la interacción del usuario y la integración con el sistema de diseño.

---

## Casos de Prueba para Componentes de Chat

| **Componente**   | **Funcionalidad**                                                    | **Resultado** |
|------------------|---------------------------------------------------------------------|--------------|
| `ChatMessage`    | Renderiza mensajes de usuario y asistente con estilos/avatares correctos | PASS         |
| `ChatMessage`    | Copia el texto del mensaje al portapapeles al hacer clic en el botón    | PASS         |
| `ChatInput`      | Permite escribir y enviar un mensaje                                   | PASS         |
| `ChatInput`      | Limpia el input después de enviar                                      | PASS         |
| `ChatInput`      | Deshabilita input y botón durante la carga                            | PASS         |
| `ChatInput`      | Muestra contador de caracteres si está habilitado                     | PASS         |

---

## Ejemplo de Prueba: ChatMessage

- **Prueba:** Renderiza un mensaje de usuario con el estilo correcto
- **Pasos:** Renderizar `ChatMessage` con `isUser={true}` y verificar el texto, sin avatar.
- **Resultado Esperado:** El mensaje es visible, no hay avatar presente.

---

## Ejemplo de Prueba: ChatInput

- **Prueba:** Permite escribir y enviar un mensaje
- **Pasos:** Escribir en el input, enviar y verificar que se llama al callback.
- **Resultado Esperado:** `onSendMessage` es llamado con el mensaje correcto.

---

## Consideraciones Técnicas

- Las pruebas están escritas usando React Testing Library y Jest.
- Para ejecutar las pruebas, instala `@testing-library/react` y `@testing-library/jest-dom` como dependencias de desarrollo.
- Las pruebas cubren renderizado, interacción de usuario y gestión de estado para la UI de chat. 