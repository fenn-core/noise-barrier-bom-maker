import math

GALVANIZATION_FACTOR = 1.035
STEEL_DENSITY_KG_PER_MM3 = 7.85e-9


def measure_check(class_name, width_mm=None, height_mm=None, thickness_mm=None):
    dimensions = {
        "width_mm": width_mm,
        "height_mm": height_mm,
        "thickness_mm": thickness_mm,
    }
    for name, value in dimensions.items():
        if value is not None and value <= 0:
            raise ValueError(f"{class_name} {name} değer aralığı dışında: {value}")


def volume_calculator(width_mm, height_mm, thickness_mm):
    return width_mm * height_mm * thickness_mm


class Post:
    HEA_density_kg_per_mm = {
        "HEA120": 19.9 / 1e3,
        "HEA140": 24.7 / 1e3,
        "HEA160": 30.4 / 1e3,
        "HEA180": 35.5 / 1e3,
    }

    def __init__(self, hea, height_mm):
        if hea not in self.HEA_density_kg_per_mm:
            raise KeyError(f"Bilinmeyen HEA ölçüsü: {hea}")
        measure_check(self.__class__.__name__, height_mm=height_mm)
        self.HEA = hea
        self.height_mm = height_mm
        density = self.HEA_density_kg_per_mm[hea]
        self.mass_kg = self.height_mm * density * GALVANIZATION_FACTOR


class Akustik:
    density_kg_per_m2 = 18
    height_mm = 500
    axis_per_side_offset_mm = 25

    def __init__(self, length_mm):
        if length_mm <= 2 * self.axis_per_side_offset_mm:
            raise ValueError(f"Akustik uzunluğu değer aralığı dışında: {length_mm}")
        self.length_mm = length_mm
        self.area_m2 = length_mm * self.height_mm * 1e-6
        self.mass_kg = self.area_m2 * self.density_kg_per_m2


class Plaka:
    def __init__(self, width_mm, height_mm, thickness_mm):
        measure_check(self.__class__.__name__, width_mm, height_mm, thickness_mm)
        self.width_mm = width_mm
        self.height_mm = height_mm
        self.thickness_mm = thickness_mm
        self.volume_mm3 = volume_calculator(width_mm, height_mm, thickness_mm)


class Berkitme:
    def __init__(self, width_mm, height_mm, thickness_mm):
        measure_check(self.__class__.__name__, width_mm, height_mm, thickness_mm)
        self.width_mm = width_mm
        self.height_mm = height_mm
        self.thickness_mm = thickness_mm
        self.volume_mm3 = volume_calculator(width_mm, height_mm, thickness_mm)
        self.mass_kg = self.volume_mm3 * STEEL_DENSITY_KG_PER_MM3 * GALVANIZATION_FACTOR


class PcLevha:
    density_kg_per_mm3 = 1.2e-6

    def __init__(self, width_mm, height_mm, thickness_mm):
        measure_check(self.__class__.__name__, width_mm, height_mm, thickness_mm)
        self.width_mm = width_mm
        self.height_mm = height_mm
        self.thickness_mm = thickness_mm
        self.area_m2 = width_mm * height_mm * 1e-6
        self.volume_mm3 = volume_calculator(width_mm, height_mm, thickness_mm)
        self.mass_kg = self.volume_mm3 * self.density_kg_per_mm3
        self.tape_length_mm = (width_mm + height_mm) * 2 * 1.01


class Stiffener:
    axis_per_side_offset_mm = 20
    stiffener_masses_kg = {
        "H120": 0.1,
        "H120D": 0.2,
        "H140": 0.2,
        "H140D": 0.4,
        "H160": 0.3,
        "H160D": 0.6,
        "H180": 0.4,
        "H180D": 0.8,
    }

    def __init__(self, kind):
        if kind not in self.stiffener_masses_kg:
            raise TypeError(f"Bilinmeyen stiffener tipi: {kind}")
        self.kind = kind
        self.mass_kg = self.stiffener_masses_kg[kind]


class Civata:
    bolt_masses = {
        "M16": 0.4316,
        "M18": 0.5401,
        "M20": 0.6837,
        "M22": 0.8420,
        "M24": 1.0108,
    }

    def __init__(self, m_size, is_stud):
        if m_size not in self.bolt_masses:
            raise KeyError(f"Bilinmeyen M civata olcusu: {m_size}")
        self.isStud = is_stud
        self.M_size = m_size
        self.mass_kg = self.bolt_masses[m_size]


def _read_input(parts, key, default=None):
    if isinstance(parts, dict):
        return parts.get(key, default)

    value = getattr(parts, key, default)
    return value.get() if hasattr(value, "get") else value


def _parse_mm_text(value):
    if isinstance(value, (int, float)):
        return int(value)
    cleaned = str(value).strip().lower().replace("mm", "")
    return int(cleaned)


