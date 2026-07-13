/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
    '../cycles/templates/**/*.html',
  ],
  theme: {
    extend: {
      fontFamily: {
        heading: ['Orbitron', 'system-ui', 'sans-serif'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      colors: {
        cosmic: {
          dark: '#07071a',
          midnight: '#0f0c29',
          deep: '#1a0a2e',
          purple: '#7c3aed',
          cyan: '#06b6d4',
          gold: '#f59e0b',
        },
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'pulse-glow': 'pulseGlow 3s ease-in-out infinite',
        'slide-up': 'slideUp 0.6s ease-out forwards',
        'twinkle': 'twinkle 4s ease-in-out infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' },
        },
        pulseGlow: {
          '0%, 100%': { boxShadow: '0 0 20px rgba(168, 85, 247, 0.2)' },
          '50%': { boxShadow: '0 0 40px rgba(168, 85, 247, 0.4), 0 0 60px rgba(6, 182, 212, 0.2)' },
        },
      },
    },
  },
  plugins: [],
}
