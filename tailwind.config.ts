import { Montserrat } from "next/font/google";
import type { Config } from "tailwindcss";

const config: Config = {
  darkMode : 'class',
  content: [
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        customblue: "#222831",
        customwhite: "#EEEEEE",
        customlightblue: "#76ABAE",
        customgrey: "#31363F",
        white25: 'rgba(255, 255, 255, 0.25)',
        fieldwhite : 'rgba(238, 238, 238, 0.8)',
        white20 : 'rgba(238, 238, 238, 0.2)',
        white60 : 'rgba(238,238,238,0.6)',
        darkbg: "#181818", // Dark mode background
        darktext: "#E0E0E0", // Dark mode text color
        darklightblue: "#4A6A6B" // Dark mode light blue
      },
      fontFamily: {
        cabin: ['Cabin', 'sans-serif'],
        montserrat : ['Montserrat','sans-serif']
      },
    },
  },
  plugins: [],
};

export default config;

