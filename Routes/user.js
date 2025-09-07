import express from "express";
import pgClient from "../db.js";

const UserRoutes = express.Router();


UserRoutes.get("/courses", async (req, res) => {

    const response = await pgClient.query('SELECT * FROM courses');
    res.json(response.rows);
});




UserRoutes.post('/user-courses', async (req, res) => {
    const { email, username } = req.body;
    if (!email || !username) {
        return res.status(400).json({ error: 'Email and username are required.' });
    }
    try {
        const query = 'SELECT * FROM user_course WHERE email = $1 AND username = $2';
        const result = await pgClient.query(query, [email, username]);
        return res.json(result.rows);
    } catch (err) {
        console.error(err);
        return res.status(500).json({ error: 'Server error.' });
    }
});






UserRoutes.post('/Login', async (req, res) => {
    const { email, password } = req.body;
    if (!email || !password) {
        return res.status(400).json({ error: 'Email and password are required.' });
    }
    try {
       
        const result = await pgClient.query('SELECT role, username FROM users WHERE email = $1 AND password = $2', [email, password]);
        if (!result.rows || result.rows.length === 0) {
            return res.status(401).json({ error: 'Invalid email or password.' });
        }
       
        return res.json({ role: result.rows[0].role, username: result.rows[0].username });
    } catch (err) {
        console.error(err);
        return res.status(500).json({ error: 'Server error.' });
    }
});





UserRoutes.post('/addCart', async (req, res) => {
    const {
        username,
        email,
        title,
        description,
        instructor,
        price,
        category,
        duration,
        lessons_count,
        rating,
        image_url,
        quantity
    } = req.body;

    if (!username || !email || !title || !instructor || price === undefined || !category || !duration || lessons_count === undefined || rating === undefined || !image_url || quantity === undefined || description === undefined) {
        return res.status(400).json({ error: 'All fields are required.' });
    }

    try {
        const query = `INSERT INTO cart_products (username, email, title, description, instructor, price, category, duration, lessons_count, rating, image_url, quantity)
                       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12) RETURNING *`;
        const values = [username, email, title, description, instructor, price, category, duration, lessons_count, rating, image_url, quantity];

        const result = await pgClient.query(query, values);
        return res.status(201).json({ product: result.rows[0] });
    } catch (err) {
        console.error(err);
        return res.status(500).json({ error: 'Server error.' });
    }
});






    
    UserRoutes.post('/showcart', async (req, res) => {
        const { email } = req.body;
        if (!email) {
            return res.status(400).json({ error: 'Email is required.' });
        }
        try {
            const query = 'SELECT * FROM cart_products WHERE email = $1 ORDER BY id ASC';
            const result = await pgClient.query(query, [email]);
            return res.json(result.rows);
        } catch (err) {
            console.error(err);
            return res.status(500).json({ error: 'Server error.' });
        }
    });








UserRoutes.delete('/delcart', async (req, res) => {
    const { id } = req.body;
    if (!id) {
        return res.status(400).json({ error: 'ID is required.' });
    }
    try {
        const query = 'DELETE FROM cart_products WHERE id = $1 RETURNING *';
        const result = await pgClient.query(query, [id]);
        if (result.rowCount === 0) {
            return res.status(404).json({ error: 'Item not found.' });
        }
        return res.json({ deleted: result.rows[0] });
    } catch (err) {
        console.error(err);
        return res.status(500).json({ error: 'Server error.' });
    }
});







UserRoutes.put('/updatecartquantity', async (req, res) => {
    const { id, quantity } = req.body;
    if (!id || quantity === undefined) {
        return res.status(400).json({ error: 'ID and quantity are required.' });
    }
    try {
        const query = 'UPDATE cart_products SET quantity = $1 WHERE id = $2 RETURNING *';
        const values = [quantity, id];
        const result = await pgClient.query(query, values);
        if (result.rowCount === 0) {
            return res.status(404).json({ error: 'Item not found.' });
        }
        return res.json({ updated: result.rows[0] });
    } catch (err) {
        console.error(err);
        return res.status(500).json({ error: 'Server error.' });
    }
});




UserRoutes.post('/addcoursestouser', async (req, res) => {
    const {
        username,
        email,
        title,
        description,
        instructor,
        price,
        category,
        duration,
        lessons_count,
        rating,
        image_url
    } = req.body;

    if (!username || !email || !title || !description || !instructor || price === undefined || !category || !duration || lessons_count === undefined || rating === undefined || !image_url) {
        return res.status(400).json({ error: 'All fields are required.' });
    }

    try {
        const query = `INSERT INTO user_course (username, email, title, description, instructor, price, category, duration, lessons_count, rating, image_url)
                       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11) RETURNING *`;
        const values = [username, email, title, description, instructor, price, category, duration, lessons_count, rating, image_url];
        const result = await pgClient.query(query, values);
        return res.status(201).json({ enrolled: result.rows[0] });
    } catch (err) {
        console.error(err);
        return res.status(500).json({ error: 'Server error.' });
    }
});





UserRoutes.get('/assignments', async (req, res) => {
    try {
        const result = await pgClient.query('SELECT * FROM tasks');
        return res.json(result.rows);
    } catch (err) {
        console.error(err);
        return res.status(500).json({ error: 'Server error.' });
    }
});




UserRoutes.post('/signup', async (req, res) => {
    const { username, email, password, role } = req.body;
    if (!username || !email || !password || !role) {
        return res.status(400).json({ error: 'All fields are required.' });
    }
    try {
        const checkQuery = 'SELECT * FROM users WHERE email = $1 OR username = $2';
        const checkResult = await pgClient.query(checkQuery, [email, username]);
        if (checkResult.rows.length > 0) {
            return res.status(409).json({ error: 'Account already exists.' });
        }
        const query = `INSERT INTO users (username, email, password, role) VALUES ($1, $2, $3, $4) RETURNING *`;
        const values = [username, email, password, role];
        const result = await pgClient.query(query, values);
        return res.status(201).json({ user: result.rows[0] });
    } catch (err) {
        console.error(err);
        return res.status(500).json({ error: 'Server error.' });
    }
});



export default UserRoutes;


