import { useState, useRef, useEffect } from 'react'
import {
  Box,
  Container,
  Heading,
  VStack,
  useToast,
  Flex,
  Text,
  Spinner,
} from '@chakra-ui/react'
import ChatMessage from './components/ChatMessage'
import ChatInput from './components/ChatInput'
import axios from 'axios'

function App() {
  const [messages, setMessages] = useState([
    {
      text: 'Hola, soy tu asistente virtual. ¿En qué puedo ayudarte?',
      isUser: false,
    },
  ])
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)
  const toast = useToast()

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async (message) => {
    if (!message.trim()) return

    // Agregar mensaje del usuario
    setMessages((prev) => [...prev, { text: message, isUser: true }])
    setIsLoading(true)

    try {
      // Aquí deberás reemplazar la URL con tu endpoint de FastAPI
      const response = await axios.post('http://localhost:8000/chat', {
        message,
      })

      // Agregar respuesta del asistente
      setMessages((prev) => [
        ...prev,
        { text: response.data.response, isUser: false, name: 'VMware Assistance' },
      ])
    } catch (error) {
      console.error('Error:', error)
      toast({
        title: 'Error',
        description: error.response?.data?.detail || 'No se pudo obtener respuesta del servidor',
        status: 'error',
        duration: 5000,
        isClosable: true,
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Container maxW="container.xl" h="100vh" py={4}>
      <VStack h="full" spacing={4}>
        <Box w="full" textAlign="center">
          <Heading size="lg" color="blue.600">
            VMware Assistance
          </Heading>
          <Text color="gray.600">
            Diagnóstico inteligente de infraestructura virtual
          </Text>
        </Box>

        <Box
          flex={1}
          w="full"
          bg="white"
          borderRadius="lg"
          boxShadow="md"
          overflow="hidden"
          display="flex"
          flexDirection="column"
        >
          <Box
            flex={1}
            overflowY="auto"
            p={4}
            css={{
              '&::-webkit-scrollbar': {
                width: '4px',
              },
              '&::-webkit-scrollbar-track': {
                width: '6px',
              },
              '&::-webkit-scrollbar-thumb': {
                background: 'gray.200',
                borderRadius: '24px',
              },
            }}
          >
            <VStack spacing={4} align="stretch">
              {messages.map((msg, index) => (
                <ChatMessage
                  key={index}
                  message={msg.text}
                  isUser={msg.isUser}
                />
              ))}
              {isLoading && (
                <Flex justify="center" my={4}>
                  <Spinner color="blue.500" />
                </Flex>
              )}
              <div ref={messagesEndRef} />
            </VStack>
          </Box>

          <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
        </Box>
      </VStack>
    </Container>
  )
}

export default App
