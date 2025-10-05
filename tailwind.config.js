/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      "./templates/**/*.html",
      "./static/**/*.js"
    ],
    theme: {
      extend: {
        fontFamily: {
          'montserrat': ['Montserrat', 'sans-serif']
        },
        animation: {
          'fade-in-up': 'fadeInUp 0.8s ease-out',
          'fade-in-left': 'fadeInLeft 0.8s ease-out',
          'fade-in-right': 'fadeInRight 0.8s ease-out',
          'scale-in': 'scaleIn 0.5s ease-out',
          'bounce-slow': 'bounce 3s infinite',
          'pulse-glow': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
          'gradient-shift': 'gradientShift 8s ease infinite',
          'float': 'float 6s ease-in-out infinite',
          'wiggle': 'wiggle 1s ease-in-out infinite',
        },
        keyframes: {
          fadeInUp: {
            '0%': { 
              opacity: '0',
              transform: 'translateY(50px)'
            },
            '100%': { 
              opacity: '1',
              transform: 'translateY(0)'
            }
          },
          fadeInLeft: {
            '0%': { 
              opacity: '0',
              transform: 'translateX(-50px)'
            },
            '100%': { 
              opacity: '1',
              transform: 'translateX(0)'
            }
          },
          fadeInRight: {
            '0%': { 
              opacity: '0',
              transform: 'translateX(50px)'
            },
            '100%': { 
              opacity: '1',
              transform: 'translateX(0)'
            }
          },
          scaleIn: {
            '0%': { 
              opacity: '0',
              transform: 'scale(0.9)'
            },
            '100%': { 
              opacity: '1',
              transform: 'scale(1)'
            }
          },
          gradientShift: {
            '0%, 100%': { 
              'background-position': '0% 50%'
            },
            '50%': { 
              'background-position': '100% 50%'
            }
          },
          float: {
            '0%, 100%': { 
              transform: 'translateY(0px)'
            },
            '50%': { 
              transform: 'translateY(-20px)'
            }
          },
          wiggle: {
            '0%, 100%': { 
              transform: 'rotate(-3deg)'
            },
            '50%': { 
              transform: 'rotate(3deg)'
            }
          }
        }
      },
    },
    plugins: [
      require("daisyui")
    ],
    daisyui: {
      themes: ["light", "dark", "corporate"],
    },
  }
  