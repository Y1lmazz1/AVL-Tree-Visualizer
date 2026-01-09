import os
import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk
from graphviz import Digraph
import random

# --- MODERN RENK PALETİ ---
BG_COLOR = "#1e2124"
PANEL_COLOR = "#2f3136"
ACCENT_COLOR = "#7289da"
TEXT_COLOR = "#ffffff"
SUCCESS_COLOR = "#43b581"
DANGER_COLOR = "#f04747"
PRACTICE_COLOR = "#faa61a" # Alıştırma modu için turuncu

os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

class Node:
    def __init__(self, key):
        self.key, self.left, self.right, self.height = key, None, None, 1

class AVLTree:
    def __init__(self, log_callback): self.log = log_callback
    def get_height(self, n): return n.height if n else 0
    def get_balance(self, n): return self.get_height(n.left) - self.get_height(n.right) if n else 0

    def rotate_right(self, y):
        self.log(f"🔄 {y.key} -> Sağa Rotasyon")
        x, T2 = y.left, y.left.right
        x.right, y.left = y, T2
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        return x

    def rotate_left(self, x):
        self.log(f"🔄 {x.key} -> Sola Rotasyon")
        y, T2 = x.right, x.right.left
        y.left, x.right = x, T2
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def insert(self, root, key):
        if not root: return Node(key)
        if key < root.key: root.left = self.insert(root.left, key)
        else: root.right = self.insert(root.right, key)
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        b = self.get_balance(root)
        if b > 1 and key < root.left.key: return self.rotate_right(root)
        if b < -1 and key > root.right.key: return self.rotate_left(root)
        if b > 1 and key > root.left.key:
            root.left = self.rotate_left(root.left); return self.rotate_right(root)
        if b < -1 and key < root.right.key:
            root.right = self.rotate_right(root.right); return self.rotate_left(root)
        return root

    def get_traversal(self, root, mode="In-order"):
        res = []
        if root:
            if mode == "Pre-order": res.append(str(root.key))
            res += self.get_traversal(root.left, mode)
            if mode == "In-order": res.append(str(root.key))
            res += self.get_traversal(root.right, mode)
            if mode == "Post-order": res.append(str(root.key))
        return res

