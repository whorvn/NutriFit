const express = require('express');
const WebSocket = require('ws');
const axios = require('axios');  // For making HTTP requests to the chatbot
const app = express();
const PORT = 3000;

// Start the WebSocket server
const server = app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});

const wss = new WebSocket.Server({ server });

wss.on('connection', (ws) => {
  console.log('New client connected');

  ws.on('message', async (message) => {
    console.log(`Received: ${message}`);

    try {
      // Send message to the Python chatbot API
      const response = await axios.post('http://localhost:5000/chatbot', {
        message: message
      });

      const botResponse = response.data.response;

      // Broadcast the chatbot response back to all connected clients
      wss.clients.forEach((client) => {
        if (client.readyState === WebSocket.OPEN) {
          client.send(`Bot: ${botResponse}`);
        }
      });

    } catch (error) {
      console.error('Error fetching chatbot response:', error);
    }
  });

  ws.on('close', () => {
    console.log('Client disconnected');
  });
});
