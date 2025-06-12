import { Input, IconButton, Flex } from '@chakra-ui/react'
import { FaPaperPlane } from 'react-icons/fa'
import { useState } from 'react'

const ChatInput = ({ onSendMessage, isLoading }) => {
  const [message, setMessage] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (message.trim() && !isLoading) {
      onSendMessage(message)
      setMessage('')
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <Flex p={4} borderTop="1px" borderColor="gray.200">
        <Input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Escribe tu consulta sobre la infraestructura VMware..."
          size="lg"
          mr={2}
          bg="white"
          isDisabled={isLoading}
          _focus={{
            borderColor: 'blue.500',
            boxShadow: '0 0 0 1px var(--chakra-colors-blue-500)',
          }}
        />
        <IconButton
          type="submit"
          colorScheme="blue"
          aria-label="Enviar mensaje"
          icon={<FaPaperPlane />}
          size="lg"
          isLoading={isLoading}
          isDisabled={isLoading || !message.trim()}
        />
      </Flex>
    </form>
  )
}

export default ChatInput 