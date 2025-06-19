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
import { motion, AnimatePresence } from 'framer-motion'

function App() {
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)
  const toast = useToast()
  const { colorMode, toggleColorMode } = useColorMode()
  const [chatOpen, setChatOpen] = useState(false)
  const [firstMessage, setFirstMessage] = useState("")
  const [isTransitioning, setIsTransitioning] = useState(false)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    if (isTransitioning || isLoading) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = 'auto'
    }
    return () => {
      document.body.style.overflow = 'auto'
    }
  }, [isTransitioning, isLoading])

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
        text: '¡Hola! Consulta aquí cualquier duda sobre tu infraestructura VMware.',
        isUser: false,
      },
    ])
    setChatOpen(false)
    setFirstMessage("")
  }

  const bgMain = colorMode === 'dark' ? '#18181A' : '#fff'
  const bgInput = colorMode === 'dark' ? '#232328' : '#f5f5f5'
  const textColor = colorMode === 'dark' ? 'white' : '#232328'
  const subtitleColor = colorMode === 'dark' ? 'gray.400' : 'gray.600'

  return (
    <Box minH="100vh" minW="100vw" bg="#18181A" position="relative">
      {/* INTERFAZ INICIAL: solo título, subtítulo e input centrados verticalmente, con animación */}
      <AnimatePresence>
        {!chatOpen && (
          <motion.div
            key="inicio"
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -40 }}
            transition={{ duration: 0.5, ease: 'easeInOut' }}
            style={{ width: '100%', background: bgMain }}
            onAnimationStart={() => setIsTransitioning(true)}
            onAnimationComplete={() => setIsTransitioning(false)}
          >
            <Box minH="100vh" display="flex" flexDirection="column" alignItems="center" justifyContent="center" bg={bgMain}>
              <Heading size="2xl" color="blue.300" letterSpacing="tight" mb={2}>
                VMware Assistance
              </Heading>
              <Text color={subtitleColor} fontSize="xl" mb={8}>
                Diagnóstico inteligente de infraestructura virtual
              </Text>
              <motion.div
                initial={{ opacity: 0, y: 40 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, ease: 'easeInOut' }}
                style={{ width: '100%', background: 'transparent' }}
              >
                <Box
                  w="100%"
                  maxW="800px"
                  mx="auto"
                  display="flex"
                  alignItems="center"
                  bg={bgInput}
                  borderRadius="xl"
                  p={2}
                  boxShadow="none"
                >
                  <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} placeholder="Escribe tu consulta..." showCounter={false} modernStyle={true} hideBox={true} inputBg={bgInput} fullWidthInput={true} inputColor={textColor} />
                </Box>
              </motion.div>
              {/* Botones arriba a la derecha SIEMPRE visibles */}
              <Box position="absolute" top={6} right={10} zIndex={20} display="flex" alignItems="center" gap={2}>
                <IconButton
                  icon={<FaRedo />}
                  onClick={handleResetChat}
                  aria-label="Reiniciar chat"
                  colorScheme="blue"
                  variant="solid"
                  borderRadius="full"
                  size="lg"
                  bg="#2196f3"
                  _hover={{ bg: '#1976d2' }}
                  _active={{ bg: '#1565c0' }}
                  color="white"
                  boxShadow="0 2px 8px 0 rgba(0,0,0,0.10)"
                  mt={-2}
                />
                <IconButton
                  icon={colorMode === 'dark' ? <FaSun /> : <FaMoon />}
                  onClick={toggleColorMode}
                  aria-label="Cambiar tema"
                  colorScheme="blue"
                  variant="solid"
                  borderRadius="full"
                  size="lg"
                  bg="#2196f3"
                  _hover={{ bg: '#1976d2' }}
                  _active={{ bg: '#1565c0' }}
                  color="white"
                  mt={-2}
                />
              </Box>
            </Box>
          </motion.div>
        )}
      </AnimatePresence>
      {/* INTERFAZ DE CHAT: header arriba, historial e input centrados, con transición suave */}
      <AnimatePresence>
        {chatOpen && (
          <motion.div
            key="chat"
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -40 }}
            transition={{ duration: 0.5, ease: 'easeInOut' }}
            style={{ width: '100%', background: bgMain }}
            onAnimationStart={() => setIsTransitioning(true)}
            onAnimationComplete={() => setIsTransitioning(false)}
          >
            <Box minH="100vh" display="flex" flexDirection="column" alignItems="center" justifyContent="flex-start" bg={bgMain}>
              {/* Header arriba */}
              <Box w="100%" px={12} pt={8} pb={2} display="flex" alignItems="flex-start" justifyContent="space-between" bg={bgMain}>
                <Box>
                  <Heading size="2xl" color="blue.300" letterSpacing="tight">
                    VMware Assistance
                  </Heading>
                  <Text color={subtitleColor} fontSize="xl" mt={2}>
                    Diagnóstico inteligente de infraestructura virtual
                  </Text>
                </Box>
                <Box display="flex" alignItems="center" gap={2}>
                  <IconButton
                    icon={<FaRedo />}
                    onClick={handleResetChat}
                    aria-label="Reiniciar chat"
                    colorScheme="blue"
                    variant="solid"
                    borderRadius="full"
                    size="lg"
                    bg="#2196f3"
                    _hover={{ bg: '#1976d2' }}
                    _active={{ bg: '#1565c0' }}
                    color="white"
                    boxShadow="0 2px 8px 0 rgba(0,0,0,0.10)"
                    mt={-2}
                  />
                  <IconButton
                    icon={colorMode === 'dark' ? <FaSun /> : <FaMoon />}
                    onClick={toggleColorMode}
                    aria-label="Cambiar tema"
                    colorScheme="blue"
                    variant="solid"
                    borderRadius="full"
                    size="lg"
                    bg="#2196f3"
                    _hover={{ bg: '#1976d2' }}
                    _active={{ bg: '#1565c0' }}
                    color="white"
                    mt={-2}
                  />
                </Box>
              </Box>
              {/* Chat centrado */}
              <Box
                w="100%"
                maxW="800px"
                mx="auto"
                flex={1}
                display="flex"
                flexDirection="column"
                justifyContent="center"
                alignItems="center"
                pt={8}
                bg={bgMain}
              >
                <Box
                  w="100%"
                  maxH="60vh"
                  overflowY="auto"
                  css={{
                    '::-webkit-scrollbar': {
                      width: '6px',
                    },
                    '::-webkit-scrollbar-thumb': {
                      background: colorMode === 'dark' ? '#232328' : '#bbb',
                      borderRadius: '8px',
                    },
                    '::-webkit-scrollbar-track': {
                      background: 'transparent',
                    },
                  }}
                >
                  <VStack spacing={4} align="stretch" w="100%">
                    {messages.map((msg, index) => (
                      <ChatMessage
                        key={index}
                        message={msg.text}
                        isUser={msg.isUser}
                      />
                    ))}
                    {isLoading && (
                      <Flex justify="center" my={4}>
                        <Spinner color="blue.300" />
                      </Flex>
                    )}
                    <div ref={messagesEndRef} />
                  </VStack>
                </Box>
                <Box
                  w="100%"
                  maxW="800px"
                  mx="auto"
                  mt={8}
                  display="flex"
                  alignItems="center"
                  bg={bgInput}
                  borderRadius="xl"
                  p={2}
                  boxShadow="none"
                >
                  <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} placeholder="Escribe tu consulta..." showCounter={false} modernStyle={true} hideBox={true} inputBg={bgInput} fullWidthInput={true} inputColor={textColor} />
                </Box>
              </Box>
            </Box>
          </motion.div>
        )}
      </AnimatePresence>
    </Box>
  )
}

export default App
