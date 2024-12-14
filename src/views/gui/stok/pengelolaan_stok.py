import tkinter as tk
from tkinter import ttk, messagebox
from controllers.produk_controller import ProdukController 
from utils.database import DatabaseManager
from datetime import datetime

class PengelolaanStok:
    """Kelas untuk mengelola stok produk"""
    def __init__(self, parent, colors):
        self.parent = parent
        self.colors = colors
        self.controller = ProdukController()
        self.db = DatabaseManager()

        # Frame utama
        self.frame = tk.Frame(
            self.parent,
            bg=self.colors['background']
        )
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.create_header()
        self.create_filter_section()
        self.create_table()
        self.create_adjustment_section()
        self.refresh_data()
        
    def create_header(self):
        """Membuat bagian header dengan judul dan statistik"""
        header_frame = tk.Frame(
            self.frame,
            bg=self.colors['primary'],
            padx=20,
            pady=15
        )
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Label judul
        tk.Label(
            header_frame,
            text="Pengelolaan Stok",
            font=('Arial', 24, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        ).pack(side=tk.LEFT)
        
        # Statistik stok
        self.stats_var = tk.StringVar()
        tk.Label(
            header_frame,
            textvariable=self.stats_var,
            font=('Arial', 12),
            bg=self.colors['primary'],
            fg='white'
        ).pack(side=tk.RIGHT)
        
    def create_filter_section(self):
        """Membuat bagian filter untuk stok"""
        filter_frame = tk.LabelFrame(
            self.frame,
            text="Filter",
            font=('Arial', 10, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['text'],
            padx=10,
            pady=10
        )
        filter_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Kategori filter
        tk.Label(
            filter_frame,
            text="Kategori:",
            font=('Arial', 10),
            bg=self.colors['background'],
            fg=self.colors['text']
        ).pack(side=tk.LEFT, padx=5)
        
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
        category_cb.pack(side=tk.LEFT, padx=5)
        
        # Status stok filter
        tk.Label(
            filter_frame,
            text="Status:",
            font=('Arial', 10),
            bg=self.colors['background'],
            fg=self.colors['text']
        ).pack(side=tk.LEFT, padx=5)
        
        statuses = ["Semua", "Stok Aman", "Stok Menipis", "Habis"]
        self.status_var = tk.StringVar(value="Semua")
        status_cb = ttk.Combobox(
            filter_frame,
            textvariable=self.status_var,
            values=statuses,
            width=15,
            state="readonly"
        )
        status_cb.pack(side=tk.LEFT, padx=5)
        
        # Bind event
        category_cb.bind('<<ComboboxSelected>>', lambda e: self.refresh_data())
        status_cb.bind('<<ComboboxSelected>>', lambda e: self.refresh_data())
        
    def create_table(self):
        """Membuat tabel untuk menampilkan stok produk"""
        table_frame = tk.Frame(
            self.frame,
            bg=self.colors['background']
        )
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Buat Treeview
        columns = (
            'ID Produk',
            'Nama Produk',
            'Kategori',
            'Stok',
            'Min Stok',
            'Status'
        )
        
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            height=10
        )
        
        # Setup kolom
        for col in columns:
            self.tree.heading(col, text=col)
            width = 150 if col in ['Nama Produk', 'Kategori'] else 100
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
        
    def create_adjustment_section(self):
        """Membuat bagian penyesuaian stok"""
        adjust_frame = tk.LabelFrame(
            self.frame,
            text="Penyesuaian Stok",
            font=('Arial', 10, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['text'],
            padx=20,
            pady=10
        )
        adjust_frame.pack(fill=tk.X, pady=(0, 20))
        
        # ID Produk
        tk.Label(
            adjust_frame,
            text="ID Produk:",
            font=('Arial', 10),
            bg=self.colors['background'],
            fg=self.colors['text']
        ).grid(row=0, column=0, sticky='w', pady=5)
        
        self.id_var = tk.StringVar()
        ttk.Entry(
            adjust_frame,
            textvariable=self.id_var,
            state='readonly',
            width=20
        ).grid(row=0, column=1, sticky='w', padx=5)
        
        # Jumlah Perubahan
        tk.Label(
            adjust_frame,
            text="Jumlah:",
            font=('Arial', 10),
            bg=self.colors['background'],
            fg=self.colors['text']
        ).grid(row=0, column=2, sticky='w', padx=20)
        
        self.qty_var = tk.StringVar(value="0")
        vcmd = (self.frame.register(self.validate_number), '%P')
        ttk.Spinbox(
            adjust_frame,
            from_=-9999,
            to=9999,
            textvariable=self.qty_var,
            width=10,
            validate='key',
            validatecommand=vcmd
        ).grid(row=0, column=3, sticky='w')
        
        # Tombol Update
        ttk.Button(
            adjust_frame,
            text="Update Stok",
            command=self.update_stock,
            style='Primary.TButton'
        ).grid(row=0, column=4, padx=20)
        
    def create_history_section(self):
        """Membuat bagian riwayat perubahan stok"""
        history_frame = tk.LabelFrame(
            self.frame,
            text="Riwayat Perubahan",
            font=('Arial', 10, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['text'],
            padx=20,
            pady=10
        )
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tabel riwayat
        columns = (
            'Tanggal',
            'Produk',
            'Perubahan',
            'Stok Akhir',
            'Keterangan'
        )
        
        self.history_tree = ttk.Treeview(
            history_frame,
            columns=columns,
            show='headings',
            height=5
        )
        
        # Setup kolom
        for col in columns:
            self.history_tree.heading(col, text=col)
            width = 200 if col == 'Keterangan' else 100
            self.history_tree.column(col, width=width)
            
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            history_frame,
            orient=tk.VERTICAL,
            command=self.history_tree.yview
        )
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack komponen
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def validate_number(self, value):
        """Validasi input angka"""
        if not value:
            return True
        try:
            int(value)
            return True
        except ValueError:
            return False
            
    def update_stock(self):
        """Handler untuk update stok"""
        if not self.id_var.get():
            messagebox.showwarning(
                "Peringatan",
                "Pilih produk terlebih dahulu"
            )
            return
            
        try:
            qty = int(self.qty_var.get())
            if qty == 0:
                messagebox.showwarning(
                    "Peringatan",
                    "Masukkan jumlah perubahan"
                )
                return
                
            # Update stok
            success = self.controller.update_stock(
                self.id_var.get(),
                qty
            )
            
            if success:
                messagebox.showinfo(
                    "Sukses",
                    "Stok berhasil diperbarui"
                )
                self.refresh_data()
                self.id_var.set("")
                self.qty_var.set("0")
            else:
                messagebox.showerror(
                    "Error",
                    "Gagal memperbarui stok"
                )
                
        except ValueError:
            messagebox.showerror(
                "Error",
                "Jumlah tidak valid"
            )
            
    def refresh_data(self):
        """Memperbarui tampilan data"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Get products from database
        products = self.db.get_all_produk()
        
        # Apply filters
        category = self.category_var.get()
        status = self.status_var.get()
        
        filtered_products = []
        total_products = 0
        low_stock = 0
        out_of_stock = 0
        
        for product in products:
            # Category filter
            if category != "Semua" and product['kategori'] != category:
                continue
                
            # Status filter
            stok = int(product['stok'])
            product_status = "Stok Aman"
            tags = ('normal',)
            
            if stok == 0:
                product_status = "Habis"
                tags = ('habis',)
                out_of_stock += 1
            elif stok <= 10:
                product_status = "Stok Menipis"
                tags = ('menipis',)
                low_stock += 1
                
            if status != "Semua" and status != product_status:
                continue
                
            filtered_products.append(product)
            total_products += 1
            
            # Insert to table
            self.tree.insert(
                '',
                tk.END,
                values=(
                    product['id_produk'],
                    product['nama_produk'],
                    product['kategori'],
                    product['stok'],
                    "10",  # Minimum stock threshold
                    product_status
                ),
                tags=tags
            )
            
        # Configure tags
        self.tree.tag_configure(
            'normal',
            background=self.colors['success'],
            foreground='white'
        )
        self.tree.tag_configure(
            'menipis',
            background=self.colors['warning'],
            foreground='black'
        )
        self.tree.tag_configure(
            'habis',
            background=self.colors['error'],
            foreground='white'
        )
        
        # Update statistics
        self.stats_var.set(
            f"Total: {total_products} | "
            f"Stok Menipis: {low_stock} | "
            f"Habis: {out_of_stock}"
        )