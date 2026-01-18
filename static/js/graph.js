(() => {
  const stage = document.querySelector(".graph-stage");
  if (!stage) return;
  const raw = stage.dataset.path || "[]";
  let path = [];
  try {
    path = JSON.parse(raw);
  } catch (error) {
    return;
  }
  if (!Array.isArray(path) || !path.length) return;

  const keys = new Set();
  for (let i = 0; i < path.length - 1; i += 1) {
    const a = path[i];
    const b = path[i + 1];
    const key = a < b ? `${a}||${b}` : `${b}||${a}`;
    keys.add(key);
  }

  document.querySelectorAll(".rail-seg").forEach((seg) => {
    const key = seg.getAttribute("data-key");
    if (keys.has(key)) seg.classList.add("route-active");
  });
})();
