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
  Button,
} from '@chakra-ui/react'
import { FaMoon, FaSun, FaSyncAlt } from 'react-icons/fa'
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

    if (!chatOpen) {
      setChatOpen(true)
      setFirstMessage(message)
    }

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
        name: 'VMware Assistance',
      },
    ])
  }

  const bgMain =
    colorMode === 'dark'
      ? 'radial-gradient(circle at 50% 50%, #2d2d2d 0%, #1E1E1E 80%)'
      : '#FFFFFF'
  const bgInput = colorMode === 'dark' ? '#2d2d2d' : '#f5f5f5'
  const textColor = colorMode === 'dark' ? '#FFFFFF' : '#1E1E1E'
  const subtitleColor = colorMode === 'dark' ? '#e0e0e0' : '#606060'

  return (
    <Box minH="100vh" minW="100vw" bg={bgMain} position="relative">
      {/* interfaz */}
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
              <Heading size="2xl" color="#2E8B57" letterSpacing="tight" mb={2} className="app-title">
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
              {/* botones */}
              <Box position="absolute" top={8} right={12} zIndex={20} display="flex" alignItems="center" gap={2}>
                <IconButton
                  icon={<FaSyncAlt />}
                  onClick={handleResetChat}
                  aria-label="Reiniciar chat"
                  variant="ghost"
                  size="lg"
                  color={subtitleColor}
                  _hover={{ color: textColor }}
                  transition="transform 0.2s"
                  _active={{ transform: 'scale(0.85) rotate(90deg)' }}
                />
                <IconButton
                  icon={colorMode === 'dark' ? <FaSun /> : <FaMoon />}
                  onClick={toggleColorMode}
                  aria-label="Cambiar tema"
                  variant="ghost"
                  size="lg"
                  color={subtitleColor}
                  _hover={{ color: textColor }}
                />
              </Box>
            </Box>
          </motion.div>
        )}
      </AnimatePresence>
      {/* interfaz de chat*/}
      <AnimatePresence>
        {chatOpen && (
          <motion.div
            key="chat"
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -40 }}
            transition={{ duration: 0.5, ease: 'easeInOut' }}
            style={{ width: '100%', background: 'transparent' }}
            onAnimationStart={() => setIsTransitioning(true)}
            onAnimationComplete={() => setIsTransitioning(false)}
          >
            <Box minH="100vh" display="flex" flexDirection="column" alignItems="center" justifyContent="flex-start" bg="transparent">
              {/* header */}
              <Box w="100%" px={12} pt={8} pb={2} position="relative" bg="transparent">
                <Box textAlign="center">
                  <Heading size="2xl" color="#2E8B57" letterSpacing="tight" className="app-title">
                    VMware Assistance
                  </Heading>
                  <Text color={subtitleColor} fontSize="xl" mt={2}>
                    Diagnóstico inteligente de infraestructura virtual
                  </Text>
                </Box>
                <Box position="absolute" top={8} right={12} display="flex" alignItems="center" gap={2}>
                  <IconButton
                    icon={<FaSyncAlt />}
                    onClick={handleResetChat}
                    aria-label="Reiniciar chat"
                    variant="ghost"
                    size="lg"
                    color={subtitleColor}
                    _hover={{ color: textColor }}
                    transition="transform 0.2s"
                    _active={{ transform: 'scale(0.85) rotate(90deg)' }}
                  />
                  <IconButton
                    icon={colorMode === 'dark' ? <FaSun /> : <FaMoon />}
                    onClick={toggleColorMode}
                    aria-label="Cambiar tema"
                    variant="ghost"
                    size="lg"
                    color={subtitleColor}
                    _hover={{ color: textColor }}
                  />
                </Box>
              </Box>
              {/* chat */}
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
                bg="transparent"
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
                      background: colorMode === 'dark' ? '#454545' : '#a0a0a0',
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
                        message={msg}
                        isUser={msg.isUser}
                      />
                    ))}
                    {isLoading && (
                      <Flex justify="center" my={4}>
                        <Spinner color="#2E8B57" />
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
