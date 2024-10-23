/** @type {import('next').NextConfig} */
const nextConfig = {
  env:{
    NEXT_PUBLIC_API_ADDR: process.env.LEADOPT_API_ADDR,
    NEXT_PUBLIC_API_PORT: process.env.LEADOPT_API_PORT,
    NEXT_PUBLIC_PORT: process.env.PORT
  },
  output: "standalone",
};
console.log(nextConfig, process.env)
export default nextConfig;
