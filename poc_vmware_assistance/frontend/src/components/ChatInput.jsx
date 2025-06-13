import { Input, IconButton, Flex, Text } from '@chakra-ui/react'
import { FaPaperPlane } from 'react-icons/fa'
import { useState } from 'react'

const MAX_CHARS = 300

const ChatInput = ({ onSendMessage, isLoading }) => {
  const [message, setMessage] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (message.trim() && !isLoading && message.length <= MAX_CHARS) {
      onSendMessage(message)
      setMessage('')
    }
  }

  const handleChange = (e) => {
    const newMessage = e.target.value
    if (newMessage.length <= MAX_CHARS) {
      setMessage(newMessage)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <Flex p={4} borderTop="1px" borderColor="gray.200" direction="column">
        <Flex>
          <Input
            value={message}
            onChange={handleChange}
            placeholder="Escribe tu consulta sobre la infraestructura VMware..."
            size="lg"
            mr={2}
            isDisabled={isLoading}
            bg={document.body.classList.contains('chakra-ui-dark') ? '#2D3748' : 'white'}
            color={document.body.classList.contains('chakra-ui-dark') ? 'white' : 'black'}
            _placeholder={{ color: document.body.classList.contains('chakra-ui-dark') ? 'gray.300' : 'gray.500' }}
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
            isLoading={isLoading}
            isDisabled={isLoading || !message.trim() || message.length > MAX_CHARS}
            bg="blue.500"
            color="white"
            _hover={{ bg: "blue.600" }}
            _active={{ bg: "blue.700" }}
            _dark={{
              bg: "blue.500",
              color: "white",
              _hover: { bg: "blue.600" },
              _active: { bg: "blue.700" }
            }}
          />
        </Flex>
        <Text
          fontSize="sm"
          color={message.length > MAX_CHARS ? 'red.500' : 'gray.500'}
          mt={1}
          textAlign="right"
        >
          {message.length}/{MAX_CHARS}
        </Text>
      </Flex>
    </form>
  )
}

export default ChatInput 