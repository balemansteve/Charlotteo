import { Input, IconButton, Flex, Text, useColorMode } from '@chakra-ui/react'
import { FaPaperPlane } from 'react-icons/fa'
import { useState } from 'react'

const MAX_CHARS = 300

const ChatInput = ({ onSendMessage, isLoading, placeholder = "Escribe tu consulta...", showCounter = false, modernStyle = false, hideBox = false, inputBg, fullWidthInput, inputColor }) => {
  const [message, setMessage] = useState('')
  const { colorMode } = useColorMode()

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
    <form onSubmit={handleSubmit} style={hideBox ? { width: '100%' } : modernStyle ? { width: '100%' } : {}}>
      <Flex
        p={hideBox ? 0 : modernStyle ? 0 : 4}
        borderTop={hideBox ? 'none' : modernStyle ? 'none' : '1px'}
        borderColor={hideBox ? 'none' : modernStyle ? 'none' : colorMode === 'dark' ? '#454545' : '#e0e0e0'}
        direction="column"
        align="center"
        w="100%"
        bg={hideBox ? 'transparent' : undefined}
        boxShadow={hideBox ? 'none' : undefined}
      >
        <Flex w="100%" align="center" justify="center">
          <Input
            value={message}
            onChange={handleChange}
            placeholder={placeholder}
            size={hideBox ? 'md' : modernStyle ? 'lg' : 'lg'}
            isDisabled={isLoading}
            bg={fullWidthInput ? 'transparent' : inputBg ? inputBg : (hideBox ? 'transparent' : modernStyle ? colorMode === 'dark' ? '#2d2d2d' : '#FFFFFF' : (colorMode === 'dark' ? '#2d2d2d' : '#FFFFFF'))}
            color={inputColor ? inputColor : (fullWidthInput ? colorMode === 'dark' ? '#FFFFFF' : '#1E1E1E' : (hideBox ? colorMode === 'dark' ? '#FFFFFF' : '#1E1E1E' : modernStyle ? colorMode === 'dark' ? '#FFFFFF' : '#1E1E1E' : colorMode === 'dark' ? '#FFFFFF' : '#1E1E1E'))}
            borderRadius={fullWidthInput ? 'xl' : (hideBox ? 'md' : modernStyle ? 'md' : 'md')}
            fontSize={hideBox ? '1.1rem' : modernStyle ? '1.15rem' : '1rem'}
            fontWeight={hideBox ? 400 : modernStyle ? 500 : 400}
            px={fullWidthInput ? 4 : (hideBox ? 3 : modernStyle ? 6 : 4)}
            py={hideBox ? 2 : modernStyle ? 4 : 2}
            border={fullWidthInput ? 'none' : (hideBox ? 'none' : undefined)}
            borderBottom={fullWidthInput ? 'none' : (hideBox ? (inputBg ? 'none' : `2px solid ${colorMode === 'dark' ? '#454545' : '#e0e0e0'}`) : undefined)}
            boxShadow={fullWidthInput ? 'none' : (hideBox ? 'none' : modernStyle ? '0 2px 8px 0 rgba(0,0,0,0.10)' : 'none')}
            _placeholder={{ color: colorMode === 'dark' ? '#e0e0e0' : '#606060' }}
            _focus={fullWidthInput ? { borderColor: 'none', boxShadow: 'none' } : (hideBox ? { borderColor: '#2E8B57', boxShadow: 'none' } : {
              borderColor: '#2E8B57',
              boxShadow: modernStyle ? '0 0 0 2px #2E8B57' : '0 0 0 1px #2E8B57',
            })}
            borderWidth={fullWidthInput ? '0px' : (hideBox ? '0px' : modernStyle ? '0px' : '1px')}
            flex={fullWidthInput ? 1 : undefined}
            mr={fullWidthInput ? 0 : 2}
          />
          <IconButton
            type="submit"
            colorScheme={hideBox || fullWidthInput ? undefined : modernStyle ? undefined : 'primary'}
            aria-label="Enviar mensaje"
            icon={<FaPaperPlane />}
            isLoading={isLoading}
            isDisabled={isLoading || !message.trim() || message.length > MAX_CHARS}
            bg={hideBox || fullWidthInput ? 'transparent' : modernStyle ? '#2E8B57' : '#2E8B57'}
            color={hideBox || fullWidthInput ? colorMode === 'dark' ? '#e0e0e0' : '#606060' : 'white'}
            _hover={hideBox || fullWidthInput ? { bg: 'transparent', color: '#2E8B57' } : modernStyle ? { bg: '#61bc84' } : { bg: '#61bc84' }}
            _active={hideBox || fullWidthInput ? { bg: 'transparent', color: '#8FBC8F' } : modernStyle ? { bg: '#8FBC8F' } : { bg: '#8FBC8F' }}
            borderRadius={fullWidthInput ? '0 xl xl 0' : (hideBox ? 'full' : modernStyle ? 'md' : 'md')}
            size={hideBox || fullWidthInput ? 'lg' : modernStyle ? 'lg' : 'lg'}
            fontSize={hideBox || fullWidthInput ? '1.5rem' : modernStyle ? '1.5rem' : '1rem'}
            boxShadow={hideBox || fullWidthInput ? 'none' : modernStyle ? '0 2px 8px 0 rgba(0,0,0,0.10)' : 'none'}
            ml={fullWidthInput ? 0 : (hideBox ? 2 : modernStyle ? 2 : 0)}
            h={fullWidthInput ? '48px' : undefined}
          />
        </Flex>
        {showCounter && (
          <Text
            fontSize={modernStyle ? 'md' : 'sm'}
            color={message.length > MAX_CHARS ? 'red.500' : colorMode === 'dark' ? '#e0e0e0' : '#606060'}
            mt={modernStyle ? 2 : 1}
            textAlign="right"
            w="100%"
            pr={modernStyle ? 2 : 0}
          >
            {message.length}/{MAX_CHARS}
          </Text>
        )}
      </Flex>
    </form>
  )
}

export default ChatInput 