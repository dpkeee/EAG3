// Listen for installation
chrome.runtime.onInstalled.addListener(async () => {
  // Initialize default settings
  chrome.storage.local.set({
    colors: ['#FFB6C1', '#98FB98', '#87CEFA', '#DDA0DD', '#F0E68C'],
    lastUsedColor: null
  });

  chrome.contextMenus.create({
    id: "changeColor",
    title: "Change page color",
    contexts: ["page"]
  });

  // Check if API key exists in storage
  const result = await chrome.storage.local.get(['geminiApiKey']);
  if (!result.geminiApiKey) {
    // Try to get API key from api.env file
    try {
      const response = await fetch('api.env');
      const text = await response.text();
      const apiKey = text.match(/GEMINI_API_KEY=(.+)/)[1];
      await chrome.storage.local.set({ geminiApiKey: apiKey });
    } catch (error) {
      console.log('Could not load API key from api.env:', error);
    }
  }
});

// Listen for messages from popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "getColors") {
    chrome.storage.local.get(['colors'], (result) => {
      sendResponse({ colors: result.colors });
    });
    return true; // Required for async response
  }
  if (message.action === "getApiKey") {
    chrome.storage.local.get(['geminiApiKey'], (result) => {
      sendResponse({ apiKey: result.geminiApiKey });
    });
    return true;
  }
});

// Listen for extension icon clicks (optional)
chrome.action.onClicked.addListener((tab) => {
  // This only works if no default popup is set
  console.log('Extension icon clicked!');
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "changeColor") {
    chrome.storage.local.get(['colors'], (result) => {
      const colors = result.colors;
      chrome.scripting.executeScript({
        target: { tabId: tab.id },
        function: (colors) => {
          const randomColor = colors[Math.floor(Math.random() * colors.length)];
          document.body.style.backgroundColor = randomColor;
        },
        args: [colors]
      });
    });
  }
}); 