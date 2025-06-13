import React from 'react'
import ReactDOM from 'react-dom/client'
import { ChakraProvider, extendTheme } from '@chakra-ui/react'
import App from './App'
import './index.css'

const theme = extendTheme({
  fonts: {
    heading: 'Inter, sans-serif',
    body: 'Inter, sans-serif',
  },
  styles: {
    global: (props) => ({
      body: {
        bg: props.colorMode === 'dark' ? '#18181A' : 'gray.50',
        color: props.colorMode === 'dark' ? 'white' : 'gray.800',
      },
    }),
  },
  config: {
    initialColorMode: 'light',
    useSystemColorMode: false,
  },
  colors: {
    brand: {
      50: '#e3f2fd',
      100: '#bbdefb',
      200: '#90caf9',
      300: '#64b5f6',
      400: '#42a5f5',
      500: '#2196f3',
      600: '#1e88e5',
      700: '#1976d2',
      800: '#1565c0',
      900: '#0d47a1',
    },
  },
  components: {
    Input: {
      variants: {
        outline: (props) => ({
          field: {
            bg: props.colorMode === 'dark' ? 'gray.700' : 'white',
            _hover: {
              borderColor: props.colorMode === 'dark' ? 'blue.300' : 'blue.500',
            },
            _focus: {
              borderColor: props.colorMode === 'dark' ? 'blue.300' : 'blue.500',
              boxShadow: `0 0 0 1px ${props.colorMode === 'dark' ? 'var(--chakra-colors-blue-300)' : 'var(--chakra-colors-blue-500)'}`,
            },
          },
        }),
      },
    },
    Toast: {
      baseStyle: {
        container: {
          bg: '#FEB2B2',
          color: '#2D3748',
        },
      },
    },
  },
})

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ChakraProvider theme={theme}>
      <App />
    </ChakraProvider>
  </React.StrictMode>,
)
