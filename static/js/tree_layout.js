(() => {
  const layoutTreeAndBranches = () => {
    const stage = document.getElementById("treeStage");
    const svg = document.getElementById("treeSvg");
    if (!stage || !svg) return;

    const nodes = Array.from(stage.querySelectorAll(".tree-node-abs"));
    if (!nodes.length) return;

    const byIndex = {};
    nodes.forEach((node) => {
      byIndex[Number(node.dataset.index)] = node;
    });

    const build = (index = 0, level = 0) => {
      const el = byIndex[index];
      if (!el) return null;
      return {
        index,
        level,
        el,
        left: build(index * 2 + 1, level + 1),
        right: build(index * 2 + 2, level + 1)
      };
    };

    const root = build(0, 0);
    if (!root) return;

    const levelGap = 120;
    const topPad = 40;
    const allBoxes = nodes.map((node) => node.getBoundingClientRect());
    const maxChipW = Math.max(...allBoxes.map((box) => box.width));
    const baseGap = 32;
    const nodeGapMin = maxChipW + baseGap;

    let nextX = 0;

    const layout = (node) => {
      if (!node) return { leftX: 0, rightX: 0, centerX: 0 };

      const left = layout(node.left);
      const right = layout(node.right);

      if (!node.left && !node.right) {
        const width = node.el.getBoundingClientRect().width;
        const step = Math.max(nodeGapMin, width + baseGap);
        const center = nextX;
        nextX += step;
        node.centerX = center;
        return { leftX: center, rightX: center, centerX: center };
      }

      if (node.left && !node.right) {
        node.centerX = left.centerX;
        return { leftX: left.leftX, rightX: left.rightX, centerX: node.centerX };
      }

      if (!node.left && node.right) {
        node.centerX = right.centerX;
        return { leftX: right.leftX, rightX: right.rightX, centerX: node.centerX };
      }

      node.centerX = (left.centerX + right.centerX) / 2;
      return { leftX: left.leftX, rightX: right.rightX, centerX: node.centerX };
    };

    layout(root);

    const treeWidth = Math.max(0, nextX - nodeGapMin);
    const stageWidth = Math.max(700, treeWidth + maxChipW * 2);
    const maxLevel = Math.max(...nodes.map((node) => Number(node.dataset.level)));
    const height = topPad + (maxLevel + 1) * levelGap;

    stage.style.width = `${stageWidth}px`;
    stage.style.height = `${height}px`;

    const offsetX = (stageWidth - treeWidth) / 2;

    const applyPositions = (node) => {
      if (!node) return;
      node.el.style.left = `${node.centerX + offsetX}px`;
      node.el.style.top = `${topPad + node.level * levelGap}px`;
      applyPositions(node.left);
      applyPositions(node.right);
    };
    applyPositions(root);

    svg.setAttribute("width", stageWidth);
    svg.setAttribute("height", height);
    svg.setAttribute("viewBox", `0 0 ${stageWidth} ${height}`);
    svg.innerHTML = "";

    nodes.forEach((child) => {
      const parentIdx = child.dataset.parent;
      if (parentIdx == null) return;
      const parent = byIndex[Number(parentIdx)];
      if (!parent) return;

      const pBox = parent.getBoundingClientRect();
      const cBox = child.getBoundingClientRect();
      const sBox = stage.getBoundingClientRect();

      const pCx = pBox.left - sBox.left + pBox.width / 2;
      const cCx = cBox.left - sBox.left + cBox.width / 2;
      const childIndex = Number(child.dataset.index);
      const parentIndex = Number(parentIdx);
      const isLeft = childIndex === parentIndex * 2 + 1;
      const side = isLeft ? -1 : 1;

      const startEdgeOffset = pBox.width * 0.35;
      const startX = pCx + side * startEdgeOffset;
      const startY = pBox.bottom - sBox.top + 2;

      const endX = cCx;
      const endY = cBox.top - sBox.top - 2;

      const maxR = Math.max(pBox.width, cBox.width) / 2;
      const reach = Math.min(0, maxR * 1.8);
      const pull = Math.min(100, maxR * 1.1);

      const c1X = startX + side * reach;
      const c1Y = startY + pull;
      const c2X = endX - side * reach;
      const c2Y = endY - pull;

      const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
      path.setAttribute("d", `M ${startX} ${startY} C ${c1X} ${c1Y}, ${c2X} ${c2Y}, ${endX} ${endY}`);
      path.setAttribute("class", "branch-line");
      svg.appendChild(path);
    });

    const foundEl = stage.querySelector(".found-node");
    if (foundEl) {
      const rect = foundEl.getBoundingClientRect();
      const targetY = window.scrollY + rect.top - (window.innerHeight / 2 - rect.height / 2);
      window.scrollTo({ top: Math.max(0, targetY), behavior: "smooth" });
    }
  };

  window.addEventListener("load", () => {
    requestAnimationFrame(() => requestAnimationFrame(layoutTreeAndBranches));
  });
  window.addEventListener("resize", () => {
    requestAnimationFrame(layoutTreeAndBranches);
  });
})();
