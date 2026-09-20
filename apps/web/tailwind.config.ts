import type { Config } from 'tailwindcss';

// Brand palette from CLAUDE.md section 5: greens and cream. Gold is donate CTAs
// only, purple is Dr. Elaine memorial content only. One shadow value.
const config: Config = {
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        green: {
          deep: '#1d3b2a',
          mid: '#2f6b46',
          bright: '#4c9a68',
        },
        cream: '#f4efe4',
        gold: '#c8963e',
        elaine: '#6b4f8a',
      },
      boxShadow: {
        sfw: '0 2px 8px rgba(29, 59, 42, 0.12)',
      },
    },
  },
  plugins: [],
};

export default config;