class AVLApp:
    def __init__(self, window):
        self.window = window
        self.window.title("AVL Lab: Alıştırma & Görselleştirme")
        self.window.configure(bg=BG_COLOR)
        self.tree_logic = AVLTree(self.add_log)
        
        # Değişkenler
        self.root = None
        self.pending_root = None # Alıştırma modunda çözümü bekleyen ağaç
        self.current_type = None
        self.traversal_mode = tk.StringVar(value="In-order")
        self.app_mode = tk.StringVar(value="Öğrenme") # Öğrenme veya Alıştırma

        self.setup_ui()

    def setup_ui(self):
        # --- ÜST BAR ---
        top_bar = tk.Frame(self.window, bg=PANEL_COLOR, height=70)
        top_bar.pack(side=tk.TOP, fill=tk.X)
        top_bar.pack_propagate(False)

        tk.Label(top_bar, text="MOD:", bg=PANEL_COLOR, fg=PRACTICE_COLOR, font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=(20, 5))
        mode_menu = tk.OptionMenu(top_bar, self.app_mode, "Öğrenme", "Alıştırma", command=self.on_mode_change)
        mode_menu.config(bg=BG_COLOR, fg=TEXT_COLOR, relief="flat")
        mode_menu.pack(side=tk.LEFT, padx=5)

        tk.Label(top_bar, text="DEĞER:", bg=PANEL_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=(15, 5))
        self.entry = tk.Entry(top_bar, bg=BG_COLOR, fg=TEXT_COLOR, insertbackground="white", relief="flat", font=("Segoe UI", 12), width=8)
        self.entry.pack(side=tk.LEFT, padx=5)

        btn_opt = {"bg": ACCENT_COLOR, "fg": "white", "relief": "flat", "font": ("Segoe UI", 9, "bold"), "padx": 10, "cursor": "hand2"}
        
        tk.Button(top_bar, text="EKLE", command=self.process_input, **btn_opt).pack(side=tk.LEFT, padx=5)
        
        self.solve_btn = tk.Button(top_bar, text="ÇÖZÜMÜ GÖSTER", command=self.apply_solution, bg=SUCCESS_COLOR, fg="white", relief="flat", font=("Segoe UI", 9, "bold"), padx=10, state="disabled")
        self.solve_btn.pack(side=tk.LEFT, padx=5)

        tk.Button(top_bar, text="RANDOM YENİLE", command=self.add_random, **btn_opt).pack(side=tk.LEFT, padx=5)
        tk.Button(top_bar, text="SIFIRLA", command=self.reset, bg=DANGER_COLOR, fg="white", relief="flat", font=("Segoe UI", 9, "bold"), padx=10).pack(side=tk.RIGHT, padx=20)

        # --- ANA GÖVDE ---
        container = tk.Frame(self.window, bg=BG_COLOR)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.canvas_label = tk.Label(container, bg=BG_COLOR)
        self.canvas_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        right_panel = tk.Frame(container, bg=PANEL_COLOR, width=320)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y)

        tk.Label(right_panel, text="📊 İSTATİSTİKLER", bg=PANEL_COLOR, fg=ACCENT_COLOR, font=("Segoe UI", 11, "bold")).pack(pady=(15, 5))
        self.stats_label = tk.Label(right_panel, text="Düğüm: 0\nYükseklik: 0", bg=PANEL_COLOR, fg=TEXT_COLOR, justify=tk.LEFT, font=("Segoe UI", 10))
        self.stats_label.pack()

        tk.Label(right_panel, text="🔍 SIRALAMA TÜRÜ", bg=PANEL_COLOR, fg=ACCENT_COLOR, font=("Segoe UI", 11, "bold")).pack(pady=(20, 5))
        for mode in ["In-order", "Pre-order", "Post-order"]:
            tk.Radiobutton(right_panel, text=mode, variable=self.traversal_mode, value=mode, bg=PANEL_COLOR, fg=TEXT_COLOR, selectcolor=BG_COLOR, font=("Segoe UI", 9), command=self.update_ui).pack(anchor=tk.W, padx=30)

        tk.Label(right_panel, text="📜 İŞLEM KAYITLARI", bg=PANEL_COLOR, fg=ACCENT_COLOR, font=("Segoe UI", 11, "bold")).pack(pady=(20, 5))
        self.log_area = scrolledtext.ScrolledText(right_panel, bg=BG_COLOR, fg="#b9bbbe", borderwidth=0, font=("Consolas", 9), width=35, height=18)
        self.log_area.pack(padx=10, pady=10)

        self.footer = tk.Frame(self.window, bg=PANEL_COLOR, height=40)
        self.footer.pack(side=tk.BOTTOM, fill=tk.X)
        self.trav_label = tk.Label(self.footer, text="Dizi: -", bg=PANEL_COLOR, fg=SUCCESS_COLOR, font=("Segoe UI", 10, "bold italic"))
        self.trav_label.pack(pady=10)

    def on_mode_change(self, mode):
        self.reset()
        self.add_log(f"Mod Değiştirildi: {mode}")

    def add_log(self, msg):
        self.log_area.insert(tk.END, f"> {msg}\n")
        self.log_area.see(tk.END)

    def process_input(self):
        val = self.entry.get()
        if not val: return
        try: v_final, v_type = int(val), int
        except: v_final, v_type = val, str

        if self.root is None and self.pending_root is None: self.current_type = v_type
        elif v_type != self.current_type:
            messagebox.showerror("Hata", "Tür uyuşmazlığı!"); return

        if self.app_mode.get() == "Öğrenme":
            self.root = self.tree_logic.insert(self.root, v_final)
            self.add_log(f"Eklendi: {v_final}")
            self.update_ui()
        else:
            # Alıştırma Modu: Çözümü hazırla ama gösterme
            self.pending_root = self.tree_logic.insert(self.root if self.root else self.pending_root, v_final)
            self.solve_btn.config(state="normal", bg=PRACTICE_COLOR)
            self.add_log(f"❓ {v_final} eklendi. Şimdi ağacın yeni halini tahmin et ve butona bas!")
            self.entry.delete(0, tk.END)

    def apply_solution(self):
        self.root = self.pending_root
        self.pending_root = None
        self.solve_btn.config(state="disabled", bg=SUCCESS_COLOR)
        self.add_log("✅ Çözüm uygulandı.")
        self.update_ui()

    def add_random(self):
        self.reset()
        adet = random.randint(5, 20)
        nums = random.sample(range(1, 101), adet)
        self.add_log(f"--- {adet} Rastgele Sayı Hazır ---")
        
        if self.app_mode.get() == "Öğrenme":
            for r in nums: self.root = self.tree_logic.insert(self.root, r)
            self.update_ui()
        else:
            # Alıştırma modunda random sayıları loga yaz ama ağacı hemen kurma
            self.add_log(f"Sırasıyla ekle: {nums}")
            self.add_log("İpucu: İlk sayı root olacak.")
            # İlk sayıyı otomatik pending'e alalım ki kullanıcı başlasın
            self.entry.insert(0, str(nums[0]))
            self.process_input()

    def reset(self):
        self.root = self.pending_root = self.current_type = None
        self.log_area.delete('1.0', tk.END)
        self.solve_btn.config(state="disabled")
        self.update_ui()

    def update_ui(self):
        self.entry.delete(0, tk.END)
        h = self.tree_logic.get_height(self.root)
        n = self.count_nodes(self.root)
        self.stats_label.config(text=f"Düğüm Sayısı: {n}\nAğaç Yüksekliği: {h}")
        
        mode = self.traversal_mode.get()
        seq = " → ".join(self.tree_logic.get_traversal(self.root, mode))
        self.trav_label.config(text=f"{mode} Dizilimi: {seq}")

        if not self.root:
            self.canvas_label.config(image='')
            return

        dot = Digraph(format='png')
        dot.attr(bgcolor=BG_COLOR)
        dot.attr('node', shape='circle', style='filled', fontname='Segoe UI Semibold', fontsize='12', fontcolor='white')
        dot.attr('edge', color='#4f545c', penwidth='2')
        self._build_dot(self.root, dot)
        dot.render("avl_practice", cleanup=True)
        
        img = Image.open("avl_practice.png")
        img.thumbnail((800, 600), Image.Resampling.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(img)
        self.canvas_label.config(image=self.tk_img)

    def _build_dot(self, node, dot):
        if node:
            b = self.tree_logic.get_balance(node)
            fcolor = SUCCESS_COLOR if abs(b) <= 1 else DANGER_COLOR
            dot.node(str(node.key), f"{node.key}\n(b:{b})", fillcolor=fcolor, color=fcolor)
            if node.left:
                dot.edge(str(node.key), str(node.left.key))
                self._build_dot(node.left, dot)
            if node.right:
                dot.edge(str(node.key), str(node.right.key))
                self._build_dot(node.right, dot)

    def count_nodes(self, root):
        return 1 + self.count_nodes(root.left) + self.count_nodes(root.right) if root else 0

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x850")
    app = AVLApp(root)
    root.mainloop()