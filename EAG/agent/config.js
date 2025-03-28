// Load API key from storage
async function getApiKey() {
  const result = await chrome.storage.local.get(['geminiApiKey']);
  return result.geminiApiKey;
}

// Set API key in storage
async function setApiKey(apiKey) {
  await chrome.storage.local.set({ geminiApiKey: apiKey });
}

export { getApiKey, setApiKey }; 