import { extendTheme } from '@chakra-ui/react';

const theme = extendTheme({
  fonts: {
    heading: 'Inter, sans-serif',
    body: 'Inter, sans-serif',
  },
  styles: {
    global: (props) => ({
      body: {
        bg: props.colorMode === 'dark' ? '#1E1E1E' : '#FFFFFF',
        color: props.colorMode === 'dark' ? '#FFFFFF' : '#1E1E1E',
      },
    }),
  },
  config: {
    initialColorMode: 'dark',
    useSystemColorMode: false,
  },
  colors: {
    primary: {
      100: '#2E8B57',
      200: '#61bc84',
      300: '#c6ffe6',
    },
    accent: {
      100: '#8FBC8F',
      200: '#345e37',
    },
    text: {
      100: '#FFFFFF',
      200: '#e0e0e0',
    },
    bg: {
      100: '#1E1E1E',
      200: '#2d2d2d',
      300: '#454545',
    },
    brand: {
      50: '#c6ffe6',
      100: '#61bc84',
      200: '#2E8B57',
      300: '#8FBC8F',
      400: '#345e37',
      500: '#2E8B57',
      600: '#61bc84',
      700: '#8FBC8F',
      800: '#345e37',
      900: '#1E1E1E',
    },
    gray: {
      50: '#f7f7f7',
      100: '#e0e0e0',
      200: '#c0c0c0',
      300: '#a0a0a0',
      400: '#808080',
      500: '#606060',
      600: '#454545',
      700: '#2d2d2d',
      800: '#1E1E1E',
      900: '#0f0f0f',
    },
    blue: {
      50: '#c6ffe6',
      100: '#61bc84',
      200: '#2E8B57',
      300: '#8FBC8F',
      400: '#345e37',
      500: '#2E8B57',
      600: '#61bc84',
      700: '#8FBC8F',
      800: '#345e37',
      900: '#1E1E1E',
    },
  },
  components: {
    Input: {
      variants: {
        outline: (props) => ({
          field: {
            bg: props.colorMode === 'dark' ? '#2d2d2d' : '#FFFFFF',
            borderColor: props.colorMode === 'dark' ? '#454545' : '#e0e0e0',
            color: props.colorMode === 'dark' ? '#FFFFFF' : '#1E1E1E',
            _hover: {
              borderColor: props.colorMode === 'dark' ? '#61bc84' : '#2E8B57',
            },
            _focus: {
              borderColor: props.colorMode === 'dark' ? '#61bc84' : '#2E8B57',
              boxShadow: `0 0 0 1px ${props.colorMode === 'dark' ? '#61bc84' : '#2E8B57'}`,
            },
            _placeholder: {
              color: props.colorMode === 'dark' ? '#e0e0e0' : '#606060',
            },
          },
        }),
      },
    },
    Button: {
      variants: {
        solid: (props) => ({
          bg: props.colorScheme === 'blue' ? '#2E8B57' : props.colorScheme === 'primary' ? '#2E8B57' : undefined,
          color: '#FFFFFF',
          _hover: {
            bg: props.colorScheme === 'blue' ? '#61bc84' : props.colorScheme === 'primary' ? '#61bc84' : undefined,
          },
          _active: {
            bg: props.colorScheme === 'blue' ? '#8FBC8F' : props.colorScheme === 'primary' ? '#8FBC8F' : undefined,
          },
        }),
      },
    },
    Alert: {
      variants: {
        solid: (props) => {
          if (props.status === 'error') {
            return {
              container: {
                bg: '#c53030',
                color: 'white',
              },
            };
          }
          return {};
        },
      },
    },
  },
});

export default theme; 