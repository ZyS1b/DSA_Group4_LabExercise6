(() => {
  const barsEl = document.getElementById("insertion-bars");
  if (!barsEl) return;

  const inputEl = document.getElementById("insertion-input");
  const speedEl = document.getElementById("insertion-speed");
  const speedLabelEl = document.getElementById("insertion-speed-label");
  const countEl = document.getElementById("insertion-count");
  const stepsEl = document.getElementById("insertion-steps");
  const stepsListEl = document.getElementById("insertion-steps-list");
  const stepSliderEl = document.getElementById("insertion-step-slider");
  const playBtn = document.getElementById("insertion-play");
  const stopBtn = document.getElementById("insertion-stop");
  const prevBtn = document.getElementById("insertion-prev");
  const nextBtn = document.getElementById("insertion-next");
  const firstBtn = document.getElementById("insertion-first");
  const lastBtn = document.getElementById("insertion-end");

  const loadBtn = document.getElementById("insertion-load");
  const randomBtn = document.getElementById("insertion-random");
  const startBtn = document.getElementById("insertion-start");
  const resetBtn = document.getElementById("insertion-reset");

  const algoId = "insertion";
  const maxBars = 50;
  const defaultValues = [29, 12, 33, 5, 17, 9, 41, 21];
  const storageKey = "sorting-values";
  const baseDelay = 220;

  const state = {
    values: [],
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
      bar.classList.remove("is-pivot", "is-compare", "is-swap");
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
    if (action.type === "key") return `Select key at index ${action.index}.`;
    if (action.type === "compare") return `Compare indices ${action.indices[0]} and ${action.indices[1]}.`;
    if (action.type === "swap") return `Swap index ${action.i} with index ${action.j}.`;
    if (action.type === "locked") return `Value at index ${action.index} is sorted.`;
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
      .map((value) => Math.max(2, Math.min(99, value)))
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

  const setValues = (values, options = {}) => {
    state.values = values.slice();
    state.initial = values.slice();
    state.actions = [];
    state.actionIndex = 0;
    state.running = false;
    setSteps(0, 0);
    clearStepList();
    renderBars(state.values);
    updateStepSlider();
    if (!options.silent) {
      saveStoredValues(state.values);
      window.dispatchEvent(new CustomEvent("sorting-values-updated", {
        detail: { values: state.values, source: algoId }
      }));
    }
  };

  const insertionSortActions = (values) => {
    const actions = [];
    const arr = values.slice();
    for (let i = 1; i < arr.length; i += 1) {
      actions.push({
        type: "key",
        index: i,
        desc: `Select key ${arr[i]} at index ${i}.`
      });
      let j = i;
      while (j > 0 && arr[j - 1] > arr[j]) {
        actions.push({
          type: "compare",
          indices: [j - 1, j],
          desc: `Compare ${arr[j - 1]} with ${arr[j]}.`
        });
        actions.push({
          type: "swap",
          i: j - 1,
          j,
          desc: `Swap ${arr[j - 1]} at index ${j - 1} with ${arr[j]} at index ${j}.`
        });
        [arr[j - 1], arr[j]] = [arr[j], arr[j - 1]];
        j -= 1;
      }
      actions.push({
        type: "locked",
        index: j,
        desc: `Position ${j} is now sorted.`
      });
    }
    actions.push({ type: "done", desc: "Array sorted." });
    return actions;
  };

  const fetchActions = async (values) => {
    try {
      const response = await fetch("/works/sorting/insertion-steps", {
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
      return { actions: insertionSortActions(values.slice()), values };
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

    barA.style.transition = "transform 200ms ease-in-out";
    barB.style.transition = "transform 200ms ease-in-out";
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

  const applyActionInstant = (action) => {
    const bars = getBars();
    clearHighlights();

    if (action.type === "key") {
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

    if (action.type === "locked") {
      if (bars[action.index]) bars[action.index].classList.add("is-sorted");
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

    if (action.type === "key") {
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
      await animateSwap(action.i, action.j);
      return;
    }

    if (action.type === "locked") {
      if (bars[action.index]) bars[action.index].classList.add("is-sorted");
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
    const sourceValues = state.values.length ? state.values : state.initial;
    const response = await fetchActions(sourceValues.slice());
    state.actions = response.actions;
    state.actionIndex = 0;
    state.values = response.values.slice();
    state.initial = response.values.slice();
    renderBars(state.values);
    clearHighlights();
    setSteps(0, state.actions.length);
    updateStepSlider();
  };

  const renderAtStep = (stepIndex) => {
    state.values = state.initial.slice();
    renderBars(state.values);
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
    await ensureActions();
    state.paused = true;
    setPlayState(false);
    renderAtStep(state.actionIndex - 1);
  });

  nextBtn?.addEventListener("click", async () => {
    await ensureActions();
    state.paused = true;
    setPlayState(false);
    renderAtStep(state.actionIndex + 1);
  });

  lastBtn?.addEventListener("click", async () => {
    await ensureActions();
    state.paused = true;
    setPlayState(false);
    renderAtStep(state.actions.length);
  });

  stepSliderEl?.addEventListener("input", async (event) => {
    await ensureActions();
    state.paused = true;
    setPlayState(false);
    const nextValue = parseInt(event.target.value, 10);
    renderAtStep(Number.isFinite(nextValue) ? nextValue : 0);
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
