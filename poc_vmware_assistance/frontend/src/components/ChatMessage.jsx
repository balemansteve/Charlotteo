import { Box, Text, Flex, Avatar, useColorMode, IconButton, useToast } from '@chakra-ui/react'
import { FaRobot, FaCopy, FaEdit, FaSyncAlt } from 'react-icons/fa'

const ChatMessage = ({ message, isUser }) => {
  const { colorMode } = useColorMode()
  const toast = useToast()

  const handleCopy = () => {
    navigator.clipboard.writeText(message.text)
    toast({
      title: 'Copiado',
      description: 'El mensaje ha sido copiado al portapapeles.',
      status: 'success',
      duration: 2000,
      isClosable: true,
      position: 'top',
    })
  }

  if (isUser) {
    return (
      <Flex w="100%" justify="flex-end" mb={4} px={4}>
        <Box maxW={{ base: '90%', md: '70%' }}>
          <Box
            bg="#00b94e"
            color="white"
            p={3}
            borderRadius="20px 20px 5px 20px"
          >
            <Text whiteSpace="pre-wrap" wordBreak="break-word">
              {message.text}
            </Text>
          </Box>
          <Flex justify="flex-end" mt={2} gap={1}>
            <IconButton
              size="xs"
              variant="ghost"
              icon={<FaCopy />}
              aria-label="Copiar mensaje"
              onClick={handleCopy}
              _hover={{ color: 'primary.200' }}
            />
          </Flex>
        </Box>
      </Flex>
    )
  }

  // bot message
  return (
    <Flex w="100%" justify="flex-start" mb={4} px={4}>
      <Flex align="flex-start">
        <Avatar size="sm" icon={<FaRobot size={20} />} bg="#00b94e" mr={3} />
        <Box maxW={{ base: '90%', md: '70%' }}>
          <Text fontWeight="bold" mb={2} color={colorMode === 'dark' ? 'text.200' : 'gray.700'}>
            {message.name || 'Charlotteo'}
          </Text>
          <Text
            whiteSpace="pre-wrap"
            wordBreak="break-word"
            color={colorMode === 'dark' ? 'text.100' : 'gray.800'}
          >
            {message.text}
          </Text>
          <Flex justify="flex-start" mt={2} gap={1}>
            <IconButton
              size="xs"
              variant="ghost"
              icon={<FaCopy />}
              aria-label="Copiar mensaje"
              onClick={handleCopy}
              _hover={{ color: 'primary.200' }}
            />
          </Flex>
        </Box>
      </Flex>
    </Flex>
  )
}

export default ChatMessage 