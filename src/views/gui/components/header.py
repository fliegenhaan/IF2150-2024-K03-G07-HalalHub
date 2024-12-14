import tkinter as tk
from datetime import datetime
from ..components.notification import Notification

class Header:
    def __init__(self, parent, colors):
        """Inisialisasi komponen header"""
        self.parent = parent
        self.colors = colors
        
        # Buat frame header
        self.header_frame = tk.Frame(
            self.parent,
            bg=self.colors['primary'],
            height=60
        )
        self.header_frame.pack(fill=tk.X)
        self.header_frame.pack_propagate(False)
        
        self.create_title()
        self.create_datetime()
        self.create_notification_icon()
        
    def create_title(self):
        """Membuat judul aplikasi"""
        # Logo (emoji masjid) dan nama aplikasi
        title_frame = tk.Frame(
            self.header_frame,
            bg=self.colors['primary']
        )
        title_frame.pack(side=tk.LEFT, padx=20)
        
        logo_label = tk.Label(
            title_frame,
            text="🕌",  # Emoji masjid
            font=('Arial', 24),
            bg=self.colors['primary'],
            fg='white'
        )
        logo_label.pack(side=tk.LEFT, padx=(0, 10))
        
        title_label = tk.Label(
            title_frame,
            text="HalalHub",
            font=('Arial', 24, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        )
        title_label.pack(side=tk.LEFT)
        
    def create_datetime(self):
        """Membuat tampilan tanggal dan waktu"""
        self.datetime_frame = tk.Frame(
            self.header_frame,
            bg=self.colors['primary']
        )
        self.datetime_frame.pack(side=tk.RIGHT, padx=20)
        
        # Label tanggal
        self.date_label = tk.Label(
            self.datetime_frame,
            text=datetime.now().strftime("%d %B %Y"),
            font=('Arial', 12),
            bg=self.colors['primary'],
            fg='white'
        )
        self.date_label.pack(side=tk.TOP)
        
        # Label waktu
        self.time_label = tk.Label(
            self.datetime_frame,
            text="",
            font=('Arial', 12),
            bg=self.colors['primary'],
            fg='white'
        )
        self.time_label.pack(side=tk.TOP)
        
        # Mulai update waktu
        self.update_time()
        
    def create_notification_icon(self):
        """Membuat ikon notifikasi"""
        self.notification = Notification(self.header_frame, self.colors)
        notification_frame = tk.Frame(
            self.header_frame,
            bg=self.colors['primary']
        )
        notification_frame.pack(side=tk.RIGHT, padx=10)

        # Tombol notifikasi
        notification_button = tk.Button(
            notification_frame,
            text="🔔",  # Emoji lonceng
            font=('Arial', 16),
            bg=self.colors['primary'],
            fg='white',
            bd=0,
            command=self.notification.create_notification_window
        )
        notification_button.pack()

    def update_time(self):
        """Update waktu setiap detik"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.configure(text=current_time)
        self.parent.after(1000, self.update_time)
        
    def show_notifications(self):
        """Menampilkan daftar notifikasi"""
        # TODO: Implementasi popup notifikasi
        pass
        
    def update_notification_count(self, count):
        """Update jumlah notifikasi"""
        self.notification_count.set(str(count))
