import tkinter as tk
from typing import List, Dict, Optional
from datetime import datetime
from controllers.notification_controller import NotificationController

class Notification:
    def __init__(self, parent, colors):
        """Inisialisasi sistem notifikasi"""
        self.parent = parent
        self.colors = colors
        self.controller = NotificationController()
        
    def create_notification_window(self):
        """Membuat window popup untuk notifikasi"""
        self.notif_window = tk.Toplevel(self.parent)
        self.notif_window.title("Notifikasi")
        self.notif_window.geometry("300x400")
        self.notif_window.configure(bg='white')
        
        # Header
        header_frame = tk.Frame(
            self.notif_window,
            bg=self.colors['primary'],
            height=40
        )
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="Notifikasi",
            font=('Arial', 12, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        ).pack(side=tk.LEFT, padx=10, pady=5)
        
        # Container untuk daftar notifikasi
        self.notif_container = tk.Frame(
            self.notif_window,
            bg='white'
        )
        self.notif_container.pack(fill=tk.BOTH, expand=True)
        
        # Tampilkan notifikasi
        self.show_notifications()
        
    def check_stock_notification(self, product_info: Dict):
        """
        Cek dan tambah notifikasi stok jika diperlukan
        """
        notif = self.controller.beri_notifikasi(product_info)
        if notif:
            self.show_notifications()
            return True
        return False
    
    def show_notifications(self):
        """Menampilkan semua notifikasi dalam window"""
        # Bersihkan container
        for widget in self.notif_container.winfo_children():
            widget.destroy()
            
        notifications = self.controller.get_semua_notifikasi()
        if not notifications:
            # Tampilkan pesan jika tidak ada notifikasi
            tk.Label(
                self.notif_container,
                text="Tidak ada notifikasi",
                font=('Arial', 10),
                bg='white',
                fg=self.colors['text']
            ).pack(pady=20)
            return
            
        # Tampilkan setiap notifikasi
        for notif in reversed(notifications):
            self.create_notification_card(notif)
    
    def create_notification_card(self, notif):
        """Membuat card untuk satu notifikasi"""
        # Frame untuk satu notifikasi
        card = tk.Frame(
            self.notif_container,
            bg='white',
            bd=1,
            relief=tk.SOLID
        )
        card.pack(fill=tk.X, padx=10, pady=5)
        
        # Header notifikasi dengan warna sesuai tipe
        header_color = (self.colors['error'] if notif['type'] == 'error' 
                       else self.colors['warning'] if notif['type'] == 'warning'
                       else self.colors['primary'])
        
        header = tk.Frame(card, bg=header_color, height=30)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text=notif['title'],
            font=('Arial', 10, 'bold'),
            bg=header_color,
            fg='white'
        ).pack(side=tk.LEFT, padx=10, pady=5)
        
        # Timestamp
        tk.Label(
            header,
            text=notif['timestamp'].strftime("%H:%M"),
            font=('Arial', 8),
            bg=header_color,
            fg='white'
        ).pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Pesan notifikasi
        message = tk.Label(
            card,
            text=notif['message'],
            font=('Arial', 9),
            bg='white',
            fg=self.colors['text'],
            wraplength=250,
            justify=tk.LEFT
        )
        message.pack(fill=tk.X, padx=10, pady=10)
        
        # Tombol aksi
        button_frame = tk.Frame(card, bg='white')
        button_frame.pack(fill=tk.X, padx=10, pady=(0,10))
        
        # Tombol tutup notifikasi
        tk.Button(
            button_frame,
            text="Tutup",
            bg=self.colors['secondary'],
            fg='white',
            relief=tk.FLAT,
            command=lambda: self.dismiss_notification(notif['id_produk'])
        ).pack(side=tk.RIGHT)
    
    def dismiss_notification(self, id_produk: str):
        """Menghapus notifikasi tertentu"""
        if self.controller.hapus_notifikasi(id_produk):
            self.show_notifications()
    
    def clear_notifications(self):
        """Menghapus semua notifikasi"""
        self.controller.notifikasi_list.clear()
        if hasattr(self, 'notif_window') and self.notif_window.winfo_exists():
            self.show_notifications()