(() => {
  const barsEl = document.getElementById("quick-bars");
  if (!barsEl) return;

  const inputEl = document.getElementById("quick-input");
  const speedEl = document.getElementById("quick-speed");
  const speedLabelEl = document.getElementById("quick-speed-label");
  const pivotEl = document.getElementById("quick-pivot");
  const stepsEl = document.getElementById("quick-steps");
  const stepsListEl = document.getElementById("quick-steps-list");

  const loadBtn = document.getElementById("quick-load");
  const randomBtn = document.getElementById("quick-random");
  const startBtn = document.getElementById("quick-start");
  const resetBtn = document.getElementById("quick-reset");

  const maxBars = 14;
  const defaultValues = [32, 11, 5, 26, 18, 9, 41, 15];

  const state = {
    values: [],
    initial: [],
    actions: [],
    actionIndex: 0,
    running: false,
    speed: parseInt(speedEl.value, 10) || 220,
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
    speedLabelEl.textContent = `${state.speed}ms`;
  };

  const setSteps = (current, total) => {
    stepsEl.textContent = `${current}/${total}`;
  };

  const describeAction = (action) => {
    if (action.desc) return action.desc;
    if (action.type === "pivot") return `Pick pivot at index ${action.index}.`;
    if (action.type === "compare") return "Compare with pivot.";
    if (action.type === "swap") return `Swap index ${action.i} with index ${action.j}.`;
    if (action.type === "pivot_done") return `Pivot placed at index ${action.index}.`;
    if (action.type === "range") return `Sort subarray indices ${action.range[0]}-${action.range[1]}.`;
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
    item.scrollIntoView({ block: "nearest" });
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
    const size = 8 + Math.floor(Math.random() * 5);
    const values = Array.from({ length: size }, () => 8 + Math.floor(Math.random() * 80));
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
    pivotEl.textContent = "-";
    setSteps(0, 0);
    clearStepList();
    renderBars(state.values);
  };

  const quickSortActions = (values) => {
    const actions = [];

    const partition = (lo, hi) => {
      const pivotIndex = hi;
      const pivotValue = values[pivotIndex];
      actions.push({
        type: "pivot",
        index: pivotIndex,
        desc: `Pick pivot ${pivotValue} at index ${pivotIndex} (range ${lo}-${hi}).`
      });

      let i = lo;
      for (let j = lo; j < hi; j += 1) {
        actions.push({
          type: "compare",
          indices: [j, pivotIndex],
          desc: `Compare ${values[j]} with pivot ${pivotValue}.`
        });
        if (values[j] <= pivotValue) {
          if (i !== j) {
            actions.push({
              type: "swap",
              i,
              j,
              desc: `Swap ${values[i]} at index ${i} with ${values[j]} at index ${j}.`
            });
            [values[i], values[j]] = [values[j], values[i]];
          }
          i += 1;
        }
      }

      if (i !== hi) {
        actions.push({
          type: "swap",
          i,
          j: hi,
          desc: `Swap ${values[i]} at index ${i} with pivot ${values[hi]} at index ${hi}.`
        });
        [values[i], values[hi]] = [values[hi], values[i]];
      }

      actions.push({
        type: "pivot_done",
        index: i,
        desc: `Pivot ${pivotValue} placed at index ${i}.`
      });
      return i;
    };

    const quickSort = (lo, hi) => {
      if (lo >= hi) return;
      actions.push({
        type: "range",
        range: [lo, hi],
        desc: `Sort subarray indices ${lo}-${hi}.`
      });
      const pivot = partition(lo, hi);
      quickSort(lo, pivot - 1);
      quickSort(pivot + 1, hi);
    };

    quickSort(0, values.length - 1);
    actions.push({ type: "done", desc: "Array sorted." });
    return actions;
  };

  const fetchActions = async (values) => {
    try {
      const response = await fetch("/works/sorting/quick-steps", {
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
      return { actions: quickSortActions(values.slice()), values };
    }
  };

  const applyAction = (action) => {
    const bars = getBars();
    clearHighlights();

    if (action.type === "pivot") {
      pivotEl.textContent = state.values[action.index];
      if (bars[action.index]) bars[action.index].classList.add("is-pivot");
      return;
    }

    if (action.type === "compare") {
      action.indices.forEach((index) => {
        if (bars[index]) bars[index].classList.add("is-compare");
      });
      return;
    }

    if (action.type === "swap") {
      if (bars[action.i]) bars[action.i].classList.add("is-swap");
      if (bars[action.j]) bars[action.j].classList.add("is-swap");
      [state.values[action.i], state.values[action.j]] = [state.values[action.j], state.values[action.i]];
      syncBars(state.values);
      return;
    }

    if (action.type === "pivot_done") {
      if (bars[action.index]) bars[action.index].classList.add("is-sorted");
      pivotEl.textContent = state.values[action.index];
      return;
    }

    if (action.type === "range") {
      return;
    }

    if (action.type === "done") {
      bars.forEach((bar) => bar.classList.add("is-sorted"));
      pivotEl.textContent = "-";
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

    const response = await fetchActions(state.initial.slice());
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
      applyAction(state.actions[state.actionIndex]);
      setSteps(state.actionIndex + 1, state.actions.length);
      await sleep(state.speed);
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
    const nextValue = parseInt(event.target.value, 10);
    state.speed = Number.isFinite(nextValue) ? nextValue : 220;
    updateSpeedLabel();
  });

  updateSpeedLabel();
  inputEl.value = defaultValues.join(", ");
  setValues(defaultValues);
})();
