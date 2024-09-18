module.exports = {
  content: [
    './smarthome/templates/**/*.html',             // All HTML files in templates
    './smarthome/templates/devices/**/*.html',     // HTML files in devices directory
    './smarthome/templates/logs/consumption/**/*.html', // HTML files in consumption logs
    './smarthome/templates/logs/history/**/*.html', // HTML files in history logs
    './smarthome/templates/rooms/**/*.html',        // HTML files in rooms directory
    './smarthome/static/**/*.js',                    // JavaScript files
  ],
  theme: {
    extend: {
      colors: {
        primary: '#007bff',
        secondary: '#6c757d',
      },
      spacing: {
        '128': '32rem',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
};