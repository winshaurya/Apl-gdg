/** @type {import('next').NextConfig} */
const nextConfig = {
  // Build output will be placed inside the functions folder so Firebase
  // Functions can serve the built Next app during deployment.
  distDir: 'functions/.next'
}

module.exports = nextConfig;
