const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');
const cors = require('cors');

const server = express();
const SERVER_PORT = 3000;

// Middleware setup
server.use(cors());
server.use(bodyParser.json());
server.use(express.static('public'));

// Utility to create file paths for logs based on timestamps
const generateLogFilePath = () => {
    const currentDate = new Date();
    const year = currentDate.getFullYear();
    const month = String(currentDate.getMonth() + 1).padStart(2, '0');
    const day = String(currentDate.getDate()).padStart(2, '0');
    const hour = String(currentDate.getHours()).padStart(2, '0');
    const minute = String(currentDate.getMinutes()).padStart(2, '0');
    const second = String(currentDate.getSeconds()).padStart(2, '0');

    const logFolder = path.join(__dirname, 'logs', `${year}${month}${day}${hour}`);
    fs.mkdirSync(logFolder, { recursive: true });
    const logFile = path.join(logFolder, `${year}${month}${day}${hour}${minute}${second}.txt`);
    return logFile;
};

// Format a timestamp into a readable string
const formatLogTimestamp = (timestamp) => {
    const dateInstance = new Date(timestamp);
    const year = dateInstance.getFullYear();
    const month = String(dateInstance.getMonth() + 1).padStart(2, '0');
    const day = String(dateInstance.getDate()).padStart(2, '0');
    const hour = String(dateInstance.getHours()).padStart(2, '0');
    const minute = String(dateInstance.getMinutes()).padStart(2, '0');
    const second = String(dateInstance.getSeconds()).padStart(2, '0');

    return `${year}/${month}/${day} ${hour}:${minute}:${second}`;
};

// Endpoint to record events
server.post('/api/event-log', (req, res) => {
    const { timestamp, action, product, quantity, price, route, agent } = req.body;

    // Generate formatted timestamp
    const logTimestamp = formatLogTimestamp(timestamp);

    // Construct the log entry
    const logEntry = `${logTimestamp}|${action}|${product}|${quantity}|${price}|${route}\n`;

    // Determine file path for logging
    const logFilePath = generateLogFilePath();

    // Write the log entry to the file
    fs.appendFile(logFilePath, logEntry, (error) => {
        if (error) {
            console.error('Error writing log entry:', error);
            return res.status(500).send('Failed to record event');
        }
        console.log('Logged event:', logEntry);
        res.status(200).send('Event successfully recorded');
    });
});

// Start the server
server.listen(SERVER_PORT, () => {
    console.log(`Server listening on http://localhost:${SERVER_PORT}`);
});
