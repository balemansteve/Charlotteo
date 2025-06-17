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
  IconButton,
  useColorMode,
} from '@chakra-ui/react'
import { FaMoon, FaSun, FaRedo } from 'react-icons/fa'
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
  const { colorMode, toggleColorMode } = useColorMode()

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async (message) => {
    if (!message.trim()) return

    setMessages((prev) => [...prev, { text: message, isUser: true }])
    setIsLoading(true)

    try {
      // reemplazar la url con el endpoint de fastapi
      const response = await axios.post('http://localhost:8000/api/v1/prompt/', {
        message,
      })

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

  const handleResetChat = () => {
    setMessages([
      {
        text: 'Hola, soy tu asistente virtual. ¿En qué puedo ayudarte?',
        isUser: false,
      },
    ])
  }

  return (
    <Container maxW="container.xl" h="100vh" py={10}>
      <VStack h="full" spacing={4}>
        <Flex w="full" justify="space-between" align="center">
          <Box textAlign="center" flex={1}>
            <Heading size="lg" color={colorMode === 'dark' ? 'blue.300' : 'blue.600'}>
              VMware Assistance
            </Heading>
            <Text color={colorMode === 'dark' ? 'gray.400' : 'gray.600'}>
              Diagnóstico inteligente de infraestructura virtual
            </Text>
          </Box>
          <Flex gap={2}>
            <IconButton
              icon={colorMode === 'dark' ? <FaSun /> : <FaMoon />}
              onClick={toggleColorMode}
              aria-label="Cambiar tema"
              colorScheme="blue"
              variant="solid"
              borderRadius="md"
              size="lg"
              bg="#2196f3"
              _hover={{ bg: '#1976d2' }}
              _active={{ bg: '#1565c0' }}
              color="white"
            />
            <IconButton
              icon={<FaRedo />}
              onClick={handleResetChat}
              aria-label="Reiniciar chat"
              colorScheme="blue"
              variant="solid"
              borderRadius="md"
              size="lg"
              bg="#2196f3"
              _hover={{ bg: '#1976d2' }}
              _active={{ bg: '#1565c0' }}
              color="white"
            />
          </Flex>
        </Flex>

        <Box
          flex={1}
          w="full"
          bg={colorMode === 'dark' ? '#232328' : 'white'}
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
                background: colorMode === 'dark' ? 'gray.600' : 'gray.200',
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
                  <Spinner color={colorMode === 'dark' ? 'blue.300' : 'blue.500'} />
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
