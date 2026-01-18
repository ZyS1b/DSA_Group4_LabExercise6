(() => {
  const barsEl = document.getElementById("merge-bars");
  if (!barsEl) return;

  const inputEl = document.getElementById("merge-input");
  const speedEl = document.getElementById("merge-speed");
  const speedLabelEl = document.getElementById("merge-speed-label");
  const countEl = document.getElementById("merge-count");
  const stepsEl = document.getElementById("merge-steps");
  const stepsListEl = document.getElementById("merge-steps-list");
  const stepSliderEl = document.getElementById("merge-step-slider");
  const playBtn = document.getElementById("merge-play");
  const stopBtn = document.getElementById("merge-stop");
  const prevBtn = document.getElementById("merge-prev");
  const nextBtn = document.getElementById("merge-next");
  const firstBtn = document.getElementById("merge-first");
  const lastBtn = document.getElementById("merge-end");

  const loadBtn = document.getElementById("merge-load");
  const randomBtn = document.getElementById("merge-random");
  const startBtn = document.getElementById("merge-start");
  const resetBtn = document.getElementById("merge-reset");

  const algoId = "merge";
  const maxBars = 50;
  const defaultValues = [42, 16, 8, 23, 4, 15, 9, 50];
  const storageKey = "sorting-values";

  const baseDelay = 220;
  const state = {
    values: [],
    items: [],
    initialItems: [],
    initial: [],
    actions: [],
    actionIndex: 0,
    running: false,
    speed: parseFloat(speedEl.value) || 1,
    currentStepItem: null,
    paused: false,
    stopRequested: false
  };

  let stepItems = [];
  const playIcon = '<svg class="media-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5l11 7-11 7V5z"/></svg>';
  const pauseIcon = '<svg class="media-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 5h4v14H7V5zm6 0h4v14h-4V5z"/></svg>';

  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  const getBars = () => Array.from(barsEl.querySelectorAll(".sort-bar"));

  const clearHighlights = () => {
    getBars().forEach((bar) => {
      bar.classList.remove("is-compare", "is-swap");
    });
  };

  const updateSpeedLabel = () => {
    speedLabelEl.textContent = `${state.speed}x`;
  };

  const setSteps = (current, total) => {
    stepsEl.textContent = `${current}/${total}`;
  };

  const setPlayState = (isPlaying) => {
    if (!playBtn) return;
    playBtn.innerHTML = isPlaying ? pauseIcon : playIcon;
    playBtn.setAttribute("aria-label", isPlaying ? "Pause" : "Play");
  };

  const updateStepSlider = () => {
    if (!stepSliderEl) return;
    stepSliderEl.max = state.actions.length;
    stepSliderEl.value = state.actionIndex;
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

  const renderStepList = (stepIndex) => {
    if (!stepsListEl) return;
    stepsListEl.innerHTML = "";
    stepItems = [];
    state.currentStepItem = null;
    for (let i = 0; i < stepIndex; i += 1) {
      const item = document.createElement("li");
      item.textContent = describeAction(state.actions[i]);
      if (i === stepIndex - 1) {
        item.classList.add("is-current");
        state.currentStepItem = item;
      }
      stepsListEl.appendChild(item);
      stepItems.push(item);
    }
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
      .map((value) => Math.max(1, Math.min(99, value)))
      .slice(0, maxBars);
    return cleaned;
  };

  const loadStoredValues = () => {
    try {
      const raw = localStorage.getItem(storageKey);
      if (!raw) return null;
      const parsed = JSON.parse(raw);
      if (!Array.isArray(parsed)) return null;
      const cleaned = normalizeValues(parsed);
      return cleaned.length ? cleaned : null;
    } catch (error) {
      return null;
    }
  };

  const saveStoredValues = (values) => {
    try {
      localStorage.setItem(storageKey, JSON.stringify(values));
    } catch (error) {
      return;
    }
  };

  const randomValues = () => {
    const fallbackSize = 8 + Math.floor(Math.random() * 5);
    const desired = parseInt(countEl?.value, 10);
    const size = Number.isFinite(desired) ? desired : fallbackSize;
    const finalSize = Math.max(1, Math.min(maxBars, size));
    const values = Array.from({ length: finalSize }, () => 8 + Math.floor(Math.random() * 80));
    return normalizeValues(values);
  };

  const renderBars = (items) => {
    barsEl.innerHTML = "";
    const maxValue = Math.max(...items.map((item) => item.value));
    items.forEach((item) => {
      const bar = document.createElement("div");
      bar.className = "sort-bar";
      bar.dataset.id = item.id;
      const heightPercent = Math.max(8, (item.value / maxValue) * 100);
      bar.style.height = `${heightPercent}%`;

      const label = document.createElement("span");
      label.className = "bar-label";
      label.textContent = item.value;
      bar.appendChild(label);
      barsEl.appendChild(bar);
    });
  };

  const syncBars = (items) => {
    const bars = getBars();
    const maxValue = Math.max(...items.map((item) => item.value));
    bars.forEach((bar, index) => {
      const item = items[index];
      if (!item) return;
      const heightPercent = Math.max(8, (item.value / maxValue) * 100);
      bar.style.height = `${heightPercent}%`;
      bar.dataset.id = item.id;
      const label = bar.querySelector(".bar-label");
      if (label) label.textContent = item.value;
    });
  };

  const setValues = (values, options = {}) => {
    const items = values.map((value, index) => ({
      id: `m-${Date.now()}-${index}-${Math.random().toString(16).slice(2)}`,
      value
    }));
    state.values = values.slice();
    state.items = items.slice();
    state.initialItems = items.map((item) => ({ ...item }));
    state.initial = values.slice();
    state.actions = [];
    state.actionIndex = 0;
    state.running = false;
    setSteps(0, 0);
    clearStepList();
    renderBars(state.items);
    updateStepSlider();
    if (!options.silent) {
      saveStoredValues(state.values);
      window.dispatchEvent(new CustomEvent("sorting-values-updated", {
        detail: { values: state.values, source: algoId }
      }));
    }
  };

  const mergeSortActions = (items) => {
    const actions = [];
    const arr = items.map((item) => ({ ...item }));

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
        let item;
        if (i >= left.length) {
          item = right[j];
          j += 1;
        } else if (j >= right.length) {
          item = left[i];
          i += 1;
        } else {
          actions.push({
            type: "compare",
            indices: [lo + i, mid + 1 + j],
            desc: `Compare ${left[i].value} with ${right[j].value}.`
          });
          if (left[i].value <= right[j].value) {
            item = left[i];
            i += 1;
          } else {
            item = right[j];
            j += 1;
          }
        }
        actions.push({
          type: "write",
          index: k,
          id: item.id,
          value: item.value,
          desc: `Write ${item.value} to index ${k}.`
        });
        arr[k] = item;
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

  const fetchActions = async () => {
    return { actions: mergeSortActions(state.items), values: state.values };
  };

  const animateMove = (id, toIndex) => {
    const bars = getBars();
    const bar = bars.find((node) => node.dataset.id === id);
    if (!bar) return Promise.resolve();
    const currentIndex = bars.indexOf(bar);
    if (currentIndex === toIndex) return Promise.resolve();

    const rectBefore = bar.getBoundingClientRect();
    const refBar = bars[toIndex];
    if (toIndex >= bars.length - 1) {
      barsEl.appendChild(bar);
    } else if (toIndex < currentIndex) {
      barsEl.insertBefore(bar, refBar);
    } else {
      barsEl.insertBefore(bar, refBar.nextSibling);
    }

    const rectAfter = bar.getBoundingClientRect();
    const deltaX = rectBefore.left - rectAfter.left;

    bar.style.transition = "none";
    bar.style.transform = `translateX(${deltaX}px)`;
    bar.getBoundingClientRect();

    bar.style.transition = "transform 200ms ease-in-out";
    bar.style.transform = "";

    return new Promise((resolve) => {
      const finish = () => {
        bar.style.transition = "";
        resolve();
      };
      bar.addEventListener("transitionend", finish, { once: true });
      setTimeout(finish, 260);
    });
  };

  const applyActionInstant = (action) => {
    const bars = getBars();
    clearHighlights();

    if (action.type === "compare") {
      action.indices.forEach((index) => {
        if (bars[index]) bars[index].classList.add("is-compare");
      });
      return;
    }

    if (action.type === "write") {
      const movedIndex = state.items.findIndex((item) => item.id === action.id);
      if (movedIndex >= 0) {
        const [moved] = state.items.splice(movedIndex, 1);
        moved.value = action.value;
        state.items.splice(action.index, 0, moved);
        state.values = state.items.map((item) => item.value);
        syncBars(state.items);
      }
      return;
    }

    if (action.type === "range") {
      return;
    }

    if (action.type === "done") {
      bars.forEach((bar) => bar.classList.add("is-sorted"));
    }
  };

  const applyAction = async (action, options = {}) => {
    if (options.instant) {
      applyActionInstant(action);
      return;
    }
    const bars = getBars();
    clearHighlights();

    if (action.type === "compare") {
      action.indices.forEach((index) => {
        if (bars[index]) bars[index].classList.add("is-compare");
      });
      return;
    }

    if (action.type === "write") {
      const movedIndex = state.items.findIndex((item) => item.id === action.id);
      if (movedIndex >= 0) {
        const [moved] = state.items.splice(movedIndex, 1);
        moved.value = action.value;
        state.items.splice(action.index, 0, moved);
        state.values = state.items.map((item) => item.value);
        await animateMove(action.id, action.index);
        syncBars(state.items);
      }
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

  const ensureActions = async () => {
    if (state.actions.length) return;
    const response = await fetchActions();
    state.actions = response.actions;
    state.actionIndex = 0;
    state.values = response.values.slice();
    state.initial = response.values.slice();
    state.items = state.initialItems.map((item) => ({ ...item }));
    renderBars(state.items);
    clearHighlights();
    setSteps(0, state.actions.length);
    updateStepSlider();
  };

  const renderAtStep = (stepIndex) => {
    state.values = state.initial.slice();
    state.items = state.initialItems.map((item) => ({ ...item }));
    renderBars(state.items);
    clearHighlights();
    const clamped = Math.max(0, Math.min(stepIndex, state.actions.length));
    for (let i = 0; i < clamped; i += 1) {
      applyActionInstant(state.actions[i]);
    }
    state.actionIndex = clamped;
    setSteps(clamped, state.actions.length);
    updateStepSlider();
    renderStepList(clamped);
  };

  const stepTo = async (stepIndex, options = {}) => {
    await ensureActions();
    const clamped = Math.max(0, Math.min(stepIndex, state.actions.length));
    const forwardAction = state.actions[state.actionIndex];
    if (options.animate && clamped === state.actionIndex + 1 && forwardAction) {
      if (forwardAction.type === "write") {
        await applyAction(forwardAction);
        state.actionIndex = clamped;
        setSteps(clamped, state.actions.length);
        updateStepSlider();
        renderStepList(clamped);
        return;
      }
    }
    renderAtStep(clamped);
  };

  const runAnimation = async () => {
    if (state.running) return;
    if (state.initial.length < 2) return;

    state.running = true;
    state.paused = false;
    state.stopRequested = false;
    setPlayState(true);
    setControlsDisabled(true);

    await ensureActions();

    for (; state.actionIndex < state.actions.length; state.actionIndex += 1) {
      if (state.stopRequested) break;
      while (state.paused) {
        await sleep(80);
        if (state.stopRequested) break;
      }
      if (state.stopRequested) break;
      appendStep(state.actions[state.actionIndex]);
      await applyAction(state.actions[state.actionIndex]);
      setSteps(state.actionIndex + 1, state.actions.length);
      updateStepSlider();
      await sleep(baseDelay / state.speed);
    }

    state.running = false;
    state.paused = false;
    setPlayState(false);
    setControlsDisabled(false);
  };

  const resetVisualization = () => {
    state.running = false;
    setControlsDisabled(false);
    setPlayState(false);
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

  inputEl.addEventListener("input", () => {
    inputEl.value = inputEl.value.replace(/[^0-9,\\s]/g, "");
  });

  startBtn.addEventListener("click", () => {
    runAnimation();
  });

  resetBtn.addEventListener("click", () => {
    resetVisualization();
  });

  playBtn?.addEventListener("click", async () => {
    if (state.running) {
      state.paused = !state.paused;
      setPlayState(!state.paused);
      return;
    }
    await runAnimation();
  });

  stopBtn?.addEventListener("click", async () => {
    state.stopRequested = true;
    state.running = false;
    state.paused = false;
    setPlayState(false);
    await ensureActions();
    renderAtStep(0);
    setControlsDisabled(false);
  });

  firstBtn?.addEventListener("click", async () => {
    await ensureActions();
    state.paused = true;
    setPlayState(false);
    renderAtStep(0);
  });

  prevBtn?.addEventListener("click", async () => {
    state.paused = true;
    setPlayState(false);
    await stepTo(state.actionIndex - 1, { animate: true });
  });

  nextBtn?.addEventListener("click", async () => {
    state.paused = true;
    setPlayState(false);
    await stepTo(state.actionIndex + 1, { animate: true });
  });

  lastBtn?.addEventListener("click", async () => {
    await ensureActions();
    state.paused = true;
    setPlayState(false);
    renderAtStep(state.actions.length);
  });

  stepSliderEl?.addEventListener("input", async (event) => {
    state.paused = true;
    setPlayState(false);
    const nextValue = parseInt(event.target.value, 10);
    await stepTo(Number.isFinite(nextValue) ? nextValue : 0, { animate: true });
  });

  speedEl.addEventListener("input", (event) => {
    const nextValue = parseFloat(event.target.value);
    state.speed = Number.isFinite(nextValue) ? nextValue : 1;
    updateSpeedLabel();
  });

  window.addEventListener("sorting-values-updated", (event) => {
    if (!event.detail || event.detail.source === algoId) return;
    if (state.running) return;
    const incoming = normalizeValues(event.detail.values || []);
    if (!incoming.length) return;
    inputEl.value = incoming.join(", ");
    setValues(incoming, { silent: true });
  });

  updateSpeedLabel();
  setPlayState(false);
  const storedValues = loadStoredValues();
  const startValues = storedValues && storedValues.length ? storedValues : defaultValues;
  inputEl.value = startValues.join(", ");
  setValues(startValues, { silent: true });
})();
