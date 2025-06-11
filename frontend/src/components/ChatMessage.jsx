import { Box, Text, Flex, Avatar } from '@chakra-ui/react'
import { FaUser, FaRobot } from 'react-icons/fa'

const ChatMessage = ({ message, isUser }) => {
  return (
    <Flex
      w="100%"
      mb={4}
      justify={isUser ? 'flex-end' : 'flex-start'}
    >
      <Flex
        maxW="70%"
        bg={isUser ? 'blue.500' : 'gray.100'}
        color={isUser ? 'white' : 'black'}
        p={3}
        borderRadius="lg"
        boxShadow="sm"
        direction="column"
      >
        <Flex align="center" mb={2}>
          <Avatar
            size="sm"
            icon={isUser ? <FaUser /> : <FaRobot />}
            bg={isUser ? 'blue.600' : 'gray.400'}
            mr={2}
          />
          <Text fontSize="sm" fontWeight="bold">
            {isUser ? 'Tú' : (message.name || 'VMware Assistance')}
          </Text>
        </Flex>
        <Box>
          <Text 
            fontSize="md" 
            whiteSpace="pre-wrap"
            wordBreak="break-word"
          >
            {message}
          </Text>
        </Box>
      </Flex>
    </Flex>
  )
}

export default ChatMessage 