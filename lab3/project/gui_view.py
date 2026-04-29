import customtkinter as ctk
from tkinter import ttk


class KnapsackAppView:
    def __init__(self, root, controller_callback, defaults):
        self.root = root
        self.controller_callback = controller_callback

        # Налаштування вигляду (Темна тема та синій акцент)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root.title("Система моделювання задачі «Рюкзак» 🎒")
        self.root.geometry("950x850")

        # --- СТИЛІЗАЦІЯ ТАБЛИЦІ (Treeview) ---
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#2A2D2E", foreground="white", rowheight=35,
                        fieldbackground="#2A2D2E", bordercolor="#343638", borderwidth=0, font=("Roboto", 11))
        style.map('Treeview', background=[('selected', '#1F6AA5')])
        style.configure("Treeview.Heading", background="#343638", foreground="white",
                        relief="flat", font=("Roboto", 12, "bold"), padding=5)
        style.map("Treeview.Heading", background=[('active', '#1F6AA5')])

        # --- ГОЛОВНИЙ КОНТЕЙНЕР ---
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.methods_list = [
            "1. Повний перебір (Brute Force)",
            "2. Рекурсивний метод",
            "3. Жадібний алгоритм",
            "4. Динамічне програмування",
            "5. Метод гілок і меж"
        ]

        # --- 1. БЛОК ВВЕДЕННЯ ---
        input_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        input_frame.pack(fill="x", pady=(0, 20))
        input_frame.columnconfigure(1, weight=1)

        # Заголовок блоку
        ctk.CTkLabel(input_frame, text="⚙️ ПАРАМЕТРИ ЗАДАЧІ", font=("Roboto", 14, "bold"), text_color="#1F6AA5").grid(
            row=0, column=0, columnspan=2, pady=(15, 10), padx=20, sticky="w")

        ctk.CTkLabel(input_frame, text="Місткість (W):", font=("Roboto", 13)).grid(row=1, column=0, sticky="w", padx=20,
                                                                                   pady=5)
        self.ent_W = ctk.CTkEntry(input_frame, width=150, corner_radius=8)
        self.ent_W.insert(0, defaults["W"])
        self.ent_W.grid(row=1, column=1, sticky="w", padx=20, pady=5)

        ctk.CTkLabel(input_frame, text="Ваги (w1, w2...):", font=("Roboto", 13)).grid(row=2, column=0, sticky="w",
                                                                                      padx=20, pady=5)
        self.ent_weights = ctk.CTkEntry(input_frame, corner_radius=8)
        self.ent_weights.insert(0, defaults["weights"])
        self.ent_weights.grid(row=2, column=1, sticky="ew", padx=20, pady=5)

        ctk.CTkLabel(input_frame, text="Цінності (v1, v2...):", font=("Roboto", 13)).grid(row=3, column=0, sticky="w",
                                                                                          padx=20, pady=5)
        self.ent_values = ctk.CTkEntry(input_frame, corner_radius=8)
        self.ent_values.insert(0, defaults["values"])
        self.ent_values.grid(row=3, column=1, sticky="ew", padx=20, pady=5)

        ctk.CTkLabel(input_frame, text="Метод:", font=("Roboto", 13)).grid(row=4, column=0, sticky="w", padx=20, pady=5)
        self.combo_method = ctk.CTkComboBox(input_frame, values=self.methods_list, corner_radius=8, width=350,
                                            state="readonly")
        self.combo_method.set(self.methods_list[3])  # За замовчуванням DP
        self.combo_method.grid(row=4, column=1, sticky="w", padx=20, pady=5)

        self.btn_start = ctk.CTkButton(input_frame, text="ЗАПУСТИТИ ОБЧИСЛЕННЯ", font=("Roboto", 14, "bold"),
                                       corner_radius=8, height=40, command=self._on_click)
        self.btn_start.grid(row=5, column=0, columnspan=2, pady=20)

        # --- 2. ТЕКСТОВИЙ БЛОК ДЛЯ РЕЗУЛЬТАТІВ ---
        res_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        res_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(res_frame, text="📊 ЗВІТ ПРО РЕЗУЛЬТАТИ", font=("Roboto", 14, "bold"), text_color="#1F6AA5").pack(
            anchor="w", padx=20, pady=(15, 5))

        self.txt_output = ctk.CTkTextbox(res_frame, height=140, font=("Consolas", 13), corner_radius=8,
                                         fg_color="#1D1E20")
        self.txt_output.pack(fill="x", padx=20, pady=(0, 20))
        self.txt_output.configure(state="disabled")

        # --- 3. ГРІД ДЛЯ МАТРИЦІ DP ---
        table_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        table_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(table_frame, text="🧮 ВІЗУАЛІЗАЦІЯ МАТРИЦІ СТАНІВ", font=("Roboto", 14, "bold"),
                     text_color="#1F6AA5").pack(anchor="w", padx=20, pady=(15, 5))

        tree_container = ctk.CTkFrame(table_frame, fg_color="transparent")
        tree_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.tree = ttk.Treeview(tree_container, show="headings")
        vsb = ctk.CTkScrollbar(tree_container, orientation="vertical", command=self.tree.yview)
        hsb = ctk.CTkScrollbar(tree_container, orientation="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")

    def _on_click(self):
        # Отримує індекс обраного методу
        selected_method = self.combo_method.get()
        m_idx = self.methods_list.index(selected_method)

        self.controller_callback(
            self.ent_W.get(),
            self.ent_weights.get(),
            self.ent_values.get(),
            m_idx
        )

    def update_result_text(self, text):
        self.txt_output.configure(state="normal")
        self.txt_output.delete("0.0", "end")
        self.txt_output.insert("end", text)
        self.txt_output.configure(state="disabled")

    def render_grid(self, matrix, W, n):
        self.tree.delete(*self.tree.get_children())
        if not matrix:
            self.tree["columns"] = ("msg",)
            self.tree.heading("msg", text="Повідомлення")
            self.tree.column("msg", width=800, anchor="center")
            self.tree.insert("", "end",
                             values=("Матриця станів генерується виключно для методу №4 (Динамічне програмування)",))
            return

        cols = ["Об'єкт / Вага"] + [str(i) for i in range(W + 1)]
        self.tree["columns"] = cols
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=45, anchor="center")

        self.tree.column(cols[0], width=140)

        for i in range(n + 1):
            name = f"Предмет {i}" if i > 0 else "Базис (0)"
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", "end", values=[name] + matrix[i], tags=(tag,))

        self.tree.tag_configure('oddrow', background='#2A2D2E')
        self.tree.tag_configure('evenrow', background='#343638')