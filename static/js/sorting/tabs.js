(() => {
  const tabs = Array.from(document.querySelectorAll(".sorting-tab"));
  const panels = Array.from(document.querySelectorAll(".sorting-section"));
  if (!tabs.length || !panels.length) return;

  const applyTheme = (panel) => {
    const styles = window.getComputedStyle(panel);
    const keys = ["--accent", "--accent-2", "--bg-aurora-1", "--bg-aurora-2", "--bg-aurora-3"];
    keys.forEach((key) => {
      const value = styles.getPropertyValue(key).trim();
      if (value) {
        document.body.style.setProperty(key, value);
      }
    });
  };

  const setActive = (targetId, updateHash) => {
    panels.forEach((panel) => {
      panel.classList.toggle("is-active", panel.id === targetId);
    });
    tabs.forEach((tab) => {
      const isActive = tab.dataset.tabTarget === targetId;
      tab.classList.toggle("is-active", isActive);
      tab.setAttribute("aria-selected", isActive ? "true" : "false");
      tab.tabIndex = isActive ? 0 : -1;
    });
    const activePanel = panels.find((panel) => panel.id === targetId);
    if (activePanel) {
      applyTheme(activePanel);
    }
    if (updateHash) {
      history.replaceState(null, "", `#${targetId}`);
    }
  };

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      setActive(tab.dataset.tabTarget, true);
    });
  });

  const initial = window.location.hash.replace("#", "");
  const hasMatch = tabs.some((tab) => tab.dataset.tabTarget === initial);
  const defaultId = tabs[0].dataset.tabTarget;
  setActive(hasMatch ? initial : defaultId, false);
})();
