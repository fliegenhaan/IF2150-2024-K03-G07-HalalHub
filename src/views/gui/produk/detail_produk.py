import tkinter as tk
from tkinter import ttk, messagebox
from controllers.produk_controller import ProdukController

class DetailProduk:
    def __init__(self, parent, colors, product_id, callback=None):
        self.parent = parent
        self.colors = colors
        self.product_id = product_id
        self.callback = callback
        self.controller = ProdukController()
        
        # Load data produk
        self.product = self.controller.get_produk(self.product_id)
        if not self.product:
            messagebox.showerror("Error", "Data produk tidak ditemukan")
            return
            
        # Buat window baru
        self.window = tk.Toplevel(self.parent)
        self.window.title("Detail Produk")
        self.window.geometry("500x600")
        self.window.configure(bg=self.colors['background'])
        
        self.create_header()
        self.create_info_section()
        self.create_stock_section()
        self.create_description_section()
        self.create_buttons()
        
        self.window.transient(self.parent)
        self.window.grab_set()
        self.parent.wait_window(self.window)

    def create_info_section(self):
        """Membuat bagian informasi produk"""
        info_frame = tk.LabelFrame(
            self.window,
            text="Informasi Produk",
            font=('Arial', 10, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['text'],
            padx=20,
            pady=10
        )
        info_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Convert harga from string to float
        try:
            harga = float(self.product.harga) 
            harga_str = f"Rp {harga:,.2f}"
        except:
            harga_str = str(self.product.harga)
            
        self.create_info_item(info_frame, "Nama", self.product.nama_produk)
        self.create_info_item(info_frame, "Kategori", self.product.kategori) 
        self.create_info_item(info_frame, "Harga", harga_str)
        self.create_info_item(info_frame, "Stok", str(self.product.stok))

    def load_product_data(self):
        """Memuat data produk yang akan ditampilkan"""
        self.product = self.controller.get_produk(self.product_id)
        if not self.product:
            messagebox.showerror(
                "Error",
                "Data produk tidak ditemukan"
            )
            self.window.destroy()
            return

    def create_header(self):
        """Membuat bagian header dengan info produk utama"""
        header_frame = tk.Frame(
            self.window,
            bg=self.colors['primary'],
            padx=20,
            pady=15
        )
        header_frame.pack(fill=tk.X)
        
        # ID Produk
        tk.Label(
            header_frame,
            text=f"#{self.product_id}",
            font=('Arial', 10),
            bg=self.colors['primary'],
            fg='white'
        ).pack(anchor='w')
        
        # Nama Produk
        tk.Label(
            header_frame,
            text=self.product.nama_produk,
            font=('Arial', 18, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        ).pack(anchor='w')
        
        # Kategori
        tk.Label(
            header_frame,
            text=self.product.kategori,
            font=('Arial', 10),
            bg=self.colors['primary'],
            fg='white'
        ).pack(anchor='w')

    def create_stock_section(self):
        """Membuat bagian informasi stok"""
        stock_frame = tk.LabelFrame(
            self.window,
            text="Status Stok",
            font=('Arial', 10, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['text'],
            padx=20,
            pady=10
        )
        stock_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Stok saat ini
        current_stock_frame = tk.Frame(
            stock_frame,
            bg=self.colors['background']
        )
        current_stock_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            current_stock_frame,
            text="Stok Saat Ini:",
            font=('Arial', 24, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['text']
        ).pack(side=tk.LEFT)
        
        tk.Label(
            current_stock_frame,
            text=str(self.product.stok),
            font=('Arial', 24, 'bold'),
            bg=self.colors['background'],
            fg=self.get_stock_color()
        ).pack(side=tk.RIGHT)
        
        # Progress bar stok
        if hasattr(self.product, 'stok_minimum') and hasattr(self.product, 'stok_maksimum'):
            ttk.Progressbar(
                stock_frame,
                value=self.product.stok,
                maximum=self.product.stok_maksimum,
                length=200
            ).pack(pady=10)
            
            # Label stok minimum dan maksimum
            range_frame = tk.Frame(
                stock_frame,
                bg=self.colors['background']
            )
            range_frame.pack(fill=tk.X)
            
            tk.Label(
                range_frame,
                text=f"Min: {self.product.stok_minimum}",
                font=('Arial', 9),
                bg=self.colors['background'],
                fg=self.colors['text']
            ).pack(side=tk.LEFT)
            
            tk.Label(
                range_frame,
                text=f"Max: {self.product.stok_maksimum}",
                font=('Arial', 9),
                bg=self.colors['background'],
                fg=self.colors['text']
            ).pack(side=tk.RIGHT)

    def create_description_section(self):
        """Membuat bagian deskripsi produk"""
        desc_frame = tk.LabelFrame(
            self.window,
            text="Deskripsi Produk",
            font=('Arial', 10, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['text'],
            padx=20,
            pady=10
        )
        desc_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Text widget untuk deskripsi
        desc_text = tk.Text(
            desc_frame,
            height=6,
            width=40,
            font=('Arial', 10),
            wrap=tk.WORD,
            bg=self.colors['background'],
            fg=self.colors['text']
        )
        desc_text.pack(fill=tk.BOTH, expand=True)
        
        # Masukkan deskripsi jika ada
        if hasattr(self.product, 'deskripsi'):
            desc_text.insert("1.0", self.product.deskripsi)
            
        # Set readonly
        desc_text.configure(state='disabled')

    def create_buttons(self):
        """Membuat tombol-tombol aksi"""
        button_frame = tk.Frame(
            self.window,
            bg=self.colors['background']
        )
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Tombol Edit
        tk.Button(
            button_frame,
            text="Edit Produk",
            font=('Arial', 10),
            bg=self.colors['primary'],
            fg='white',
            padx=20,
            pady=10,
            command=self.edit_product
        ).pack(side=tk.LEFT)
        
        # Tombol Tutup
        tk.Button(
            button_frame,
            text="Tutup",
            font=('Arial', 10),
            bg=self.colors['secondary'],
            fg='white',
            padx=20,
            pady=10,
            command=self.window.destroy
        ).pack(side=tk.RIGHT)

    def create_info_item(self, parent, label, value, value_color=None):
        """Helper untuk membuat item informasi"""
        container = tk.Frame(
            parent,
            bg=self.colors['background']
        )
        container.pack(fill=tk.X, pady=2)
        
        tk.Label(
            container,
            text=f"{label}:",
            font=('Arial', 10),
            bg=self.colors['background'],
            fg=self.colors['text']
        ).pack(side=tk.LEFT)
        
        tk.Label(
            container,
            text=value,
            font=('Arial', 10, 'bold'),
            bg=self.colors['background'],
            fg=value_color or self.colors['primary']
        ).pack(side=tk.RIGHT)

    def get_stock_color(self):
        """Mendapatkan warna berdasarkan status stok"""
        try:
            stok = int(self.product.stok)
            if stok == 0:
                return self.colors['error']
            elif stok <= 10:
                return self.colors['warning']
            return self.colors['success']
        except (ValueError, TypeError):
            return self.colors['text']

    def edit_product(self):
        """Membuka form edit produk"""
        from .edit_produk import EditProduk
        self.window.destroy()
        EditProduk(
            self.parent,
            self.colors,
            self.product_id,
            self.callback
        )
