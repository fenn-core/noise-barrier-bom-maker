# move all calculation logic to the backend
import backend 
import tkinter as tk
from tkinter import ttk, filedialog
import sv_ttk
import pandas as pd


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Structural Calculator")
        self.geometry("900x720")
        self.resizable(False, False)

        self.dark_mode = tk.BooleanVar(value=True)
        sv_ttk.set_theme("dark")

        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.axle_distance = tk.IntVar(value=0)
        self.is_dual = tk.BooleanVar(value=False)

        self.post_hea = tk.StringVar(value="HEA120")
        self.post_height = tk.IntVar(value=0)

        self.plaka_width = tk.IntVar(value=0)
        self.plaka_height = tk.IntVar(value=0)
        self.plaka_thickness = tk.IntVar(value=0)

        self.berkitme_width = tk.IntVar(value=0)
        self.berkitme_height = tk.IntVar(value=0)
        self.berkitme_thickness = tk.IntVar(value=0)

        self.pc_thickness = tk.StringVar(value="12mm")

        self.bolt_size = tk.StringVar(value="M16")
        self.isStud = tk.BooleanVar(value=False)


        self.pages = {}
        for Page in (Page1, Page2,Page3):
            page = Page(self.container, self)
            self.pages[Page] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.show(Page1)

    def show(self, page):
        self.pages[page].tkraise()

    def theme_switch(self):
        sv_ttk.set_theme("dark" if self.dark_mode.get() else "light")


class Page1(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        PAD_X = 20
        PAD_Y = 12
        ENTRY_W = 12
        COMBO_W = 12


        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)

        ttk.Label(
            self,
            text="Input Parameters",
            font=("Segoe UI", 18, "bold")
        ).grid(row=0, column=0, sticky="w", padx=PAD_X, pady=(20, 10))

        top_bar = ttk.Frame(self)
        top_bar.grid(row=0, column=1, sticky="e", padx=PAD_X, pady=(20, 10))

        ttk.Checkbutton(
            top_bar,
            text="Dark Mode",
            variable=app.dark_mode,
            command=app.theme_switch,
            style="Switch.TCheckbutton"
        ).grid()

        ttk.Separator(self).grid(row=1, column=0, columnspan=2, sticky="ew", padx=PAD_X)

        row_frame = ttk.Frame(self)
        row_frame.grid(row=2, column=0, sticky="w", padx=PAD_X, pady=PAD_Y)

        axle_frame = ttk.LabelFrame(row_frame, text="Axle", padding=10)
        axle_frame.grid(row=0, column=0, sticky="w", padx=(0, 20))

        ttk.Label(axle_frame, text="Axle Distance (mm):").grid(row=0, column=0, sticky="w")
        ttk.Entry(axle_frame, textvariable=app.axle_distance, width=ENTRY_W).grid(row=0, column=1)

        dual_frame = ttk.LabelFrame(row_frame, text="Çift", padding=10)
        dual_frame.grid(row=0, column=1, sticky="w")

        ttk.Label(dual_frame, text="Enable:").grid(row=0, column=0, sticky="w")
        ttk.Checkbutton(
            dual_frame,
            variable=app.is_dual,
            style="Switch.TCheckbutton"
        ).grid(row=0, column=1)

        post_frame = ttk.LabelFrame(self, text="Post", padding=10)
        post_frame.grid(row=3, column=0, sticky="w", padx=PAD_X, pady=PAD_Y)

        ttk.Label(post_frame, text="HEA Type:").grid(row=0, column=0, sticky="w")
        ttk.Combobox(
            post_frame,
            textvariable=app.post_hea,
            values=["HEA120", "HEA140", "HEA160", "HEA180"],
            state="readonly",
            width=COMBO_W
        ).grid(row=0, column=1, padx=(0, 12))

        ttk.Label(post_frame, text="Height (mm):").grid(row=0, column=2, sticky="w")
        ttk.Entry(post_frame, textvariable=app.post_height, width=ENTRY_W).grid(row=0, column=3)

        def dim_row(frame, items):
            for i, (label, var) in enumerate(items):
                ttk.Label(frame, text=label).grid(row=0, column=i * 2, sticky="w")
                ttk.Entry(frame, textvariable=var, width=ENTRY_W).grid(row=0, column=i * 2 + 1, padx=(0, 12))

        plaka_frame = ttk.LabelFrame(self, text="Plaka", padding=10)
        plaka_frame.grid(row=4, column=0, sticky="w", padx=PAD_X, pady=PAD_Y)
        dim_row(plaka_frame, [
            ("Width (mm):", app.plaka_width),
            ("Height (mm):", app.plaka_height),
            ("Thickness (mm):", app.plaka_thickness),
        ])

        berkitme_frame = ttk.LabelFrame(self, text="Berkitme", padding=10)
        berkitme_frame.grid(row=5, column=0, sticky="w", padx=PAD_X, pady=PAD_Y)
        dim_row(berkitme_frame, [
            ("Width (mm):", app.berkitme_width),
            ("Height (mm):", app.berkitme_height),
            ("Thickness (mm):", app.berkitme_thickness),
        ])

        pc_frame = ttk.LabelFrame(self, text="PC Levha", padding=10)
        pc_frame.grid(row=6, column=0, sticky="w", padx=PAD_X, pady=PAD_Y)

        ttk.Label(pc_frame, text="Thickness:").grid(row=0, column=0, sticky="w")
        ttk.Combobox(
            pc_frame,
            textvariable=app.pc_thickness,
            values=["12mm", "14mm", "16mm", "20mm", "22mm"],
            state="readonly",
            width=COMBO_W
        ).grid(row=0, column=1)

        bolt_frame = ttk.LabelFrame(self, text="Civata", padding=10)
        bolt_frame.grid(row=7, column=0, sticky="w", padx=PAD_X, pady=PAD_Y)

        ttk.Label(bolt_frame, text="Bolt Size:").grid(row=0, column=0, sticky="w")
        ttk.Combobox(
            bolt_frame,
            textvariable=app.bolt_size,
            values=["M16", "M18", "M20", "M22", "M24"],
            state="readonly",
            width=COMBO_W
        ).grid(row=0, column=1, padx=(0, 12))

        ttk.Label(bolt_frame, text="Stud:").grid(row=0, column=2, sticky="w")
        ttk.Checkbutton(bolt_frame, variable=app.isStud, style="Switch.TCheckbutton").grid(row=0, column=3)

        ttk.Separator(self).grid(row=8, column=0, sticky="ew", padx=PAD_X, pady=(25, 15))

        ttk.Button(
            self,
            text="Next ▶",
            command=lambda: app.show(Page2)
        ).grid(row=9, column=0, sticky="e", padx=PAD_X, pady=20)



