import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from controllers.pesanan_controller import PesananController
from utils.database import DatabaseManager

class DetailPesanan:
    def __init__(self, parent, colors, pesanan_id, callback=None):
        self.parent = parent
        self.colors = colors
        self.pesanan_id = pesanan_id  
        self.callback = callback
        self.controller = PesananController()
        self.db = DatabaseManager()
        
        # Load pesanan data
        self.load_pesanan_data()
        if not hasattr(self, 'pesanan') or self.pesanan is None:
            return

        # Create window
        self.window = tk.Toplevel(self.parent)
        self.window.title(f"Detail Pesanan - {pesanan_id}")
        self.window.geometry("500x600")
        self.window.configure(bg=self.colors['background'])
        
        # Initialize UI
        self.setup_ui()
        
        self.window.transient(self.parent)
        self.window.grab_set()
        self.parent.wait_window(self.window)

    def setup_ui(self):
        """Setup semua elemen UI"""
        self.create_header()
        self.create_status_section()
        self.create_detail_section()
        self.create_product_section()
        self.create_history_section()
        self.create_action_buttons()

    def create_header(self):
        header_frame = tk.Frame(
            self.window,
            bg=self.colors['primary'],
            padx=20,
            pady=10
        )
        header_frame.pack(fill=tk.X)
        
        # Parse tanggal pesanan string to datetime
        try:
            tanggal = datetime.fromisoformat(self.pesanan.tanggal_pesanan)
            tanggal_str = tanggal.strftime("%d %B %Y %H:%M")
        except:
            tanggal_str = str(self.pesanan.tanggal_pesanan)

        tk.Label(
            header_frame,
            text=f"Pesanan #{self.pesanan_id}",
            font=('Arial', 16, 'bold'),
            bg=header_frame['bg'],
            fg='white'
        ).pack(side=tk.LEFT)

        tk.Label(
            header_frame,
            text=tanggal_str,
            font=('Arial', 10),
            bg=header_frame['bg'],
            fg='white'
        ).pack(side=tk.RIGHT)
        
    def load_pesanan_data(self):
        """Memuat data pesanan dari database"""
        # Ambil data pesanan
        self.pesanan = self.controller.get_pesanan(self.pesanan_id)
        if not self.pesanan:
            messagebox.showerror(
                "Error",
                "Data pesanan tidak ditemukan"
            )
            self.window.destroy()
            return
            
        # Ambil data produk terkait
        self.product = next(
            (p for p in self.db.get_all_produk() 
             if p['id_produk'] == self.pesanan.id_produk),
            None
        )

    def create_status_section(self):
        """Membuat bagian status pesanan"""
        status_frame = tk.Frame(
            self.window,
            bg=self.colors['background'],
            padx=20,
            pady=10
        )
        status_frame.pack(fill=tk.X)
        
        # Status label dengan warna sesuai status
        status_colors = {
            'Pending': self.colors['warning'],
            'Selesai': self.colors['success'],
            'Dibatalkan': self.colors['error']
        }
        
        status_container = tk.Frame(
            status_frame,
            bg=status_colors.get(
                self.pesanan.status,
                self.colors['primary']
            ),
            padx=10,
            pady=5
        )
        status_container.pack(side=tk.LEFT)
        
        tk.Label(
            status_container,
            text=f"Status: {self.pesanan.status}",
            font=('Arial', 10, 'bold'),
            bg=status_container['bg'],
            fg='white'
        ).pack()
        
    def create_detail_section(self):
        """Membuat bagian detail pesanan"""
        details_frame = tk.LabelFrame(
            self.window,
            text="Detail Pesanan",
            font=('Arial', 10, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['text'],
            padx=20,
            pady=10
        )
        details_frame.pack(fill=tk.X, padx=20, pady=10)

        # Data yang akan ditampilkan
        details = [
            ("ID Pesanan", self.pesanan.id_pesanan),
            ("ID Pelanggan", self.pesanan.id_pelanggan),
            ("ID Produk", self.pesanan.id_produk),
            ("Jumlah", str(self.pesanan.jumlah_dipesan)),
            ("Total", f"Rp {float(self.pesanan.total_harga):,.2f}"),
            ("Status", self.pesanan.status)
        ]

        for label, value in details:
            container = tk.Frame(
                details_frame,
                bg=self.colors['background']
            )
            container.pack(fill=tk.X, pady=2)

            tk.Label(
                container,
                text=f"{label}:",
                font=('Arial', 10),
                width=15,
                anchor='w',
                bg=self.colors['background'],
                fg=self.colors['text']
            ).pack(side=tk.LEFT)

            tk.Label(
                container,
                text=str(value),
                font=('Arial', 10),
                bg=self.colors['background'],
                fg=self.colors['primary']
            ).pack(side=tk.LEFT, padx=5)
            
    def create_product_section(self):
        """Membuat bagian informasi produk"""
        if not self.product:
            return
            
        product_frame = tk.LabelFrame(
            self.window,
            text="Detail Produk",
            font=('Arial', 10, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['text'],
            padx=20,
            pady=10
        )
        product_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Data produk yang akan ditampilkan
        product_details = [
            ("Nama Produk", self.product['nama_produk']),
            ("Kategori", self.product['kategori']),
            ("Harga Satuan", f"Rp {float(self.product['harga']):,}"),
            ("Jumlah Pesanan", self.pesanan.jumlah_dipesan),
            ("Total", f"Rp {self.pesanan.total_harga:,}")
        ]
        
        for label, value in product_details:
            container = tk.Frame(
                product_frame,
                bg=self.colors['background']
            )
            container.pack(fill=tk.X, pady=2)
            
            tk.Label(
                container,
                text=f"{label}:",
                font=('Arial', 10),
                width=15,
                anchor='w',
                bg=self.colors['background'],
                fg=self.colors['text']
            ).pack(side=tk.LEFT)
            
            tk.Label(
                container,
                text=str(value),
                font=('Arial', 10),
                bg=self.colors['background'],
                fg=self.colors['primary']
            ).pack(side=tk.LEFT, padx=5)
            
    def create_history_section(self):
        """Membuat bagian riwayat perubahan status"""
        history_frame = tk.LabelFrame(
            self.window,
            text="Riwayat Status",
            font=('Arial', 10, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['text'],
            padx=20,
            pady=10
        )
        history_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Ambil riwayat status dari database
        history = [
            {
                'status': 'Pending',
                'timestamp': self.pesanan.tanggal_pesanan,
                'keterangan': 'Pesanan dibuat'
            }
        ]
        
        if self.pesanan.status in ['Selesai', 'Dibatalkan']:
            history.append({
                'status': self.pesanan.status,
                'timestamp': datetime.now(),  # Idealnya dari database
                'keterangan': f"Pesanan {self.pesanan.status.lower()}"
            })
        
        # Tampilkan setiap riwayat
        for item in history:
            container = tk.Frame(
                history_frame,
                bg=self.colors['background']
            )
            container.pack(fill=tk.X, pady=5)
            

            # Status dan timestamp
            tk.Label(
                container,
                text=item['timestamp'],
                font=('Arial', 9),
                bg=self.colors['background'],
                fg=self.colors['text']
            ).pack(side=tk.LEFT)
            
            tk.Label(
                container,
                text=f" - {item['status']}",
                font=('Arial', 9, 'bold'),
                bg=self.colors['background'],
                fg=self.colors['primary']
            ).pack(side=tk.LEFT)
            
            tk.Label(
                container,
                text=f" - {item['keterangan']}",
                font=('Arial', 9),
                bg=self.colors['background'],
                fg=self.colors['text']
            ).pack(side=tk.LEFT)
            
    def create_action_buttons(self):
        """Membuat tombol-tombol aksi"""
        button_frame = tk.Frame(
            self.window,
            bg=self.colors['background']
        )
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Tombol yang akan ditampilkan berdasarkan status
        if self.pesanan.status == "Pending":
            # Tombol Selesai
            tk.Button(
                button_frame,
                text="✅ Selesaikan Pesanan",
                font=('Arial', 10),
                bg=self.colors['success'],
                fg='white',
                padx=20,
                pady=10,
                command=self.complete_order
            ).pack(side=tk.LEFT, padx=5)
            
            # Tombol Batalkan
            tk.Button(
                button_frame,
                text="❌ Batalkan Pesanan",
                font=('Arial', 10),
                bg=self.colors['error'],
                fg='white',
                padx=20,
                pady=10,
                command=self.cancel_order
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
        
    def complete_order(self):
        """Handler untuk menyelesaikan pesanan"""
        if not messagebox.askyesno(
            "Konfirmasi",
            "Yakin ingin menyelesaikan pesanan ini?"
        ):
            return
            
        # Cek status pesanan saat ini
        if self.pesanan.status == "Selesai":
            messagebox.showerror(
                "Error",
                "Pesanan ini sudah selesai"
            )
            return
        elif self.pesanan.status == "Dibatalkan":
            messagebox.showerror(
                "Error",
                "Tidak dapat menyelesaikan pesanan yang sudah dibatalkan"
            )
            return
            
        try:
            # Proses penyelesaian pesanan
            success, message = self.controller.mark_as_done(self.pesanan_id)
            
            if success:
                messagebox.showinfo(
                    "Sukses", 
                    "Pesanan telah diselesaikan"
                )
                if self.callback:
                    self.callback()
                self.window.destroy()
            else:
                messagebox.showerror(
                    "Error",
                    message or "Gagal menyelesaikan pesanan"
                )
                
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Terjadi kesalahan: {str(e)}"
            )
                
    def cancel_order(self):
        """Handler untuk membatalkan pesanan"""
        if messagebox.askyesno(
            "Konfirmasi",
            "Yakin ingin membatalkan pesanan ini?"
        ):
            success = self.controller.cancel_pesanan(self.pesanan_id)
            if success:
                messagebox.showinfo(
                    "Sukses",
                    "Pesanan telah dibatalkan"
                )
                if self.callback:
                    self.callback()
                self.window.destroy()
            else:
                messagebox.showerror(
                    "Error",
                    "Gagal membatalkan pesanan"
                )
