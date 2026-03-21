(function initDomUtils(global) {
  const SELECTORS = [
    "textarea",
    "[contenteditable='true']",
    "[contenteditable='plaintext-only']",
    "[role='textbox']"
  ];

  function isElementVisible(element) {
    if (!element || !element.isConnected) {
      return false;
    }

    const style = window.getComputedStyle(element);
    if (style.display === "none" || style.visibility === "hidden") {
      return false;
    }

    const rect = element.getBoundingClientRect();
    return rect.width > 80 && rect.height > 28;
  }

  function isTextLikeElement(element) {
    if (!element) {
      return false;
    }

    if (element instanceof HTMLTextAreaElement) {
      return true;
    }

    if (element instanceof HTMLInputElement) {
      const type = (element.type || "").toLowerCase();
      return type === "text" || type === "search";
    }

    const contentEditable = element.getAttribute("contenteditable");
    if (contentEditable === "true" || contentEditable === "plaintext-only") {
      return true;
    }

    return element.getAttribute("role") === "textbox";
  }

  function isSupportedPromptField(element) {
    return isTextLikeElement(element) && isElementVisible(element);
  }

  function findPromptFields(root) {
    const scope = root || document;
    return Array.from(scope.querySelectorAll(SELECTORS.join(","))).filter(isSupportedPromptField);
  }

  function normalizeText(value) {
    return (value || "").replace(/\u00a0/g, " ").replace(/\r/g, "").trim();
  }

  function getPromptValue(element) {
    if (!element) {
      return "";
    }

    if ("value" in element) {
      return normalizeText(element.value);
    }

    return normalizeText(element.innerText || element.textContent || "");
  }

  function dispatchTextEvents(element) {
    element.dispatchEvent(new InputEvent("input", { bubbles: true, inputType: "insertText" }));
    element.dispatchEvent(new Event("change", { bubbles: true }));
  }

  function setInputValue(element, value) {
    const prototype = Object.getPrototypeOf(element);
    const descriptor = Object.getOwnPropertyDescriptor(prototype, "value");

    if (descriptor && typeof descriptor.set === "function") {
      descriptor.set.call(element, value);
    } else {
      element.value = value;
    }

    dispatchTextEvents(element);
  }

  function setContentEditableValue(element, value) {
    element.focus();

    const selection = window.getSelection();
    const range = document.createRange();
    range.selectNodeContents(element);
    selection.removeAllRanges();
    selection.addRange(range);

    const inserted = document.execCommand && document.execCommand("insertText", false, value);
    if (!inserted) {
      element.innerHTML = "";
      const lines = value.split("\n");
      lines.forEach((line, index) => {
        if (index > 0) {
          element.appendChild(document.createElement("br"));
        }
        element.appendChild(document.createTextNode(line));
      });
    }

    selection.removeAllRanges();
    dispatchTextEvents(element);
  }

  function setPromptValue(element, value) {
    if (!element) {
      return;
    }

    if ("value" in element) {
      setInputValue(element, value);
      return;
    }

    setContentEditableValue(element, value);
  }

  function detectSite() {
    const host = window.location.hostname;
    if (host.includes("claude.ai")) {
      return "Claude";
    }
    if (host.includes("chatgpt.com") || host.includes("chat.openai.com")) {
      return "ChatGPT";
    }
    return "Unknown";
  }

  global.NukhbaPromptDom = {
    detectSite,
    findPromptFields,
    getPromptValue,
    isSupportedPromptField,
    setPromptValue
  };
})(typeof globalThis !== "undefined" ? globalThis : window);
