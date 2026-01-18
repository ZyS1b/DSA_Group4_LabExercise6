(() => {
  const barsEl = document.getElementById("merge-bars");
  if (!barsEl) return;

  const inputEl = document.getElementById("merge-input");
  const speedEl = document.getElementById("merge-speed");
  const speedLabelEl = document.getElementById("merge-speed-label");
  const stepsEl = document.getElementById("merge-steps");
  const stepsListEl = document.getElementById("merge-steps-list");

  const loadBtn = document.getElementById("merge-load");
  const randomBtn = document.getElementById("merge-random");
  const startBtn = document.getElementById("merge-start");
  const resetBtn = document.getElementById("merge-reset");

  const maxBars = 14;
  const defaultValues = [42, 16, 8, 23, 4, 15, 9, 50];

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
      bar.classList.remove("is-compare", "is-swap");
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
    if (action.type === "compare") return `Compare indices ${action.indices[0]} and ${action.indices[1]}.`;
    if (action.type === "write") return `Write ${action.value} to index ${action.index}.`;
    if (action.type === "range") return `Merge subarray indices ${action.range[0]}-${action.range[1]}.`;
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
    setSteps(0, 0);
    clearStepList();
    renderBars(state.values);
  };

  const mergeSortActions = (values) => {
    const actions = [];
    const arr = values.slice();

    const merge = (lo, mid, hi) => {
      actions.push({
        type: "range",
        range: [lo, hi],
        desc: `Merge subarray indices ${lo}-${hi}.`
      });
      const left = arr.slice(lo, mid + 1);
      const right = arr.slice(mid + 1, hi + 1);
      let i = 0;
      let j = 0;
      for (let k = lo; k <= hi; k += 1) {
        let value;
        if (i >= left.length) {
          value = right[j];
          j += 1;
        } else if (j >= right.length) {
          value = left[i];
          i += 1;
        } else {
          actions.push({
            type: "compare",
            indices: [lo + i, mid + 1 + j],
            desc: `Compare ${left[i]} with ${right[j]}.`
          });
          if (left[i] <= right[j]) {
            value = left[i];
            i += 1;
          } else {
            value = right[j];
            j += 1;
          }
        }
        actions.push({
          type: "write",
          index: k,
          value,
          desc: `Write ${value} to index ${k}.`
        });
        arr[k] = value;
      }
    };

    const mergeSort = (lo, hi) => {
      if (lo >= hi) return;
      const mid = Math.floor((lo + hi) / 2);
      mergeSort(lo, mid);
      mergeSort(mid + 1, hi);
      merge(lo, mid, hi);
    };

    if (arr.length) {
      mergeSort(0, arr.length - 1);
    }
    actions.push({ type: "done", desc: "Array sorted." });
    return actions;
  };

  const fetchActions = async (values) => {
    try {
      const response = await fetch("/works/sorting/merge-steps", {
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
      return { actions: mergeSortActions(values.slice()), values };
    }
  };

  const applyAction = (action) => {
    const bars = getBars();
    clearHighlights();

    if (action.type === "compare") {
      action.indices.forEach((index) => {
        if (bars[index]) bars[index].classList.add("is-compare");
      });
      return;
    }

    if (action.type === "write") {
      if (bars[action.index]) bars[action.index].classList.add("is-swap");
      state.values[action.index] = action.value;
      syncBars(state.values);
      return;
    }

    if (action.type === "range") {
      return;
    }

    if (action.type === "done") {
      bars.forEach((bar) => bar.classList.add("is-sorted"));
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
