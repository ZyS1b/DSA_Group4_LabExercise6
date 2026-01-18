(() => {
  const barsEl = document.getElementById("selection-bars");
  if (!barsEl) return;

  const inputEl = document.getElementById("selection-input");
  const speedEl = document.getElementById("selection-speed");
  const speedLabelEl = document.getElementById("selection-speed-label");
  const countEl = document.getElementById("selection-count");
  const minEl = document.getElementById("selection-min");
  const stepsEl = document.getElementById("selection-steps");
  const stepsListEl = document.getElementById("selection-steps-list");

  const loadBtn = document.getElementById("selection-load");
  const randomBtn = document.getElementById("selection-random");
  const startBtn = document.getElementById("selection-start");
  const resetBtn = document.getElementById("selection-reset");

  const maxBars = 50;
  const defaultValues = [71, 22, 36, 45, 12, 88, 54];

  const baseDelay = 220;
  const state = {
    values: [],
    initial: [],
    actions: [],
    actionIndex: 0,
    running: false,
    speed: parseFloat(speedEl.value) || 1,
    currentStepItem: null
  };

  let stepItems = [];

  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  const getBars = () => Array.from(barsEl.querySelectorAll(".sort-bar"));

  const clearHighlights = () => {
    getBars().forEach((bar) => {
      bar.classList.remove("is-pivot", "is-compare", "is-swap");
    });
  };

  const updateSpeedLabel = () => {
    speedLabelEl.textContent = `${state.speed}x`;
  };

  const setSteps = (current, total) => {
    stepsEl.textContent = `${current}/${total}`;
  };

  const describeAction = (action) => {
    if (action.desc) return action.desc;
    if (action.type === "start_pass") return `Start pass for position ${action.index}.`;
    if (action.type === "compare") return "Compare with current min.";
    if (action.type === "min_found") return `New min found at index ${action.index}.`;
    if (action.type === "swap") return `Swap index ${action.i} with index ${action.j}.`;
    if (action.type === "sorted") return `Position ${action.index} is now sorted.`;
    if (action.type === "done") return "Array sorted.";
    return action.type;
  };

  const clearStepList = () => {
    if (!stepsListEl) return;
    stepsListEl.innerHTML = "";
    stepItems = [];
    state.currentStepItem = null;
  };

  const appendStep = (action) => {
    if (!stepsListEl) return;
    const item = document.createElement("li");
    item.textContent = describeAction(action);
    stepsListEl.appendChild(item);
    stepItems.push(item);
    if (state.currentStepItem) {
      state.currentStepItem.classList.remove("is-current");
    }
    item.classList.add("is-current");
    state.currentStepItem = item;
    stepsListEl.scrollTop = stepsListEl.scrollHeight;
  };

  const parseValues = (raw) => {
    return raw
      .split(/[,\s]+/)
      .map((value) => parseInt(value, 10))
      .filter((value) => Number.isFinite(value));
  };

  const normalizeValues = (values) => {
    const cleaned = values
      .map((value) => Math.max(2, Math.min(99, value)))
      .slice(0, maxBars);
    return cleaned;
  };

  const randomValues = () => {
    const fallbackSize = 8 + Math.floor(Math.random() * 5);
    const desired = parseInt(countEl?.value, 10);
    const size = Number.isFinite(desired) ? desired : fallbackSize;
    const finalSize = Math.max(2, Math.min(maxBars, size));
    const values = Array.from({ length: finalSize }, () => 8 + Math.floor(Math.random() * 80));
    return normalizeValues(values);
  };

  const renderBars = (values) => {
    barsEl.innerHTML = "";
    const maxValue = Math.max(...values);
    values.forEach((value) => {
      const bar = document.createElement("div");
      bar.className = "sort-bar";
      const heightPercent = Math.max(8, (value / maxValue) * 100);
      bar.style.height = `${heightPercent}%`;

      const label = document.createElement("span");
      label.className = "bar-label";
      label.textContent = value;
      bar.appendChild(label);
      barsEl.appendChild(bar);
    });
  };

  const syncBars = (values) => {
    const bars = getBars();
    const maxValue = Math.max(...values);
    bars.forEach((bar, index) => {
      const value = values[index];
      const heightPercent = Math.max(8, (value / maxValue) * 100);
      bar.style.height = `${heightPercent}%`;
      const label = bar.querySelector(".bar-label");
      if (label) label.textContent = value;
    });
  };

  const setValues = (values) => {
    state.values = values.slice();
    state.initial = values.slice();
    state.actions = [];
    state.actionIndex = 0;
    state.running = false;
    minEl.textContent = "-";
    setSteps(0, 0);
    clearStepList();
    renderBars(state.values);
  };

  const selectionSortActions = (values) => {
    const actions = [];
    const n = values.length;
    for (let i = 0; i < n - 1; i += 1) {
      let minIndex = i;
      actions.push({
        type: "start_pass",
        index: i,
        desc: `Start pass for position ${i}, find min in subarray ${i}-${n-1}.`
      });
      for (let j = i + 1; j < n; j += 1) {
        actions.push({
          type: "compare",
          indices: [minIndex, j],
          desc: `Compare current min ${values[minIndex]} with ${values[j]}.`
        });
        if (values[j] < values[minIndex]) {
          minIndex = j;
          actions.push({
            type: "min_found",
            index: minIndex,
            desc: `New min found: ${values[minIndex]} at index ${minIndex}.`
          });
        }
      }
      if (minIndex !== i) {
        actions.push({
          type: "swap",
          i,
          j: minIndex,
          desc: `Swap ${values[i]} at index ${i} with min ${values[minIndex]} at index ${minIndex}.`
        });
        [values[i], values[minIndex]] = [values[minIndex], values[i]];
      }
      actions.push({
        type: "sorted",
        index: i,
        desc: `Position ${i} is now sorted.`
      });
    }
    actions.push({ type: "done", desc: "Array sorted." });
    return actions;
  };

  const fetchActions = async (values) => {
    try {
      const response = await fetch("/works/sorting/selection-steps", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ values })
      });
      if (!response.ok) throw new Error("Request failed");
      const data = await response.json();
      if (!data || !Array.isArray(data.actions)) throw new Error("Bad payload");
      const returnedValues = Array.isArray(data.values) ? data.values : values;
      return { actions: data.actions, values: returnedValues };
    } catch (error) {
      return { actions: selectionSortActions(values.slice()), values };
    }
  };

  const animateSwap = (i, j) => {
    const bars = getBars();
    const barA = bars[i];
    const barB = bars[j];
    if (!barA || !barB || barA === barB) return Promise.resolve();

    const rectA = barA.getBoundingClientRect();
    const rectB = barB.getBoundingClientRect();

    const parent = barsEl;
    const barA_next = barA.nextSibling;
    const barB_next = barB.nextSibling;
    parent.insertBefore(barB, barA_next);
    parent.insertBefore(barA, barB_next);

    const rectA_after = barA.getBoundingClientRect();
    const rectB_after = barB.getBoundingClientRect();

    const deltaA = rectA.left - rectA_after.left;
    const deltaB = rectB.left - rectB_after.left;

    barA.style.transition = "none";
    barB.style.transition = "none";
    barA.style.transform = `translateX(${deltaA}px)`;
    barB.style.transform = `translateX(${deltaB}px)`;
    barA.getBoundingClientRect();

    barA.style.transition = "transform 200ms var(--ease)";
    barB.style.transition = "transform 200ms var(--ease)";
    barA.style.transform = "";
    barB.style.transform = "";

    return new Promise((resolve) => {
      let done = 0;
      const finish = () => {
        done += 1;
        if (done < 2) return;
        barA.style.transition = "";
        barB.style.transition = "";
        resolve();
      };
      barA.addEventListener("transitionend", finish, { once: true });
      barB.addEventListener("transitionend", finish, { once: true });
      setTimeout(finish, 260);
    });
  };

  const applyAction = async (action) => {
    const bars = getBars();
    clearHighlights();

    if (action.type === "start_pass") {
      minEl.textContent = state.values[action.index];
      if (bars[action.index]) bars[action.index].classList.add("is-pivot");
      return;
    }

    if (action.type === "compare") {
      action.indices.forEach((index) => {
        if (bars[index]) bars[index].classList.add("is-compare");
      });
      return;
    }

    if (action.type === "min_found") {
      minEl.textContent = state.values[action.index];
      if (bars[action.index]) bars[action.index].classList.add("is-pivot");
      return;
    }

    if (action.type === "swap") {
      if (bars[action.i]) bars[action.i].classList.add("is-swap");
      if (bars[action.j]) bars[action.j].classList.add("is-swap");
      [state.values[action.i], state.values[action.j]] = [state.values[action.j], state.values[action.i]];
      await animateSwap(action.i, action.j);
      return;
    }

    if (action.type === "sorted") {
      if (bars[action.index]) bars[action.index].classList.add("is-sorted");
      return;
    }

    if (action.type === "done") {
      bars.forEach((bar) => bar.classList.add("is-sorted"));
      minEl.textContent = "-";
    }
  };

  const setControlsDisabled = (disabled) => {
    inputEl.disabled = disabled;
    loadBtn.disabled = disabled;
    randomBtn.disabled = disabled;
    startBtn.disabled = disabled;
  };

  const runAnimation = async () => {
    if (state.running) return;
    if (state.initial.length < 2) return;

    state.running = true;
    setControlsDisabled(true);

    const sourceValues = state.values.length ? state.values : state.initial;
    const response = await fetchActions(sourceValues.slice());
    state.actions = response.actions;
    state.actionIndex = 0;
    state.values = response.values.slice();
    state.initial = response.values.slice();
    renderBars(state.values);
    clearHighlights();
    setSteps(0, state.actions.length);

    for (; state.actionIndex < state.actions.length; state.actionIndex += 1) {
      if (!state.running) break;
      appendStep(state.actions[state.actionIndex]);
      await applyAction(state.actions[state.actionIndex]);
      setSteps(state.actionIndex + 1, state.actions.length);
      await sleep(baseDelay / state.speed);
    }

    state.running = false;
    setControlsDisabled(false);
  };

  const resetVisualization = () => {
    state.running = false;
    setControlsDisabled(false);
    setValues(state.initial.length ? state.initial : defaultValues);
  };

  loadBtn.addEventListener("click", () => {
    if (state.running) return;
    const parsed = normalizeValues(parseValues(inputEl.value));
    const values = parsed.length ? parsed : defaultValues;
    inputEl.value = values.join(", ");
    setValues(values);
  });

  randomBtn.addEventListener("click", () => {
    if (state.running) return;
    const values = randomValues();
    inputEl.value = values.join(", ");
    setValues(values);
  });

  startBtn.addEventListener("click", () => {
    runAnimation();
  });

  resetBtn.addEventListener("click", () => {
    resetVisualization();
  });

  speedEl.addEventListener("input", (event) => {
    const nextValue = parseFloat(event.target.value);
    state.speed = Number.isFinite(nextValue) ? nextValue : 1;
    updateSpeedLabel();
  });

  updateSpeedLabel();
  inputEl.value = defaultValues.join(", ");
  setValues(defaultValues);
})();