class Page2(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        PAD_X = 20
        PAD_Y = 12

        self.post_height_m = 4
        self.pc_panel_height_m = 1.0
        self.acoustic_panel_height_m = 0.5

        self.acoustic_count = tk.IntVar(value=0)
        self.pc_count = tk.IntVar(value=0)

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(3, weight=1)

        ttk.Label(
            self,
            text="Ses Bariyeri Geometrisi",
            font=("Segoe UI", 18, "bold")
        ).grid(row=0, column=0, sticky="w", padx=PAD_X, pady=(20, 10))

        ttk.Separator(self).grid(
            row=1, column=0, columnspan=2, sticky="ew", padx=PAD_X
        )

        self.canvas = tk.Canvas(
            self,
            bg="#1e1e1e",
            highlightthickness=0
        )
        self.canvas.grid(
            row=3, column=0, sticky="nsew", padx=(PAD_X, 10), pady=PAD_Y
        )

        control_frame = ttk.Frame(self)
        control_frame.grid(
            row=3, column=1, sticky="nw", padx=(10, PAD_X), pady=PAD_Y
        )

        self._build_controls(control_frame)

        ttk.Separator(self).grid(
            row=4, column=0, columnspan=2, sticky="ew", padx=PAD_X, pady=(20, 10)
        )

        ttk.Button(
            self,
            text="◀ Back",
            command=lambda: app.show(Page1)
        ).grid(row=5, column=0, sticky="e", padx=PAD_X, pady=20)

        ttk.Button(
            self,
            text="Next ▶",
            command=lambda: app.show(Page3)
        ).grid(row=5, column=1, sticky="e", padx=PAD_X, pady=20)


        self.canvas.bind("<Configure>", lambda e: self._draw_model())
        self._draw_model()

    def _build_controls(self, parent):
        ttk.Label(
            parent,
            text="Panel Seçimi",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", pady=(0, 10))

        acoustic = ttk.LabelFrame(parent, text="Akustik Paneller", padding=10)
        acoustic.pack(fill="x", pady=(0, 10))

        ttk.Button(acoustic, text="−", width=3, command=self._remove_acoustic).grid(row=0, column=0)
        ttk.Label(acoustic, textvariable=self.acoustic_count, width=5, anchor="center").grid(row=0, column=1)
        ttk.Button(acoustic, text="+", width=3, command=self._add_acoustic).grid(row=0, column=2)

        ttk.Label(acoustic, text="0.5 m / adet", foreground="gray").grid(
            row=1, column=0, columnspan=3
        )

        pc = ttk.LabelFrame(parent, text="PC Paneller", padding=10)
        pc.pack(fill="x")

        ttk.Button(pc, text="−", width=3, command=self._remove_pc).grid(row=0, column=0)
        ttk.Label(pc, textvariable=self.pc_count, width=5, anchor="center").grid(row=0, column=1)
        ttk.Button(pc, text="+", width=3, command=self._add_pc).grid(row=0, column=2)

        ttk.Label(
            pc,
            text=f"{self.pc_panel_height_m} m / adet",
            foreground="gray"
        ).grid(row=1, column=0, columnspan=3)

    def _used_height(self):
        return (
            self.acoustic_count.get() * self.acoustic_panel_height_m +
            self.pc_count.get() * self.pc_panel_height_m
        )

    def _remaining_height(self):
        return self.post_height_m - self._used_height()

    def _add_acoustic(self):
        if self._remaining_height() >= self.acoustic_panel_height_m:
            self.acoustic_count.set(self.acoustic_count.get() + 1)
            self._draw_model()

    def _remove_acoustic(self):
        if self.acoustic_count.get() > 0:
            self.acoustic_count.set(self.acoustic_count.get() - 1)
            self._draw_model()

    def _add_pc(self):
        if self._remaining_height() >= self.pc_panel_height_m:
            self.pc_count.set(self.pc_count.get() + 1)
            self._draw_model()

    def _remove_pc(self):
        if self.pc_count.get() > 0:
            self.pc_count.set(self.pc_count.get() - 1)
            self._draw_model()

    def _draw_model(self):
        
        self.canvas.delete("all")

        canvas_h = self.canvas.winfo_height() or 600
        canvas_w = self.canvas.winfo_width() or 400

        top_margin = 30
        bottom_margin = 30

        usable_h = canvas_h - top_margin - bottom_margin
        scale = usable_h / self.post_height_m

        model_width = canvas_w * 0.55
        x_center = canvas_w / 2

        x_left = x_center - model_width / 2
        x_right = x_center + model_width / 2

        post_width = model_width * 0.06
        panel_inset = post_width * 0.6

        y_bottom = canvas_h - bottom_margin
        y_top = y_bottom - self.post_height_m * scale

        steel_fill = "#6f7276"
        steel_edge = "#5a5d61"

        acoustic_fill = "#2a2a2a"
        acoustic_edge = "#3a3a3a"

        pc_fill = "#d6d6d6"
        pc_edge = "#bdbdbd"

        ruler_x = x_left - post_width - 25

        self.canvas.create_line(
            ruler_x, y_top, ruler_x, y_bottom,
            fill="#888", width=1
        )

        h = 0.0
        while h <= self.post_height_m + 1e-6:
            y = y_bottom - h * scale
            if abs(h % 1.0) < 1e-6:
                self.canvas.create_line(
                    ruler_x - 10, y, ruler_x, y,
                    fill="#aaa", width=1
                )
                self.canvas.create_text(
                    ruler_x - 15, y,
                    text=f"{h:.1f} m",
                    fill="#aaa",
                    anchor="e",
                    font=("Segoe UI", 9)
                )
            else:
                self.canvas.create_line(
                    ruler_x - 5, y, ruler_x, y,
                    fill="#777", width=1
                )
            h += 0.5

        self.canvas.create_rectangle(
            x_left - post_width, y_top,
            x_left, y_bottom,
            fill=steel_fill,
            outline=steel_edge,
            width=1
        )

        self.canvas.create_rectangle(
            x_right, y_top,
            x_right + post_width, y_bottom,
            fill=steel_fill,
            outline=steel_edge,
            width=1
        )

        panel_x1 = x_left + panel_inset
        panel_x2 = x_right - panel_inset

        y = y_bottom

        for _ in range(self.acoustic_count.get()):
            h = self.acoustic_panel_height_m * scale
            self.canvas.create_rectangle(
                panel_x1, y - h,
                panel_x2, y,
                fill=acoustic_fill,
                outline=acoustic_edge,
                width=1
            )
            y -= h

        for _ in range(self.pc_count.get()):
            h = self.pc_panel_height_m * scale
            self.canvas.create_rectangle(
                panel_x1, y - h,
                panel_x2, y,
                fill=pc_fill,
                outline=pc_edge,
                width=1
            )
            y -= h

        self.canvas.create_line(
            x_left - post_width, y_bottom,
            x_right + post_width, y_bottom,
            fill="#444",
            width=1
        )
    


class Page3(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.results = []

        PAD_X = 20
        PAD_Y = 12

        self.status_text = tk.StringVar(value="Ready")
        self.save_path = tk.StringVar(value="")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        ttk.Label(
            self,
            text="Calculation Results",
            font=("Segoe UI", 18, "bold")
        ).grid(row=0, column=0, sticky="w", padx=PAD_X, pady=(20, 10))

        ttk.Separator(self).grid(row=1, column=0, sticky="ew", padx=PAD_X)

        table_frame = ttk.Frame(self)
        table_frame.grid(row=2, column=0, sticky="nsew", padx=PAD_X, pady=PAD_Y)

        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        columns = ("parameter", "value", "unit")

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=12
        )

        self.table.heading("parameter", text="Parameter")
        self.table.heading("value", text="Value")
        self.table.heading("unit", text="Unit")

        self.table.column("parameter", width=250, anchor="w")
        self.table.column("value", width=120, anchor="center")
        self.table.column("unit", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.populate_demo_data()

        ttk.Separator(self).grid(row=3, column=0, sticky="ew", padx=PAD_X)

        bottom_bar = ttk.Frame(self)
        bottom_bar.grid(row=4, column=0, sticky="ew", padx=PAD_X, pady=20)

        bottom_bar.columnconfigure(0, weight=1)

        ttk.Button(
            bottom_bar,
            text="◀ Back",
            command=lambda: app.show(Page2)
        ).grid(row=0, column=0, sticky="w")

        bottom_bar.columnconfigure(1, weight=1)
        
        ttk.Frame(bottom_bar).grid(row=0, column=1, sticky="ew")
        status_label = ttk.Label(
            bottom_bar,
            textvariable=self.status_text,
            anchor="w"
        )
        status_label.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(10, 0))

        bottom_bar.columnconfigure(0, weight=1)

        ttk.Button(
            bottom_bar,
            text="Calculate",
            width=14,
            command=self.run_calculation
        ).grid(row=0, column=2, padx=(0, 10))

        ttk.Button(
            bottom_bar,
            text="Save As",
            width=14,
            command=self.select_save_location
        ).grid(row=0, column=3)

    def populate_demo_data(self):
        demo_rows = [
            ("Aks Mesafesi ", 0, "mm"),
            ("Post Yukseligi", 3000, "mm"),
            ("Bolt Diameter", 16, "mm"),
            ("Plate Thickness", 12, "mm"),
            ("Safety Factor", 1.65, "-"),
        ]

        for row in demo_rows:
            self.table.insert("", "end", values=row)

    def run_calculation(self):
        self.table.delete(*self.table.get_children())

        try:
            self.results = backend.calculate(self.app)

            if not self.results:
                self.status_text.set("No calculation data produced")
                return

            for row in self.results:
                self.table.insert(
                    "",
                    "end",
                    values=(row["Parameter"], row["Value"], row["Unit"])
                )

            self.status_text.set("Calculation completed successfully")

        except Exception as e:
            self.status_text.set(f"Calculation error: {e}")



    def select_save_location(self):
        if not self.results:
            print("Nothing to save yet")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel File", "*.xlsx")]
        )

        if not path:
            return

        df = pd.DataFrame(self.results)
        df.to_excel(path, index=False)

        print(f"Saved to {path}")


app = App()


if __name__ == "__main__":
    app.mainloop()