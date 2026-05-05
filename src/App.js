const express = require('express')
const app = express()
const PORT = process.env.PORT || 3000

// Endpoint principal
app.get('/', (req, res) => {
    res.json({
        status: 'ok',
        message: 'Pipeline CI/CD funcionando',
        env: 'dev'
    })
})

// Smoke test endpoint
app.get('/health', (req, res) => {
    res.status(200).json({ status: 'healthy' })
})

/**
 * Only start the server if this file is run directly.
 * 'require.main === module' is true when you run 'node App.js', 
 * but false when Jest 'require's it for testing.
 */
if (require.main === module) {
    app.listen(PORT, () => {
        console.log(`Server on port ${PORT}`)
    })
}

module.exports = app