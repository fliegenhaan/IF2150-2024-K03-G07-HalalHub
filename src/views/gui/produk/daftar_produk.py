import tkinter as tk
from tkinter import ttk, messagebox
from .tambah_produk import TambahProduk
from .edit_produk import EditProduk
from .detail_produk import DetailProduk
from controllers.produk_controller import ProdukController

class DaftarProduk:
    def __init__(self, parent, colors):
        """
        Inisialisasi tampilan daftar produk
        
        Args:
            parent: Widget parent untuk frame ini
            colors: Dictionary berisi kode warna untuk UI
        """
        self.parent = parent
        self.colors = colors
        self.controller = ProdukController()
        
        # Frame utama
        self.frame = tk.Frame(
            self.parent,
            bg=self.colors['background']
        )
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Inisialisasi komponen UI
        self.create_header()
        self.create_search_section()
        self.create_category_filter()
        self.create_table()
        self.create_action_buttons()
        
        # Load data awal
        self.refresh_data()
        
    def create_header(self):
        """Membuat bagian header dengan judul dan statistik"""
        header_frame = tk.Frame(
            self.frame,
            bg=self.colors['primary'],
            padx=20,
            pady=10
        )
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Label judul
        tk.Label(
            header_frame,
            text="Katalog Produk",
            font=('Arial', 24, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        ).pack(side=tk.LEFT)
        
        # Statistik produk
        self.stats_label = tk.Label(
            header_frame,
            text="",
            font=('Arial', 12),
            bg=self.colors['primary'],
            fg='white'
        )
        self.stats_label.pack(side=tk.RIGHT)
        
    def create_search_section(self):
        """Membuat bagian pencarian produk"""
        search_frame = tk.Frame(
            self.frame,
            bg=self.colors['background'],
            pady=10
        )
        search_frame.pack(fill=tk.X)
        
        # Label pencarian
        tk.Label(
            search_frame,
            text="Cari Produk:",
            font=('Arial', 10),
            bg=self.colors['background'],
            fg=self.colors['text']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Entry pencarian
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=40
        )
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Tombol cari
        ttk.Button(
            search_frame,
            text="🔍 Cari",
            command=self.search_products
        ).pack(side=tk.LEFT, padx=5)
        
        # Bind event pencarian
        self.search_var.trace_add('write', lambda *args: self.search_products())
        
    def create_category_filter(self):
        """Membuat filter berdasarkan kategori"""
        filter_frame = tk.Frame(
            self.frame,
            bg=self.colors['background'],
            pady=10
        )
        filter_frame.pack(fill=tk.X)
        
        # Label filter
        tk.Label(
            filter_frame,
            text="Filter Kategori:",
            font=('Arial', 10),
            bg=self.colors['background'],
            fg=self.colors['text']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Combobox kategori
        categories = [
            "Semua",
            "Pakaian Muslim Pria",
            "Pakaian Muslim Wanita",
            "Perlengkapan Ibadah",
            "Aksesoris Muslim"
        ]
        
        self.category_var = tk.StringVar(value="Semua")
        category_cb = ttk.Combobox(
            filter_frame,
            textvariable=self.category_var,
            values=categories,
            width=20,
            state="readonly"
        )
        category_cb.pack(side=tk.LEFT)
        
        # Bind event perubahan kategori
        category_cb.bind('<<ComboboxSelected>>', lambda e: self.filter_products())
        
    def create_table(self):
        """Membuat tabel daftar produk"""
        # Frame untuk tabel
        table_frame = tk.Frame(
            self.frame,
            bg=self.colors['background']
        )
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Definisi kolom
        columns = (
            'ID',
            'Nama Produk',
            'Kategori',
            'Harga',
            'Stok',
            'Status'
        )
        
        # Buat Treeview
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            height=15
        )
        
        # Styling
        style = ttk.Style()
        style.configure(
            "Treeview",
            background="white",
            foreground=self.colors['text'],
            rowheight=25,
            fieldbackground="white"
        )
        style.map('Treeview',
                 background=[('selected', self.colors['primary'])])
        
        # Setup kolom-kolom
        for col in columns:
            self.tree.heading(col, text=col)
            width = 100
            if col == 'Nama Produk':
                width = 200
            elif col == 'Kategori':
                width = 150
            self.tree.column(col, width=width, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack komponen
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double click
        self.tree.bind('<Double-1>', self.on_item_double_click)

    def create_action_buttons(self):
        """Membuat tombol-tombol aksi"""
        button_frame = tk.Frame(
            self.frame,
            bg=self.colors['background']
        )
        button_frame.pack(fill=tk.X, pady=10)
        
        # Definisi tombol-tombol
        buttons = [
            ("✨ Tambah Produk", self.colors['success'], self.add_product),
            ("✏️ Edit", self.colors['primary'], self.edit_product),
            ("🗑️ Hapus", self.colors['error'], self.delete_product),
            ("🔄 Refresh", self.colors['accent'], self.refresh_data)
        ]
        
        # Buat tombol-tombol
        for text, color, command in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                font=('Arial', 10, 'bold'),
                bg=color,
                fg='white',
                padx=20,
                pady=10,
                command=command
            )
            btn.pack(side=tk.LEFT, padx=5)
            
            # Efek hover
            btn.bind(
                '<Enter>',
                lambda e, b=btn: b.configure(bg=self.colors['secondary'])
            )
            btn.bind(
                '<Leave>',
                lambda e, b=btn, c=color: b.configure(bg=c)
            )

    def refresh_data(self):
        """Memperbarui data produk di tabel"""
        # Hapus data existing
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Ambil data produk melalui controller
        products = self.controller.get_all_produk()
        
        # Update statistik
        total_products = len(products)
        low_stock = len([p for p in products if int(p['stok']) <= 10])
        self.stats_label.config(
            text=f"Total: {total_products} produk | Stok Menipis: {low_stock}"
        )
        
        # Masukkan data ke tabel
        for product in products:
            # Tentukan status stok
            stok = int(product['stok'])
            if stok == 0:
                status = "Habis"
                tags = ('out_of_stock',)
            elif stok <= 10:
                status = "Menipis"
                tags = ('low_stock',)
            else:
                status = "Tersedia"
                tags = ('in_stock',)
                
            # Insert ke tabel
            self.tree.insert(
                '',
                tk.END,
                values=(
                    product['id_produk'],
                    product['nama_produk'],
                    product['kategori'],
                    f"Rp {float(product['harga']):,}",
                    product['stok'],
                    status
                ),
                tags=tags
            )
            
        # Konfigurasi warna status
        self.tree.tag_configure(
            'out_of_stock',
            foreground=self.colors['error']
        )
        self.tree.tag_configure(
            'low_stock',
            foreground=self.colors['warning']
        )
        self.tree.tag_configure(
            'in_stock',
            foreground=self.colors['success']
        )

    def search_products(self, *args):
        """Mencari produk berdasarkan keyword"""
        keyword = self.search_var.get().lower()
        category = self.category_var.get()
        
        # Reset table
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Filter produk
        products = self.controller.get_all_produk()
        filtered_products = []
        
        for product in products:
            name_match = keyword in product['nama_produk'].lower()
            category_match = (
                category == "Semua" or 
                category == product['kategori']
            )
            
            if name_match and category_match:
                filtered_products.append(product)
                
        # Update statistik
        total_filtered = len(filtered_products)
        low_stock = len([p for p in filtered_products if int(p['stok']) <= 10])
        self.stats_label.config(
            text=f"Ditemukan: {total_filtered} produk | Stok Menipis: {low_stock}"
        )
        
        # Tampilkan hasil
        for product in filtered_products:
            stok = int(product['stok'])
            if stok == 0:
                status = "Habis"
                tags = ('out_of_stock',)
            elif stok <= 10:
                status = "Menipis"
                tags = ('low_stock',)
            else:
                status = "Tersedia"
                tags = ('in_stock',)
                
            self.tree.insert(
                '',
                tk.END,
                values=(
                    product['id_produk'],
                    product['nama_produk'],
                    product['kategori'],
                    f"Rp {float(product['harga']):,}",
                    product['stok'],
                    status
                ),
                tags=tags
            )
            
    def filter_products(self):
        """Filter produk berdasarkan kategori"""
        self.search_products()
        
    def on_item_double_click(self, event):
        """Handler untuk double click pada item"""
        selected = self.tree.selection()
        if not selected:
            return
            
        # Ambil ID produk yang dipilih
        product_id = self.tree.item(selected[0])['values'][0]
        
        # Tampilkan detail produk
        DetailProduk(
            self.parent,
            self.colors,
            product_id,
            callback=self.refresh_data
        )
        
    def add_product(self):
        """Membuka form tambah produk"""
        TambahProduk(
            self.parent,
            self.colors,
            callback=self.refresh_data
        )
        
    def edit_product(self):
        """Membuka form edit produk"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(
                "Peringatan",
                "Pilih produk yang akan diedit"
            )
            return
            
        # Ambil ID produk yang dipilih
        product_id = self.tree.item(selected[0])['values'][0]
        
        # Buka form edit
        EditProduk(
            self.parent,
            self.colors,
            product_id,
            callback=self.refresh_data
        )
        
    def delete_product(self):
        """Menghapus produk yang dipilih"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(
                "Peringatan",
                "Pilih produk yang akan dihapus"
            )
            return
            
        # Ambil data produk yang dipilih
        product_id = self.tree.item(selected[0])['values'][0]
        product_name = self.tree.item(selected[0])['values'][1]
        
        # Konfirmasi penghapusan
        if messagebox.askyesno(
            "Konfirmasi",
            f"Yakin ingin menghapus produk {product_name}?"
        ):
            # Gunakan controller untuk menghapus
            success = self.controller.delete_produk(product_id)
            
            if success:
                messagebox.showinfo(
                    "Sukses",
                    "Produk berhasil dihapus"
                )
                self.refresh_data()
            else:
                messagebox.showerror(
                    "Error",
                    "Gagal menghapus produk"
                )
