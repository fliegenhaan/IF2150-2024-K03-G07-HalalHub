import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from controllers.pesanan_controller import PesananController
from utils.database import DatabaseManager

class PembatalanPesanan:
    def __init__(self, parent, colors, pesanan_id, callback=None):
        """
        Inisialisasi window pembatalan pesanan
        
        Args:
            parent: Widget parent untuk window ini
            colors: Dictionary berisi kode warna untuk UI
            pesanan_id: ID pesanan yang akan dibatalkan
            callback: Fungsi yang dipanggil setelah pembatalan berhasil
        """
        self.parent = parent
        self.colors = colors
        self.pesanan_id = pesanan_id
        self.callback = callback
        self.controller = PesananController()
        self.db = DatabaseManager()
        
        # Buat window baru
        self.window = tk.Toplevel(self.parent)
        self.window.title("Pembatalan Pesanan")
        self.window.geometry("400x600")
        self.window.configure(bg=self.colors['background'])
        
        # Load data pesanan
        self.load_pesanan_data()
        
        if not hasattr(self, 'pesanan') or self.pesanan is None:
            self.window.destroy()
            return

        # Inisialisasi komponen UI
        self.init_ui()
        
        # Center window dan set modal
        self.window.transient(self.parent)
        self.window.grab_set()

    def init_ui(self):
        """Inisialisasi semua komponen UI"""
        self.create_header()
        self.create_warning_section()
        self.create_detail_section()
        self.create_reason_section()
        self.create_confirmation_buttons()

    def create_header(self):
        """Membuat bagian header"""
        header_frame = tk.Frame(
            self.window,
            bg=self.colors['error'],
            padx=20,
            pady=15
        )
        header_frame.pack(fill=tk.X)
        
        # Icon dan judul
        tk.Label(
            header_frame,
            text="⚠️",
            font=('Arial', 24),
            bg=self.colors['error'],
            fg='white'
        ).pack(pady=(0, 5))
        
        tk.Label(
            header_frame,
            text="Pembatalan Pesanan",
            font=('Arial', 16, 'bold'),
            bg=self.colors['error'],
            fg='white'
        ).pack(pady=(0, 5))
        
        tk.Label(
            header_frame,
            text=f"Pesanan #{self.pesanan_id}",
            font=('Arial', 10),
            bg=self.colors['error'],
            fg='white'
        ).pack()

    def create_warning_section(self):
        """Membuat bagian peringatan"""
        warning_frame = tk.Frame(
            self.window,
            bg=self.colors['background'],
            padx=20,
            pady=10
        )
        warning_frame.pack(fill=tk.X)
        
        warning_text = (
            "Perhatian!\n\n"
            "• Pesanan yang sudah dibatalkan tidak dapat dikembalikan\n"
            "• Stok produk akan dikembalikan ke inventori\n"
            "• Harap pastikan pembatalan sudah sesuai"
        )
        
        tk.Label(
            warning_frame,
            text=warning_text,
            font=('Arial', 10),
            bg=self.colors['background'],
            fg=self.colors['error'],
            justify=tk.LEFT,
            wraplength=350
        ).pack(pady=10)

    def create_detail_section(self):
        """Membuat bagian detail pesanan"""
        detail_frame = tk.LabelFrame(
            self.window,
            text="Detail Pesanan",
            font=('Arial', 10, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['text'],
            padx=20,
            pady=10
        )
        detail_frame.pack(fill=tk.X, padx=20, pady=10)

        # Format tanggal pesanan
        try:
            tanggal = datetime.fromisoformat(self.pesanan.tanggal_pesanan)
            tanggal_str = tanggal.strftime("%d/%m/%Y %H:%M")
        except:
            tanggal_str = str(self.pesanan.tanggal_pesanan)

        # Data pesanan yang akan ditampilkan
        details = [
            ("ID Pesanan", self.pesanan_id),
            ("Tanggal", tanggal_str),
            ("Produk", self.product['nama_produk'] if self.product else "-"),
            ("Jumlah", self.pesanan.jumlah_dipesan),
            ("Total", f"Rp {float(self.pesanan.total_harga):,.2f}")
        ]
        
        for label, value in details:
            container = tk.Frame(
                detail_frame,
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

    def create_reason_section(self):
        """Membuat bagian alasan pembatalan"""
        reason_frame = tk.LabelFrame(
            self.window,
            text="Alasan Pembatalan",
            font=('Arial', 10, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['text'],
            padx=20,
            pady=10
        )
        reason_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Dropdown alasan pembatalan
        tk.Label(
            reason_frame,
            text="Pilih alasan:",
            font=('Arial', 10),
            bg=self.colors['background'],
            fg=self.colors['text']
        ).pack(anchor='w')
        
        reasons = [
            "Permintaan pelanggan",
            "Stok tidak tersedia", 
            "Kesalahan input pesanan",
            "Pesanan duplikat",
            "Pembatalan sistem",
            "Lainnya"
        ]
        
        self.reason_var = tk.StringVar()
        self.reason_cb = ttk.Combobox(
            reason_frame,
            textvariable=self.reason_var,
            values=reasons,
            width=30
        )
        self.reason_cb.pack(fill=tk.X, pady=(0, 10))
        
        # Text area untuk keterangan tambahan
        tk.Label(
            reason_frame,
            text="Keterangan tambahan:",
            font=('Arial', 10),
            bg=self.colors['background'],
            fg=self.colors['text']
        ).pack(anchor='w')
        
        self.notes_text = tk.Text(
            reason_frame,
            height=4,
            width=30,
            font=('Arial', 10)
        )
        self.notes_text.pack(fill=tk.X)

    def create_confirmation_buttons(self):
        """Membuat tombol-tombol konfirmasi"""
        button_frame = tk.Frame(
            self.window,
            bg=self.colors['background']
        )
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Tombol Batal
        tk.Button(
            button_frame,
            text="Kembali",
            font=('Arial', 10),
            bg=self.colors['secondary'],
            fg='white',
            padx=20,
            pady=10,
            command=self.window.destroy
        ).pack(side=tk.RIGHT, padx=5)
        
        # Tombol Konfirmasi Pembatalan
        tk.Button(
            button_frame,
            text="Konfirmasi Pembatalan",
            font=('Arial', 10, 'bold'),
            bg=self.colors['error'],
            fg='white',
            padx=20,
            pady=10,
            command=self.confirm_cancellation
        ).pack(side=tk.RIGHT)

    def load_pesanan_data(self):
        """Memuat data pesanan yang akan dibatalkan"""
        try:
            # Load pesanan
            self.pesanan = self.controller.get_pesanan(self.pesanan_id)
            if not self.pesanan:
                messagebox.showerror(
                    "Error",
                    "Data pesanan tidak ditemukan"
                )
                return
                
            # Cek status pesanan
            if self.pesanan.status != "Pending":
                messagebox.showerror(
                    "Error",
                    f"Pesanan tidak dapat dibatalkan karena status sudah {self.pesanan.status.lower()}"
                )
                return
                
            # Load data produk terkait
            self.product = next(
                (p for p in self.db.get_all_produk() 
                 if p['id_produk'] == self.pesanan.id_produk),
                None
            )
            
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Gagal memuat data pesanan: {str(e)}"
            )
            return

    def confirm_cancellation(self):
        """Handler untuk konfirmasi pembatalan"""
        if not self.reason_var.get():
            messagebox.showwarning(
                "Peringatan",
                "Pilih alasan pembatalan"  
            )
            return
            
        if not messagebox.askyesno(
            "Konfirmasi Pembatalan",
            "Yakin ingin membatalkan pesanan ini?"
        ):
            return
            
        try:
            # Get reason and notes
            reason = self.reason_var.get()
            notes = self.notes_text.get("1.0", "end-1c").strip()
            
            if notes:
                reason += f"\nKeterangan: {notes}"
                
            # Process cancellation
            if self.controller.cancel_pesanan(self.pesanan_id):
                messagebox.showinfo(
                    "Sukses",
                    "Pesanan berhasil dibatalkan"
                )
                if self.callback:
                    self.callback()
                self.window.destroy()
            else:
                messagebox.showerror(
                    "Error", 
                    "Gagal membatalkan pesanan"
                )
                
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Terjadi kesalahan: {str(e)}"
            )