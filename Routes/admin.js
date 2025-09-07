import express from 'express'
import pgClient from '../db.js';

const AdminRoutes = express.Router();


AdminRoutes.get('/usercount', async (req, res) => {
    try {
        const result = await pgClient.query('SELECT COUNT(*) FROM users');
        return res.json({ count: result.rows[0].count });
    } catch (err) {
        console.error(err);
        return res.status(500).json({ error: 'Server error.' });
    }
});


AdminRoutes.get('/coursescount', async (req, res) => {
    try {
        const result = await pgClient.query('SELECT COUNT(*) FROM courses');
        return res.json({ count: result.rows[0].count });
    } catch (err) {
        console.error(err);
        return res.status(500).json({ error: 'Server error.' });
    }
});


AdminRoutes.get('/admincourses', async (req, res) => {
    try {
        const result = await pgClient.query('SELECT id, title, description, instructor FROM courses');
        return res.json(result.rows);
    } catch (err) {
        console.error(err);
        return res.status(500).json({ error: 'Server error.' });
    }
});





AdminRoutes.delete('/deladmincourses', async (req, res) => {
    const { id } = req.body;
    if (!id) {
        return res.status(400).json({ error: 'ID is required.' });
    }
    try {
        const query = 'DELETE FROM courses WHERE id = $1 RETURNING *';
        const result = await pgClient.query(query, [id]);
        if (result.rowCount === 0) {
            return res.status(404).json({ error: 'Course not found.' });
        }
        return res.json({ deleted: result.rows[0] });
    } catch (err) {
        console.error(err);
        return res.status(500).json({ error: 'Server error.' });
    }
});





AdminRoutes.put('/editadmincourse', async (req, res) => {
    const { id, instructor } = req.body;
    if (!id || !instructor) {
        return res.status(400).json({ error: 'ID and instructor are required.' });
    }
    try {
        const query = 'UPDATE courses SET instructor = $1 WHERE id = $2 RETURNING *';
        const result = await pgClient.query(query, [instructor, id]);
        if (result.rowCount === 0) {
            return res.status(404).json({ error: 'Course not found.' });
        }
        return res.json({ updated: result.rows[0] });
    } catch (err) {
        console.error(err);
        return res.status(500).json({ error: 'Server error.' });
    }
});




AdminRoutes.post('/addadmincourse', async (req, res) => {
    const { title, description, instructor, rating, duration, lessonsCount, price, imageUrl, category } = req.body;
    if (!title || !description || !instructor || !rating || !duration || !lessonsCount || !price || !imageUrl || !category) {
        return res.status(400).json({ error: 'All fields are required.' });
    }
    try {
        const query = `INSERT INTO courses (title, description, instructor, rating, duration, lessons_count, price, image_url, category)
                       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9) RETURNING *`;
        const values = [title, description, instructor, rating, duration, lessonsCount, price, imageUrl, category];
        const result = await pgClient.query(query, values);
        return res.status(201).json({ course: result.rows[0] });
    } catch (err) {
        console.error(err);
        return res.status(500).json({ error: 'Server error.' });
    }
});





AdminRoutes.get('/adminusers', async (req, res) => {
    try {
        const result = await pgClient.query('SELECT * FROM users');
        return res.json(result.rows);
    } catch (err) {
        console.error(err);
        return res.status(500).json({ error: 'Server error.' });
    }
});





AdminRoutes.post('/addadminuser', async (req, res) => {
    const { email, username, password, role } = req.body;
    if (!email || !username || !password || !role) {
        return res.status(400).json({ error: 'All fields are required.' });
    }
    try {
        const query = `INSERT INTO users (email, username, password, role) VALUES ($1, $2, $3, $4) RETURNING *`;
        const values = [email, username, password, role];
        const result = await pgClient.query(query, values);
        return res.status(201).json({ user: result.rows[0] });
    } catch (err) {
        console.error(err);
        return res.status(500).json({ error: 'Server error.' });
    }
});




AdminRoutes.delete('/deluser', async (req, res) => {
    const { id } = req.body;
    if (!id) {
        return res.status(400).json({ error: 'ID is required.' });
    }
    try {
        const query = 'DELETE FROM users WHERE id = $1 RETURNING *';
        const result = await pgClient.query(query, [id]);
        if (result.rowCount === 0) {
            return res.status(404).json({ error: 'User not found.' });
        }
        return res.json({ deleted: result.rows[0] });
    } catch (err) {
        console.error(err);
        return res.status(500).json({ error: 'Server error.' });
    }
});


export default AdminRoutes;
