from .data_structures import RailGraph


def build_rail_graph_with_map():
    g = RailGraph()

    mrt3 = [
        "North Avenue", "Quezon Avenue", "GMA-Kamuning", "Araneta Center-Cubao (MRT-3)",
        "Santolan-Annapolis", "Ortigas", "Shaw Boulevard", "Boni", "Guadalupe",
        "Buendia", "Ayala", "Magallanes", "Taft Avenue"
    ]
    lrt2 = [
        "Recto", "Legarda", "Pureza", "V. Mapa", "J. Ruiz", "Gilmore",
        "Betty Go-Belmonte", "Araneta Center-Cubao (LRT-2)", "Anonas", "Katipunan",
        "Santolan", "Marikina-Pasig", "Antipolo"
    ]
    lrt1 = [
        "Fernando Poe Jr.", "Balintawak", "Monumento", "5th Avenue", "R. Papa",
        "Abad Santos", "Blumentritt", "Tayuman", "Bambang", "Doroteo Jose",
        "Carriedo", "Central Terminal", "United Nations", "Pedro Gil", "Quirino",
        "Vito Cruz", "Gil Puyat", "Libertad", "EDSA", "Baclaran",
        "Redemptorist-Aseana", "MIA Road", "PITX", "Ninoy Aquino Avenue", "Dr. Santos"
    ]

    g.add_line(mrt3)
    g.add_line(lrt2)
    g.add_line(lrt1)

    transfers = [
        ("Doroteo Jose", "Recto"),
        ("Araneta Center-Cubao (MRT-3)", "Araneta Center-Cubao (LRT-2)"),
        ("EDSA", "Taft Avenue"),
    ]

    for a, b in transfers:
        g.add_edge(a, b)

    coords = {
        "Fernando Poe Jr.": {"x": 335, "y": 70},
        "Balintawak": {"x": 295, "y": 92},
        "Monumento": {"x": 260, "y": 114},
        "5th Avenue": {"x": 230, "y": 136},
        "R. Papa": {"x": 205, "y": 158},
        "Abad Santos": {"x": 185, "y": 180},
        "Blumentritt": {"x": 170, "y": 202},
        "Tayuman": {"x": 160, "y": 224},
        "Bambang": {"x": 150, "y": 246},
        "Doroteo Jose": {"x": 140, "y": 268},
        "Carriedo": {"x": 130, "y": 290},
        "Central Terminal": {"x": 120, "y": 312},
        "United Nations": {"x": 115, "y": 334},
        "Pedro Gil": {"x": 110, "y": 356},
        "Quirino": {"x": 110, "y": 378},
        "Vito Cruz": {"x": 110, "y": 400},
        "Gil Puyat": {"x": 120, "y": 422},
        "Libertad": {"x": 130, "y": 444},
        "EDSA": {"x": 140, "y": 466},
        "Baclaran": {"x": 150, "y": 488},
        "Redemptorist-Aseana": {"x": 170, "y": 510},
        "MIA Road": {"x": 200, "y": 532},
        "PITX": {"x": 240, "y": 554},
        "Ninoy Aquino Avenue": {"x": 290, "y": 576},
        "Dr. Santos": {"x": 350, "y": 598},
        "Recto": {"x": 200, "y": 268},
        "Legarda": {"x": 270, "y": 268},
        "Pureza": {"x": 340, "y": 268},
        "V. Mapa": {"x": 410, "y": 268},
        "J. Ruiz": {"x": 480, "y": 268},
        "Gilmore": {"x": 550, "y": 268},
        "Betty Go-Belmonte": {"x": 620, "y": 268},
        "Araneta Center-Cubao (LRT-2)": {"x": 690, "y": 268},
        "Anonas": {"x": 760, "y": 268},
        "Katipunan": {"x": 830, "y": 268},
        "Santolan": {"x": 900, "y": 300},
        "Marikina-Pasig": {"x": 950, "y": 370},
        "Antipolo": {"x": 950, "y": 430},
        "North Avenue": {"x": 540, "y": 90},
        "Quezon Avenue": {"x": 600, "y": 120},
        "GMA-Kamuning": {"x": 650, "y": 170},
        "Araneta Center-Cubao (MRT-3)": {"x": 650, "y": 230},
        "Santolan-Annapolis": {"x": 650, "y": 300},
        "Ortigas": {"x": 620, "y": 326},
        "Shaw Boulevard": {"x": 575, "y": 360},
        "Boni": {"x": 500, "y": 390},
        "Guadalupe": {"x": 410, "y": 410},
        "Buendia": {"x": 340, "y": 425},
        "Ayala": {"x": 280, "y": 440},
        "Magallanes": {"x": 220, "y": 455},
        "Taft Avenue": {"x": 180, "y": 466},
    }

    lines = [
        {"name": "LRT-1", "color": "#ff3b30", "stations": lrt1},
        {"name": "LRT-2", "color": "#2f5cff", "stations": lrt2},
        {"name": "MRT-3", "color": "#22c55e", "stations": mrt3},
    ]

    label_text = {st: st for st in coords.keys()}
    label_text["Araneta Center-Cubao (MRT-3)"] = "Cubao (MRT-3)"
    label_text["Araneta Center-Cubao (LRT-2)"] = "Cubao (LRT-2)"
    label_text["Betty Go-Belmonte"] = "Betty Go"
    label_text["Santolan-Annapolis"] = "Santolan-Ann."
    label_text["Marikina-Pasig"] = "Marikina"
    label_text["Ninoy Aquino Avenue"] = "NAIA Ave."

    label_meta = {}

    def set_label(station, dx, dy, anchor):
        label_meta[station] = {"dx": dx, "dy": dy, "anchor": anchor}

    for st in coords.keys():
        set_label(st, 12, 4, "start")

    for st in lrt1:
        set_label(st, -12, 4, "end")

    for i, st in enumerate(lrt2):
        set_label(st, 0, (20 if i % 2 == 0 else -14), "middle")

    for i, st in enumerate(mrt3):
        set_label(st, 14, 4, "start")

    set_label("Doroteo Jose", -12, 4, "end")
    set_label("Recto", 0, 20, "middle")
    set_label("EDSA", -12, 4, "end")
    set_label("Taft Avenue", 0, 20, "middle")
    set_label("Araneta Center-Cubao (MRT-3)", 14, 4, "start")
    set_label("Araneta Center-Cubao (LRT-2)", 26, -14, "middle")

    return g, coords, lines, label_meta, label_text, transfers
