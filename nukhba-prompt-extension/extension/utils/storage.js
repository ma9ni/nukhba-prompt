(function initStorage(global) {
  const constants = global.NukhbaPromptConstants;

  function getStorageArea() {
    return chrome.storage && chrome.storage.local;
  }

  function getSettings() {
    const storage = getStorageArea();
    const defaults = constants.DEFAULTS;
    return new Promise((resolve, reject) => {
      storage.get(defaults, (items) => {
        if (chrome.runtime.lastError) {
          reject(new Error(chrome.runtime.lastError.message));
          return;
        }
        resolve(items);
      });
    });
  }

  function saveSettings(nextSettings) {
    const storage = getStorageArea();
    return new Promise((resolve, reject) => {
      storage.set(nextSettings, () => {
        if (chrome.runtime.lastError) {
          reject(new Error(chrome.runtime.lastError.message));
          return;
        }
        resolve();
      });
    });
  }

  global.NukhbaPromptStorage = {
    getSettings,
    saveSettings
  };
})(typeof globalThis !== "undefined" ? globalThis : window);
