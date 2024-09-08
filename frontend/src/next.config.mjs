/** @type {import('next').NextConfig} */
const nextConfig = {
  env:{
    NEXT_PUBLIC_API_URL: process.env.LEADOPT_API_ADDR,
    NEXT_PUBLIC_PORT: process.env.PORT
  },
  output: "standalone",
};
console.log(process.env)
export default nextConfig;
