/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class', // Enable dark mode with class strategy
content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
    "./layout.tsx", // Safe side ke liye agar file root par ho
    "./page.tsx",
  ],
  theme: {
    extend: {
      fontFamily: {
        // Define a custom font family for Inter
        sans: ['Inter', 'sans-serif'],
      },
      colors: {
        // Define custom colors for a futuristic dark theme
        'dark-background': '#030303',
        'dark-surface': '#1A1A1A',
        'dark-border': '#2A2A2A',
        'dark-text': '#E0E0E0',
        'dark-text-secondary': '#A0A0A0',
        'primary-purple': '#8B5CF6', // Example purple from specs
        'primary-blue': '#3B82F6', // Example blue from specs
        'electric-blue': '#7DF9FF',
        'neon-violet': '#BC13FE',
      },
      animation: {
        'fade-in-up': 'fadeInUp 0.6s ease-out',
        'slide-in': 'slideIn 0.3s ease-out',
        'expand': 'expand 0.3s ease-out',
        'shake': 'shake 0.4s ease-in-out',
        'pulse-slow': 'pulseSlow 4s ease-in-out infinite',
        'scale-in': 'scaleIn 0.2s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
      },
      keyframes: {
        fadeInUp: {
          from: { opacity: 0, transform: 'translateY(20px)' },
          to: { opacity: 1, transform: 'translateY(0)' },
        },
        slideIn: {
          from: { opacity: 0, transform: 'translateX(-10px)' },
          to: { opacity: 1, transform: 'translateX(0)' },
        },
        expand: {
          from: { transform: 'scaleX(0)' },
          to: { transform: 'scaleX(1)' },
        },
        shake: {
          '0%, 100%': { transform: 'translateX(0)' },
          '10%, 30%, 50%, 70%, 90%': { transform: 'translateX(-4px)' },
          '20%, 40%, 60%, 80%': { transform: 'translateX(4px)' },
        },
        pulseSlow: {
          '0%, 100%': { opacity: 0.2, transform: 'scale(1)' },
          '50%': { opacity: 0.3, transform: 'scale(1.05)' },
        },
        scaleIn: {
          from: { opacity: 0, transform: 'scale(0.95)' },
          to: { opacity: 1, transform: 'scale(1)' },
        },
        slideUp: {
          from: { opacity: 0, transform: 'translateY(10px)' },
          to: { opacity: 1, transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [],
};
