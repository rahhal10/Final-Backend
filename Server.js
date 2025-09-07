import express from 'express'
import dotenv from 'dotenv';
import pgClient from './db.js';
import UserRoutes from './Routes/user.js';
import AdminRoutes from './Routes/admin.js';
import morgan from 'morgan';
import cors from 'cors';

const app = express();
dotenv.config();

app.use(express.json());
app.use(cors());
app.use(morgan('dev'));


app.use('/api/users', UserRoutes);


pgClient.connect().then(() => {

app.listen(process.env.PORT, () => {
    console.log(`Server is running on port ${process.env.PORT}`);
});

})