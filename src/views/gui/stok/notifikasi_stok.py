# src/views/gui/stok/notifikasi_stok.py
import tkinter as tk
from tkinter import ttk
from ....controllers.notification_controller import NotificationController
from datetime import datetime

class NotifikasiStok:
    def __init__(self, parent, colors):
        """
        Inisialisasi halaman notifikasi stok
        
        Args:
            parent: Widget parent untuk frame ini
            colors: Dictionary berisi kode warna untuk UI
        """
        self.parent = parent
        self.colors = colors
        self.controller = NotificationController()
        
        # Frame utama
        self.frame = tk.Frame(
            self.parent,
            bg=self.colors['background']
        )
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Inisialisasi komponen UI
        self.create_header()
        self.create_notification_list()
        self.create_settings_section()
        
        # Load notifikasi
        self.refresh_notifications()
        
    def create_header(self):
        """Membuat bagian header"""
        header_frame = tk.Frame(
            self.frame,
            bg=self.colors['warning'],
            padx=20,
            pady=15
        )
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Icon dan judul
        tk.Label(
            header_frame,
            text="🔔",  # Bell emoji
            font=('Arial', 24),
            bg=self.colors['warning'],
            fg='white'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(
            header_frame,
            text="Notifikasi Stok",
            font=('Arial', 24, 'bold'),
            bg=self.colors['warning'],
            fg='white'
        ).pack(side=tk.LEFT)
        
        # Counter notifikasi
        self.notif_count = tk.StringVar(value="0 Notifikasi")
        tk.Label(
            header_frame,
            textvariable=self.notif_count,
            font=('Arial', 12),
            bg=self.colors['warning'],
            fg='white'
        ).pack(side=tk.RIGHT)
        
    def create_notification_list(self):
        """Membuat daftar notifikasi"""
        # Frame untuk notifikasi
        notification_frame = tk.Frame(
            self.frame,
            bg=self.colors['background']
        )
        notification_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Scrollable canvas
        canvas = tk.Canvas(
            notification_frame,
            bg=self.colors['background'],
            highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(
            notification_frame,
            orient="vertical",
            command=canvas.yview
        )
        self.notification_container = tk.Frame(
            canvas,
            bg=self.colors['background']
        )
        
        # Configure canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        self.notification_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Create window inside canvas
        canvas.create_window((0, 0), window=self.notification_container, anchor="nw")
        
        # Pack components
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_settings_section(self):
        """Membuat bagian pengaturan notifikasi"""
        settings_frame = tk.LabelFrame(
            self.frame,
            text="Pengaturan Notifikasi",
            font=('Arial', 10, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['text'],
            padx=20,
            pady=10
        )
        settings_frame.pack(fill=tk.X)
        
        # Batas minimum stok
        tk.Label(
            settings_frame,
            text="Batas Minimum Stok:",
            font=('Arial', 10),
            bg=self.colors['background'],
            fg=self.colors['text']
        ).pack(side=tk.LEFT)
        
        self.min_stock_var = tk.StringVar(value="10")
        ttk.Spinbox(
            settings_frame,
            from_=1,
            to=100,
            textvariable=self.min_stock_var,
            width=5
        ).pack(side=tk.LEFT, padx=5)
        
        # Checkbox untuk enable/disable notifikasi
        self.enable_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            settings_frame,
            text="Aktifkan Notifikasi",
            variable=self.enable_var,
            command=self.toggle_notifications
        ).pack(side=tk.LEFT, padx=20)
        
        # Tombol refresh
        tk.Button(
            settings_frame,
            text="🔄 Refresh",
            font=('Arial', 10),
            bg=self.colors['primary'],
            fg='white',
            command=self.refresh_notifications
        ).pack(side=tk.RIGHT)
        
    def create_notification_card(self, notification):
        """Membuat card untuk satu notifikasi"""
        # Frame untuk satu notifikasi
        card = tk.Frame(
            self.notification_container,
            bg='white',
            padx=15,
            pady=10,
            relief=tk.RAISED,
            bd=1
        )
        card.pack(fill=tk.X, pady=5)
        
        # Header card dengan warna sesuai tipe notifikasi
        header_color = (
            self.colors['error'] if notification['stok_tersisa'] == 0
            else self.colors['warning']
        )
        
        header = tk.Frame(card, bg=header_color)
        header.pack(fill=tk.X, pady=(0, 10))
        
        # Icon dan judul
        tk.Label(
            header,
            text="⚠️" if notification['stok_tersisa'] == 0 else "⚠️",
            font=('Arial', 14),
            bg=header_color,
            fg='white'
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        tk.Label(
            header,
            text=f"Stok {notification['nama_produk']}",
            font=('Arial', 12, 'bold'),
            bg=header_color,
            fg='white'
        ).pack(side=tk.LEFT, pady=5)
        
        # Timestamp
        tk.Label(
            header,
            text=notification['timestamp'].strftime("%d/%m/%Y %H:%M"),
            font=('Arial', 9),
            bg=header_color,
            fg='white'
        ).pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Pesan notifikasi
        message = tk.Label(
            card,
            text=notification['pesan'],
            font=('Arial', 10),
            bg='white',
            fg=self.colors['text'],
            justify=tk.LEFT,
            wraplength=400
        )
        message.pack(anchor='w')
        
        # Tombol aksi
        action_frame = tk.Frame(card, bg='white')
        action_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Button(
            action_frame,
            text="🔍 Lihat Detail",
            font=('Arial', 9),
            bg=self.colors['primary'],
            fg='white',
            command=lambda: self.show_product_detail(notification['id_produk'])
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            action_frame,
            text="✖ Tutup",
            font=('Arial', 9),
            bg=self.colors['secondary'],
            fg='white',
            command=lambda: self.dismiss_notification(notification['id_produk'])
        ).pack(side=tk.LEFT)
        
    def refresh_notifications(self):
        """Memperbarui daftar notifikasi"""
        # Hapus notifikasi lama
        for widget in self.notification_container.winfo_children():
            widget.destroy()
            
        if not self.enable_var.get():
            # Tampilkan pesan jika notifikasi dinonaktifkan
            tk.Label(
                self.notification_container,
                text="Notifikasi dinonaktifkan",
                font=('Arial', 12),
                bg=self.colors['background'],
                fg=self.colors['text']
            ).pack(pady=20)
            self.notif_count.set("0 Notifikasi")
            return
            
        # Ambil notifikasi dari controller
        notifications = self.controller.get_semua_notifikasi()
        
        if not notifications:
            tk.Label(
                self.notification_container,
                text="Tidak ada notifikasi",
                font=('Arial', 12),
                bg=self.colors['background'],
                fg=self.colors['text']
            ).pack(pady=20)
            self.notif_count.set("0 Notifikasi")
            return
            
        # Update counter
        self.notif_count.set(f"{len(notifications)} Notifikasi")
        
        # Tampilkan setiap notifikasi
        for notif in notifications:
            self.create_notification_card(notif)
            
    def toggle_notifications(self):
        """Handler untuk toggle notifikasi"""
        self.refresh_notifications()
        
    def show_product_detail(self, product_id):
        """Handler untuk menampilkan detail produk"""
        # TODO: Implement product detail view
        pass
        
    def dismiss_notification(self, product_id):
        """Handler untuk menutup notifikasi"""
        if self.controller.hapus_notifikasi(product_id):
            self.refresh_notifications()
