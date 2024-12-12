const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');

const cors = require('cors');
const app = express();

app.use(bodyParser.json());
app.use(cors({ origin: 'http://localhost:3000' }));
const FUSEKI_URL = 'http://localhost:3030/myDataset/query';

app.post('/sparql', async (req, res) => {
    const { query } = req.body;
    try {
        const response = await axios.post(FUSEKI_URL, `query=${encodeURIComponent(query)}`, {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        });
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

const PORT = 4000;
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
