from flask import Blueprint, render_template, request, jsonify, current_app

sorting_blueprint = Blueprint('sorting_blueprint', __name__)


@sorting_blueprint.route('/works/sorting')
def sorting_page():
    site_name = current_app.config.get("SITE_NAME", "Nodeus")
    return render_template("sorting.html", site_name=site_name, page_class="theme-sorting")


# ---------------------------
# Sorting Algorithms (Bubble Sort)
# ---------------------------
def build_bubble_sort_actions(values):
    actions = []
    arr = list(values)
    n = len(arr)

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            actions.append({
                "type": "compare",
                "indices": [j, j + 1],
                "desc": f"Compare {arr[j]} with {arr[j + 1]}."
            })

            if arr[j] > arr[j + 1]:
                actions.append({
                    "type": "swap",
                    "i": j,
                    "j": j + 1,
                    "desc": f"Swap {arr[j]} at index {j} with {arr[j + 1]} at index {j + 1}."
                })
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        actions.append({
            "type": "locked",
            "index": n - 1 - i,
            "desc": f"Value {arr[n - 1 - i]} is now in its sorted position."
        })

        if not swapped:
            break
    actions.append({"type": "done", "desc": "Array sorted."})
    return actions


@sorting_blueprint.route("/works/sorting/bubble-steps", methods=["POST"])
def bubble_sort_steps():
    data = request.get_json(silent=True) or {}
    raw_values = data.get("values", [])

    cleaned = []
    for value in raw_values:
        try:
            num = int(value)
        except (TypeError, ValueError):
            continue
        num = max(2, min(99, num))
        cleaned.append(num)
        if len(cleaned) >= 14:
            break

    actions = build_bubble_sort_actions(cleaned)
    return jsonify({"actions": actions, "values": cleaned})


# ---------------------------
# Sorting Algorithms (Selection Sort)
# ---------------------------
def build_selection_sort_actions(values):
    actions = []
    arr = list(values)

    n = len(arr)
    for i in range(n - 1):
        min_index = i
        actions.append({
            "type": "start_pass",
            "index": i,
            "desc": f"Start pass for position {i}, find min in subarray {i}-{n-1}."
        })
        for j in range(i + 1, n):
            actions.append({
                "type": "compare",
                "indices": [min_index, j],
                "desc": f"Compare current min {arr[min_index]} with {arr[j]}."
            })
            if arr[j] < arr[min_index]:
                min_index = j
                actions.append({
                    "type": "min_found",
                    "index": min_index,
                    "desc": f"New min found: {arr[min_index]} at index {min_index}."
                })
        if min_index != i:
            actions.append({
                "type": "swap",
                "i": i,
                "j": min_index,
                "desc": f"Swap {arr[i]} at index {i} with min {arr[min_index]} at index {min_index}."
            })
            arr[i], arr[min_index] = arr[min_index], arr[i]
        actions.append({
            "type": "sorted",
            "index": i,
            "desc": f"Position {i} is now sorted."
        })

    actions.append({"type": "done", "desc": "Array sorted."})
    return actions


@sorting_blueprint.route("/works/sorting/selection-steps", methods=["POST"])
def selection_sort_steps():
    data = request.get_json(silent=True) or {}
    raw_values = data.get("values", [])

    cleaned = []
    for value in raw_values:
        try:
            num = int(value)
        except (TypeError, ValueError):
            continue
        num = max(2, min(99, num))
        cleaned.append(num)
        if len(cleaned) >= 14:
            break

    actions = build_selection_sort_actions(cleaned)
    return jsonify({"actions": actions, "values": cleaned})


# ---------------------------
# Sorting Algorithms (Quick Sort)
# ---------------------------
def build_quick_sort_actions(values):
    actions = []
    arr = list(values)

    def partition(lo, hi):
        pivot_index = hi
        pivot_value = arr[pivot_index]
        actions.append({
            "type": "pivot",
            "index": pivot_index,
            "desc": f"Pick pivot {pivot_value} at index {pivot_index} (range {lo}-{hi})."
        })

        i = lo
        for j in range(lo, hi):
            actions.append({
                "type": "compare",
                "indices": [j, pivot_index],
                "desc": f"Compare {arr[j]} with pivot {pivot_value}."
            })
            if arr[j] <= pivot_value:
                if i != j:
                    actions.append({
                        "type": "swap",
                        "i": i,
                        "j": j,
                        "desc": f"Swap {arr[i]} at index {i} with {arr[j]} at index {j}."
                    })
                    arr[i], arr[j] = arr[j], arr[i]
                i += 1

        if i != hi:
            actions.append({
                "type": "swap",
                "i": i,
                "j": hi,
                "desc": f"Swap {arr[i]} at index {i} with pivot {arr[hi]} at index {hi}."
            })
            arr[i], arr[hi] = arr[hi], arr[i]

        actions.append({
            "type": "pivot_done",
            "index": i,
            "desc": f"Pivot {pivot_value} placed at index {i}."
        })
        return i

    def quick_sort(lo, hi):
        if lo >= hi:
            return
        actions.append({
            "type": "range",
            "range": [lo, hi],
            "desc": f"Sort subarray indices {lo}-{hi}."
        })
        pivot = partition(lo, hi)
        quick_sort(lo, pivot - 1)
        quick_sort(pivot + 1, hi)

    if arr:
        quick_sort(0, len(arr) - 1)
    actions.append({"type": "done", "desc": "Array sorted."})
    return actions


@sorting_blueprint.route("/works/sorting/quick-steps", methods=["POST"])
def quick_sort_steps():
    data = request.get_json(silent=True) or {}
    raw_values = data.get("values", [])

    cleaned = []
    for value in raw_values:
        try:
            num = int(value)
        except (TypeError, ValueError):
            continue
        num = max(2, min(99, num))
        cleaned.append(num)
        if len(cleaned) >= 14:
            break

    actions = build_quick_sort_actions(cleaned)
    return jsonify({"actions": actions, "values": cleaned})
