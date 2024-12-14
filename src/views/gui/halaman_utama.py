import tkinter as tk
from tkinter import ttk
from datetime import datetime
from utils.database import DatabaseManager
from views.gui.produk.tambah_produk import TambahProduk

class HalamanUtama:
    def __init__(self, parent, colors):
        self.parent = parent
        self.colors = colors
        self.db = DatabaseManager()
        
        # Frame utama
        self.frame = tk.Frame(
            self.parent,
            bg=self.colors['background']
        )
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.create_welcome_section()
        self.create_quick_stats()
        self.create_quick_actions()
       
    def create_welcome_section(self):
       """Membuat bagian selamat datang"""
       welcome_frame = tk.Frame(self.frame, bg=self.colors['background'])
       welcome_frame.pack(fill=tk.X, pady=(0, 20))
       
       # Label selamat datang dengan efek bayangan
       welcome_text = tk.Label(
           welcome_frame,
           text="Selamat Datang di HalalHub",
           font=('Arial', 24, 'bold'),
           bg=self.colors['background'],
           fg=self.colors['primary']
       )
       welcome_text.pack(pady=(0, 5))
       
       # Tanggal dan waktu
       self.date_label = tk.Label(
           welcome_frame,
           text="",
           font=('Arial', 12),
           bg=self.colors['background'],
           fg=self.colors['text']
       )
       self.date_label.pack()
       
       # Update waktu otomatis
       self.update_datetime()

    def update_datetime(self):
       try:
           if not self.date_label.winfo_exists():
               return
           current_time = datetime.now()
           self.date_label.config(text=current_time.strftime("%d %B %Y %H:%M:%S"))
           self.parent.after(1000, self.update_datetime)
       except Exception:
           # If widget is destroyed, stop updating
           pass

    def create_quick_stats(self):
        """Membuat bagian statistik cepat"""
        try:
            stats_frame = tk.Frame(self.frame, bg=self.colors['background'])
            stats_frame.pack(fill=tk.X, pady=20)

            # Get actual stats untuk produk
            products = self.db.get_all_produk()
            total_products = len(products) if products else 0
            low_stock = len([p for p in products if int(p.get('stok', 0)) <= 10]) if products else 0

            # Get today's orders dan pendapatan dari pesanan
            today = datetime.now().date()

            # Ambil semua pesanan
            pesanan_list = self.db.get_all_pesanan()

            # Filter pesanan hari ini
            today_orders = [
                order for order in pesanan_list 
                if datetime.strptime(order['tanggal_pesanan']).date() == today
            ] if pesanan_list else []

            # Hitung total pendapatan hari ini (dari pesanan yang selesai)
            daily_revenue = sum(
                float(order['total_harga']) 
                for order in today_orders 
                if order['status'] == 'Selesai'
            )

            # Hitung jumlah pesanan hari ini
            daily_orders = len(today_orders)

            # Membuat grid 2x2 untuk statistik
            stats_data = [
                ("Total Produk", str(total_products), self.colors['primary']),
                ("Pesanan Hari Ini", str(daily_orders), self.colors['accent']),
                ("Stok Menipis", str(low_stock), self.colors['warning']),
                ("Pendapatan Hari Ini", f"Rp {daily_revenue:,.0f}", self.colors['success'])
            ]

            for i, (title, value, color) in enumerate(stats_data):
                stat_container = tk.Frame(
                    stats_frame,
                    bg='white',
                    padx=15,
                    pady=15,
                    relief=tk.RAISED,
                    bd=1
                )
                row = i // 2
                col = i % 2
                stat_container.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')

                tk.Label(
                    stat_container,
                    text=title,
                    font=('Arial', 12),
                    bg='white',
                    fg=self.colors['text']
                ).pack(anchor='w')

                tk.Label(
                    stat_container,
                    text=value,
                    font=('Arial', 20, 'bold'),
                    bg='white',
                    fg=color
                ).pack(anchor='w', pady=(5, 0))

            stats_frame.grid_columnconfigure(0, weight=1)
            stats_frame.grid_columnconfigure(1, weight=1)

        except Exception as e:
            print(f"Error creating quick stats: {str(e)}")
            # Fallback stats jika terjadi error
            self.show_error_stats(stats_frame)

    def show_error_stats(self, parent_frame):
        """Menampilkan statistik default jika terjadi error"""
        error_stats = [
            ("Total Produk", "0", self.colors['primary']),
            ("Pesanan Hari Ini", "0", self.colors['accent']), 
            ("Stok Menipis", "0", self.colors['warning']),
            ("Pendapatan Hari Ini", "Rp 0", self.colors['success'])
        ]

        for i, (title, value, color) in enumerate(error_stats):
            stat_container = tk.Frame(
                parent_frame,
                bg='white',
                padx=15,
                pady=15,
                relief=tk.RAISED,
                bd=1
            )
            row = i // 2
            col = i % 2
            stat_container.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')

            tk.Label(
                stat_container,
                text=title,
                font=('Arial', 12),
                bg='white',
                fg=self.colors['text']
            ).pack(anchor='w')

            tk.Label(
                stat_container,
                text=value,
                font=('Arial', 20, 'bold'),
                bg='white',
                fg=color
            ).pack(anchor='w', pady=(5, 0))

    def create_quick_actions(self):
       """Membuat bagian aksi cepat"""
       actions_frame = tk.Frame(self.frame, bg=self.colors['background'])
       actions_frame.pack(fill=tk.X, pady=20)
       
       tk.Label(
           actions_frame,
           text="Aksi Cepat",
           font=('Arial', 16, 'bold'),
           bg=self.colors['background'],
           fg=self.colors['text']
       ).pack(anchor='w', pady=(0, 10))
       
       buttons_frame = tk.Frame(actions_frame, bg=self.colors['background'])
       buttons_frame.pack(fill=tk.X)
       
       quick_actions = [
           ("Tambah Produk", "📦", self.add_product),
           ("Input Pesanan", "📝", self.add_order),
           ("Laporan Harian", "📊", self.show_daily_report),
       ]
       
       for i, (text, emoji, command) in enumerate(quick_actions):
           button = tk.Button(
               buttons_frame,
               text=f"{emoji}\n{text}",
               font=('Arial', 12),
               bg='white',
               fg=self.colors['text'],
               relief=tk.RAISED,
               command=command,
               width=15,
               height=3
           )
           button.grid(row=0, column=i, padx=5)
           
           button.bind('<Enter>', lambda e, btn=button: self.on_hover(btn, True))
           button.bind('<Leave>', lambda e, btn=button: self.on_hover(btn, False))
           
       buttons_frame.grid_columnconfigure((0,1,2,3), weight=1)
   
    def on_hover(self, button, entering):
       """Efek hover untuk tombol"""
       if entering:
           button.config(
               bg=self.colors['accent'],
               fg='white'
           )
       else:
           button.config(
               bg='white',
               fg=self.colors['text']
           )
   
    def refresh_dashboard(self):
        """Memperbarui dashboard"""
        try:
            # Clear existing frames except main frame
            for widget in self.frame.winfo_children():
                if isinstance(widget, tk.Frame) and widget != self.frame:
                    widget.destroy()

            # Get current date range
            today = datetime.now()
            today_start = today.replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = today.replace(hour=23, minute=59, second=59, microsecond=999999)

            # Get data for quick stats
            products = self.db.get_all_produk()
            total_products = len(products)
            low_stock = len([p for p in products if int(p['stok']) <= 10])

            # Get today's orders and revenue
            report = self.db.generate_laporan_penjualan(today_start, today_end)
            daily_orders = report['jumlah_transaksi']
            daily_revenue = report['total_penjualan']

            # Store values that will be needed in create_quick_stats
            self._dashboard_data = {
                'total_products': total_products,
                'low_stock': low_stock,
                'daily_orders': daily_orders,
                'daily_revenue': daily_revenue
            }

            # Recreate dashboard sections with updated data
            self.create_welcome_section()
            self.create_quick_stats()
            self.create_quick_actions()

        except Exception as e:
            print(f"Error refreshing dashboard: {str(e)}")
    
    def add_product(self):
        """Menambah produk baru"""
        TambahProduk(self.parent, self.colors, callback=self.refresh_dashboard)

    def add_order(self):
        """Menambah pesanan baru"""
        from views.gui.pesanan.input_pesanan import InputPesanan
        InputPesanan(parent=self.parent, colors=self.colors, callback=self.refresh_dashboard)

    def show_daily_report(self):
        """Menampilkan laporan harian"""
        from views.gui.laporan.laporan_penjualan import LaporanPenjualan
        # Buka halaman laporan penjualan & set callback
        LaporanPenjualan(self.parent, self.colors)
        self.refresh_dashboard()