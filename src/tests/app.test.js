const request = require('supertest')
const app = require('../App')

afterAll(async () => {
    // If your app has a database connection (e.g., Mongoose)
    // await mongoose.connection.close();
    
    // If your app was explicitly started:
    await app.close(); 
});

test('GET / returns ok', async () => {
    const res = await request(app).get('/')
    expect(res.statusCode).toBe(200)
    expect(res.body.status).toBe('ok')
})

test('GET /health returns healthy', async () => {
    const res = await request(app).get('/health')
    expect(res.statusCode).toBe(200)
})