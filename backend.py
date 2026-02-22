GALVANIZATION_FACTOR = 1.035
steel_density_kg_per_mm3 = 7.85e-9
def measure_check(class_name,width_mm=None, height_mm=None, thickness_mm=None):
    dimensions = {
        "width_mm": width_mm,
        "height_mm": height_mm,
        "thickness_mm": thickness_mm
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
    def __init__(self, HEA, height_mm):
        if HEA not in self.HEA_density_kg_per_mm:
            raise KeyError(f"Bilinmeyen HEA ölçüsü: {HEA}")
        measure_check(self.__class__.__name__, height_mm)
        self.HEA = HEA
        self.height_mm = height_mm
        density = self.HEA_density_kg_per_mm[HEA]
        self.mass_kg = self.height_mm * density * GALVANIZATION_FACTOR 


class Akustik: 
    density_kg_per_m2 = 18  
    height_mm = 500
    axis_per_side_offset_mm = 25 
    def __init__(self, length_mm):
        if length_mm <= 2 * self.axis_per_side_offset_mm:
            raise ValueError(f"Akustik uzunluğu değer aralığı dışında: {length_mm}")
        self.length_mm = length_mm
        self.area_m2 = length_mm * self.height_mm * 1e-6  # mm2 to m2 conversion
        self.mass_kg =  self.area_m2 * self.density_kg_per_m2 


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
        self.mass_kg = self.volume_mm3 * steel_density_kg_per_mm3 * GALVANIZATION_FACTOR

      
class PcLevha: # 1 and 1.5 
    density_kg_per_mm3 = 1.2e-6
    def __init__(self, width_mm, height_mm, thickness_mm):
        measure_check(self.__class__.__name__, width_mm, height_mm, thickness_mm)
        self.width_mm = width_mm
        self.height_mm = height_mm
        self.thickness_mm = thickness_mm
        self.area_m2 = width_mm * height_mm * 1e-6 # mm2 to m2 conversion 
        self.volume_mm3 = volume_calculator(width_mm, height_mm, thickness_mm)
        self.mass_kg = self.volume_mm3 * self.density_kg_per_mm3
        self.tape_length_mm = (width_mm + height_mm) * 2 * 1.01 # add wastage factor


    # double stiffener for between pcs 
    # single for every other side 

class Stiffener: # dual btw pcs single btw others none to akcsts will set perside off dependant on post 
    axis_per_side_offset_mm = 20
    stiffener_masses_kg = {    # massses are placeholers ***PAY ATTENTION***
        'H120': 0.1, 'H120D': 0.2,    
        'H140': 0.2, 'H140D': 0.4,
        'H160': 0.3, 'H160D': 0.6,
        'H180': 0.4, 'H180D': 0.8,
    }

    def __init__(self,kind):
        if kind not in self.stiffener_masses_kg:
            raise TypeError(f"Bilinmeyen stiffener tipi: {kind}")
        self.kind = kind 
        self.mass_kg = self.stiffener_masses_kg[kind]

    # 4 different sizes
    # h120 depends on post 
    # h140 steel no galvanisation weight  
    # h160  
    # h180
    # lateral margins -20 mm per side offset 
 
class Civata: # 4 per plate each accompanied by a nut and a washer 
    bolt_masses = { # all bolts are defaulted do 250mm and studs are approximated to behave like normal bolts
        'M16': 0.4316,
        'M18': 0.5401,
        'M20': 0.6837,
        'M22': 0.8420,
        'M24': 1.0108,
    }
    def __init__(self, M_size, isStud):
        if M_size not in self.bolt_masses:
            raise KeyError(f"Bilinmeyen M civata olcusu: {M_size}")
        self.isStud = isStud
        self.M_size = M_size
        self.mass_kg = self.bolt_masses[M_size]

    # return bolt amonunts this is vital 4 per plate 
    # m16 - m24 x 250 mass cost amount etc 
    # isStud or isBolt same measurements for all and same M washers to add 2 mm 

def calculate():
    





    pass




# def run_calculation(app):
#     axle_distance = app.axle_distance.get()
#     post = backend.Post(app.post_hea.get(), app.post_height.get())
#     # akustik = Akustik(app.akustik_.get)
#     plaka = backend.Plaka(app.plaka_width.get(), app.plaka_height.get(), app.plaka_thickness.get())
#     berkitme = backend.Berkitme(app.berkitme_width.get(), app.berkitme_height.get(), app.berkitme_thickness.get())
#     # pclevha = PcLevha()
#     # stiffener = Stiffener
#     bolt = backend.Civata(app.bolt_size.get(), app.isStud.get())
        



#     rows = [
#         {"Parameter": "Axle Distance", "Value": axle_distance, "Unit": "mm"},

#         {"Parameter": "Post Type", "Value": post.HEA, "Unit": "-"},
#         {"Parameter": "Post Height", "Value": post.height_mm, "Unit": "mm"},
#         {"Parameter": "Post Mass", "Value": round(post.mass_kg, 2), "Unit": "kg"},

#         {"Parameter": "Plate Width", "Value": plaka.width_mm, "Unit": "mm"},
#         {"Parameter": "Plate Height", "Value": plaka.height_mm, "Unit": "mm"},
#         {"Parameter": "Plate Thickness", "Value": plaka.thickness_mm, "Unit": "mm"},

#         {"Parameter": "Berkitme Width", "Value": berkitme.width_mm, "Unit": "mm"},
#         {"Parameter": "Berkitme Height", "Value": berkitme.height_mm, "Unit": "mm"},
#         {"Parameter": "Berkitme Thickness", "Value": berkitme.thickness_mm, "Unit": "mm"},

#         {"Parameter": "Bolt Mass", "Value": bolt.mass_kg, "Unit": "kg"},
#         {"Parameter": "Bolt Mass", "Value": bolt.isStud, "Unit": "-"}







#     ]

#     return rows