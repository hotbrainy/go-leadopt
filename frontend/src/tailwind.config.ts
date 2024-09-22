import type { Config } from "tailwindcss";
const config: Config = {
  darkMode: "class",
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    markdownBase: {
      wrapperClass: "content",
    },
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
      },
      typography: () => ({
        DEFAULT: {
          css: {
            pre: {
              padding: "0 !important",
              margin: "0 !important",

            },
            maxWidth: '105ch'
          },
        },
      }),
    },
  },
  plugins: [require("@tailwindcss/typography")],
};
export default config;
