import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from controllers.pesanan_controller import PesananController
from .input_pesanan import InputPesanan
from .detail_pesanan import DetailPesanan 
from .pembatalan_pesanan import PembatalanPesanan

class DaftarPesanan:
    def __init__(self, parent, colors):
        """
        Inisialisasi tampilan daftar pesanan
        
        Args:
            parent: Widget parent untuk frame ini
            colors: Dictionary berisi kode warna untuk UI
        """
        # Inisialisasi properti dasar
        self.parent = parent
        self.colors = colors
        self.controller = PesananController()
        
        # Buat frame utama dengan gradient background
        self.frame = tk.Frame(
            self.parent,
            bg=self.colors['background']
        )
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Inisialisasi komponen UI
        self.create_header()
        self.create_filter_section()
        self.create_table_section()
        self.create_action_buttons()
        
        # Load data awal
        self.refresh_data()

    def create_header(self):
        """Membuat bagian header dengan judul dan counter pesanan aktif"""
        # Frame untuk header dengan warna primary
        header_frame = tk.Frame(
            self.frame, 
            bg=self.colors['primary']
        )
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Label judul dengan efek shadow
        title = tk.Label(
            header_frame,
            text="Daftar Pesanan",
            font=('Arial', 24, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            padx=20,
            pady=10
        )
        title.pack(side=tk.LEFT)
        
        # Counter pesanan aktif di kanan header
        self.active_orders = tk.StringVar(value="0 Pesanan Aktif")
        counter = tk.Label(
            header_frame,
            textvariable=self.active_orders,
            font=('Arial', 12),
            bg=self.colors['primary'],
            fg='white',
            pady=10
        )
        counter.pack(side=tk.RIGHT, padx=20)

    def create_filter_section(self):
        """Membuat bagian filter untuk memfilter pesanan berdasarkan status"""
        # Frame untuk bagian filter
        filter_frame = tk.LabelFrame(
            self.frame,
            text="Filter Pesanan",
            bg=self.colors['background'],
            fg=self.colors['text'],
            font=('Arial', 10, 'bold'),
            padx=10,
            pady=10
        )
        filter_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Label dan dropdown untuk filter status
        tk.Label(
            filter_frame,
            text="Status:",
            bg=self.colors['background'],
            fg=self.colors['text']
        ).pack(side=tk.LEFT, padx=5)
        
        # Opsi status pesanan
        status_options = ["Semua", "Pending", "Selesai", "Dibatalkan"]
        self.status_var = tk.StringVar(value="Semua")
        status_cb = ttk.Combobox(
            filter_frame,
            textvariable=self.status_var,
            values=status_options,
            width=15,
            state="readonly"
        )
        status_cb.pack(side=tk.LEFT, padx=5)
        
        # Bind event perubahan status untuk auto refresh
        status_cb.bind('<<ComboboxSelected>>', lambda e: self.refresh_data())
        
        # Tombol refresh di kanan
        refresh_btn = tk.Button(
            filter_frame,
            text="🔄 Refresh",
            font=('Arial', 10),
            bg=self.colors['accent'],
            fg='white',
            relief=tk.RAISED,
            command=self.refresh_data
        )
        refresh_btn.pack(side=tk.RIGHT, padx=5)

    def create_table_section(self):
        """Membuat tabel untuk menampilkan daftar pesanan"""
        # Frame untuk tabel
        table_frame = tk.Frame(
            self.frame, 
            bg=self.colors['background']
        )
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Definisi kolom tabel
        columns = (
            'ID Pesanan', 
            'Tanggal', 
            'Pelanggan', 
            'Produk',
            'Jumlah',
            'Total',
            'Status'
        )
        
        # Buat Treeview dengan styling
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            height=15
        )
        
        # Konfigurasi style tabel
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
        
        # Setup kolom-kolom tabel
        for col in columns:
            self.tree.heading(col, text=col)
            # Atur lebar kolom
            width = 150 if col in ['Produk', 'Pelanggan'] else 100
            self.tree.column(col, width=width, anchor='center')
        
        # Tambah scrollbar
        y_scroll = ttk.Scrollbar(
            table_frame,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )
        x_scroll = ttk.Scrollbar(
            table_frame,
            orient=tk.HORIZONTAL,
            command=self.tree.xview
        )
        self.tree.configure(
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set
        )
        
        # Pack komponen tabel
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind event double click
        self.tree.bind('<Double-1>', self.on_item_double_click)

    def create_action_buttons(self):
        """Membuat tombol-tombol aksi untuk manajemen pesanan"""
        # Frame untuk tombol-tombol
        button_frame = tk.Frame(
            self.frame,
            bg=self.colors['background']
        )
        button_frame.pack(fill=tk.X, pady=20)
        
        # Definisi tombol-tombol
        buttons = [
            ("✨ Pesanan Baru", self.colors['success'], self.add_new_order),
            ("✏️ Edit", self.colors['primary'], self.edit_order),
            ("❌ Batalkan", self.colors['error'], self.cancel_order),
            ("✅ Selesai", self.colors['accent'], self.complete_order)
        ]
        
        # Buat setiap tombol
        for text, color, command in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                font=('Arial', 10, 'bold'),
                bg=color,
                fg='white',
                relief=tk.RAISED,
                padx=20,
                pady=10,
                command=command
            )
            btn.pack(side=tk.LEFT, padx=5)
            
            # Tambah efek hover
            btn.bind(
                '<Enter>',
                lambda e, b=btn: b.configure(bg=self.colors['secondary'])
            )
            btn.bind(
                '<Leave>',
                lambda e, b=btn, c=color: b.configure(bg=c)
            )

    def refresh_data(self):
        """Memperbarui data pesanan di tabel"""
        try:
            # Hapus data existing
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            # Get pesanan from controller
            pesanan_list = self.controller.lihat_daftar_pesanan(
                None if self.status_var.get() == "Semua" else self.status_var.get()
            )
            
            # Update counter pesanan aktif 
            active_count = len([p for p in pesanan_list if p.status == "Pending"])
            self.active_orders.set(f"{active_count} Pesanan Aktif")
            
            # Load data produk untuk mendapatkan nama produk
            products = self.controller.db.get_all_produk()
            product_map = {p['id_produk']: p['nama_produk'] for p in products}
            
            # Display pesanan
            for pesanan in pesanan_list:
                # Get product name
                product_name = product_map.get(pesanan.id_produk, pesanan.id_produk)
                
                values = (
                    pesanan.id_pesanan,
                    datetime.fromisoformat(pesanan.tanggal_pesanan).strftime("%d/%m/%Y %H:%M"),
                    pesanan.id_pelanggan, 
                    product_name,
                    pesanan.jumlah_dipesan,
                    f"Rp {pesanan.total_harga:,}",
                    pesanan.status
                )
                
                # Set row tags based on status
                tags = ()
                if pesanan.status == "Selesai":
                    tags = ('completed',)
                elif pesanan.status == "Dibatalkan":
                    tags = ('cancelled',)
                elif pesanan.status == "Pending":
                    tags = ('pending',)
                    
                self.tree.insert('', tk.END, values=values, tags=tags)
                
        except Exception as e:
            print(f"Error refreshing data: {str(e)}")
            messagebox.showerror(
                "Error",
                "Gagal memperbarui data pesanan"
            )
            
    def on_item_double_click(self, event):
        """Handler untuk event double click pada item tabel"""
        selected = self.tree.selection()
        if not selected:
            return
            
        # Ambil ID pesanan yang dipilih
        pesanan_id = self.tree.item(selected[0])['values'][0]
        
        # Buka window detail pesanan
        DetailPesanan(
            self.parent,
            self.colors,
            pesanan_id,
            callback=self.refresh_data
        )

    def add_new_order(self):
        """Membuka form input pesanan baru"""
        InputPesanan(
            self.parent,
            self.colors,
            callback=self.refresh_data
        )

    def edit_order(self):
        """Mengedit pesanan yang dipilih"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(
                "Peringatan",
                "Pilih pesanan yang akan diedit"
            )
            return
            
        # Ambil ID pesanan yang dipilih    
        pesanan_id = self.tree.item(selected[0])['values'][0]
        
        # Buka form edit pesanan
        InputPesanan(
            self.parent,
            self.colors,
            pesanan_id=pesanan_id,
            callback=self.refresh_data
        )

    def cancel_order(self):
        """Membatalkan pesanan yang dipilih"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(
                "Peringatan",
                "Pilih pesanan yang akan dibatalkan"
            )
            return
            
        # Ambil ID pesanan yang dipilih
        pesanan_id = self.tree.item(selected[0])['values'][0]
        
        # Buka window pembatalan pesanan
        PembatalanPesanan(
            self.parent,
            self.colors,
            pesanan_id,
            callback=self.refresh_data
        )

    def complete_order(self):
        """Menandai pesanan sebagai selesai"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(
                "Peringatan",
                "Pilih pesanan yang akan diselesaikan"
            )
            return
            
        pesanan_id = self.tree.item(selected[0])['values'][0]
        current_status = self.tree.item(selected[0])['values'][6]  # Status ada di index 6
        
        # Validasi status sebelum melanjutkan
        if current_status == "Selesai":
            messagebox.showerror(
                "Error",
                "Pesanan ini sudah selesai"
            )
            return
        elif current_status == "Dibatalkan":
            messagebox.showerror(
                "Error", 
                "Tidak dapat menyelesaikan pesanan yang sudah dibatalkan"
            )
            return
        
        # Konfirmasi penyelesaian
        if messagebox.askyesno(
            "Konfirmasi",
            "Yakin ingin menyelesaikan pesanan ini?"
        ):
            # Proses penyelesaian pesanan
            success, message = self.controller.mark_as_done(pesanan_id)
            
            if success:
                messagebox.showinfo(
                    "Sukses",
                    "Pesanan telah diselesaikan"
                )
                self.refresh_data()
            else:
                messagebox.showerror(
                    "Error",
                    message or "Gagal menyelesaikan pesanan"
                )