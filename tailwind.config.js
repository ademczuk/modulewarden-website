/** @type {import('tailwindcss').Config} */
// Build: npx -y tailwindcss@3.4.17 -i input.css -o tw.css --minify
// Replaces the render-blocking cdn.tailwindcss.com Play CDN with a static, precompiled stylesheet.
module.exports = {
  content: ['./index.html', './privacy.html'],
  theme: { extend: {} },
  plugins: [],
};