def calculate(parts):
    if not parts:
        return []

    full_distance_m = float(_read_input(parts, "full_distance_m", 0))
    axle_distance_mm = int(_read_input(parts, "axle_distance_mm", _read_input(parts, "axle_distance_m", 0)))

    if full_distance_m <= 0:
        raise ValueError("Toplam mesafe 0'dan büyük olmalıdır")
    if axle_distance_mm <= 0:
        raise ValueError("Aks mesafesi 0'dan büyük olmalıdır")

    full_distance_mm = full_distance_m * 1000
    span_count = math.ceil(full_distance_mm / axle_distance_mm)

    post_hea = _read_input(parts, "post_hea")
    post_height_mm = int(_read_input(parts, "post_height_mm"))

    plaka_width_mm = int(_read_input(parts, "plaka_width_mm"))
    plaka_height_mm = int(_read_input(parts, "plaka_height_mm"))
    plaka_thickness_mm = int(_read_input(parts, "plaka_thickness_mm"))

    berkitme_width_mm = int(_read_input(parts, "berkitme_width_mm"))
    berkitme_height_mm = int(_read_input(parts, "berkitme_height_mm"))
    berkitme_thickness_mm = int(_read_input(parts, "berkitme_thickness_mm"))

    pc_thickness_mm = _parse_mm_text(_read_input(parts, "pc_thickness_mm"))
    bolt_size = _read_input(parts, "M_size")
    is_stud = bool(_read_input(parts, "isStud"))
    is_dual = bool(_read_input(parts, "is_dual"))

    acoustic_count_per_span = max(0, int(_read_input(parts, "acoustic_count", 0)))
    pc_count_per_span = max(0, int(_read_input(parts, "pc_count", 0)))

    post = Post(post_hea, post_height_mm)
    plaka = Plaka(plaka_width_mm, plaka_height_mm, plaka_thickness_mm)
    berkitme = Berkitme(berkitme_width_mm, berkitme_height_mm, berkitme_thickness_mm)
    bolt = Civata(bolt_size, is_stud)

    panel_span_mm = plaka_width_mm
    acoustic_panel = Akustik(panel_span_mm)
    pc_panel = PcLevha(panel_span_mm, 1000, pc_thickness_mm)

    used_height_mm = acoustic_count_per_span * Akustik.height_mm + pc_count_per_span * 1000
    remaining_height_mm = post_height_mm - used_height_mm
    if remaining_height_mm < 0:
        raise ValueError(
            f"Panel yükseklikleri post boyunu aşıyor: kalan {remaining_height_mm} mm"
        )

    total_acoustic_count = acoustic_count_per_span * span_count
    total_pc_count = pc_count_per_span * span_count
    total_bolt_count = (acoustic_count_per_span + pc_count_per_span) * 4 * span_count

    post_count = span_count + 1

    total_post_mass_kg = post.mass_kg * post_count
    total_pc_mass_kg = pc_panel.mass_kg * total_pc_count
    total_acoustic_mass_kg = acoustic_panel.mass_kg * total_acoustic_count
    total_bolt_mass_kg = total_bolt_count * bolt.mass_kg
    total_pc_tape_length_mm = pc_panel.tape_length_mm * total_pc_count

    rows = [
        {"Parameter": "Full Distance", "Value": full_distance_m, "Unit": "m"},
        {"Parameter": "Axle Distance", "Value": axle_distance_mm, "Unit": "mm"},
        {"Parameter": "Span Count", "Value": span_count, "Unit": "adet"},
        {"Parameter": "Post Count", "Value": post_count, "Unit": "adet"},
        {"Parameter": "Dual System", "Value": is_dual, "Unit": "-"},

        {"Parameter": "Post Type", "Value": post.HEA, "Unit": "-"},
        {"Parameter": "Single Post Mass", "Value": round(post.mass_kg, 3), "Unit": "kg"},
        {"Parameter": "Total Post Mass", "Value": round(total_post_mass_kg, 3), "Unit": "kg"},

        {"Parameter": "Plate Volume", "Value": plaka.volume_mm3, "Unit": "mm³"},
        {"Parameter": "Stiffener Volume", "Value": berkitme.volume_mm3, "Unit": "mm³"},
        {"Parameter": "Single Stiffener Mass", "Value": round(berkitme.mass_kg, 3), "Unit": "kg"},

        {"Parameter": "Bolt Size", "Value": bolt.M_size, "Unit": "-"},
        {"Parameter": "Single Bolt Mass", "Value": bolt.mass_kg, "Unit": "kg"},
        {"Parameter": "Total Bolt Count", "Value": total_bolt_count, "Unit": "adet"},
        {"Parameter": "Total Bolt Mass", "Value": round(total_bolt_mass_kg, 3), "Unit": "kg"},

        {"Parameter": "Acoustic Count / Span", "Value": acoustic_count_per_span, "Unit": "adet"},
        {"Parameter": "Total Acoustic Count", "Value": total_acoustic_count, "Unit": "adet"},
        {"Parameter": "Single Acoustic Mass", "Value": round(acoustic_panel.mass_kg, 3), "Unit": "kg"},
        {"Parameter": "Total Acoustic Mass", "Value": round(total_acoustic_mass_kg, 3), "Unit": "kg"},

        {"Parameter": "PC Thickness", "Value": pc_thickness_mm, "Unit": "mm"},
        {"Parameter": "PC Count / Span", "Value": pc_count_per_span, "Unit": "adet"},
        {"Parameter": "Total PC Count", "Value": total_pc_count, "Unit": "adet"},
        {"Parameter": "Single PC Panel Mass", "Value": round(pc_panel.mass_kg, 3), "Unit": "kg"},
        {"Parameter": "Total PC Mass", "Value": round(total_pc_mass_kg, 3), "Unit": "kg"},
        {"Parameter": "Single PC Tape Length", "Value": round(pc_panel.tape_length_mm, 1), "Unit": "mm"},
        {"Parameter": "Total PC Tape Length", "Value": round(total_pc_tape_length_mm, 1), "Unit": "mm"},

        {"Parameter": "Remaining Height", "Value": remaining_height_mm, "Unit": "mm"},
    ]

    return rows
