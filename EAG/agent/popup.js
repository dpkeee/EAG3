import { getApiKey, setApiKey } from './config.js';

document.addEventListener('DOMContentLoaded', async () => {
  const apiKey = await getApiKey();
  if (apiKey) {
    document.getElementById('apiKey').value = apiKey;
  }

  document.getElementById('saveApiKey').addEventListener('click', async () => {
    const apiKey = document.getElementById('apiKey').value;
    await setApiKey(apiKey);
    alert('API key saved!');
  });

  document.getElementById('generateResponse').addEventListener('click', async () => {
    const apiKey = await getApiKey();
    if (!apiKey) {
      alert('Please set your Gemini API key first!');
      return;
    }

    const userInput = document.getElementById('userInput').value;
    const responseDiv = document.getElementById('response');
    
    responseDiv.textContent = 'Generating response...';

    try {
      const response = await generateGeminiResponse(userInput, apiKey);
      responseDiv.textContent = response;
    } catch (error) {
      responseDiv.textContent = `Error: ${error.message}`;
    }
  });
});

async function generateGeminiResponse(prompt, apiKey) {
  const url = 'https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent';
  
  const response = await fetch(`${url}?key=${apiKey}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      contents: [{
        parts: [{
          text: prompt
        }]
      }]
    })
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.statusText}`);
  }

  const data = await response.json();
  return data.candidates[0].content.parts[0].text;
} 