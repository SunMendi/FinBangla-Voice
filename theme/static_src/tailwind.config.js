/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        '../../blogs/templates/**/*.html',  // Templates in blogs app
        '../../templates/**/*.html',       // Project-level templates
        '../../**/templates/**/*.html',    // Templates in other apps
    ],
    theme: {
        extend: {},
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}