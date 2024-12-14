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
        self.window.geometry("400x500")
        self.window.configure(bg=self.colors['background'])
        
        # Load data pesanan
        self.load_pesanan_data()
        
        # Inisialisasi komponen UI
        self.create_header()
        self.create_warning_section()
        self.create_detail_section()
        self.create_reason_section()
        self.create_confirmation_buttons()
        
        # Center window dan set modal
        self.window.transient(self.parent)
        self.window.grab_set()
        self.parent.wait_window(self.window)
        
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
            
        # Cek apakah pesanan masih bisa dibatalkan
        if self.pesanan.status != "Pending":
            messagebox.showerror(
                "Error",
                "Pesanan tidak dapat dibatalkan karena status sudah " + 
                self.pesanan.status.lower()
            )
            self.window.destroy()
            return
            
        # Ambil data produk terkait
        self.product = next(
            (p for p in self.db.get_all_produk() 
             if p['id_produk'] == self.pesanan.id_produk),
            None
        )
        
    def create_header(self):
        """Membuat bagian header"""
        header_frame = tk.Frame(
            self.window,
            bg=self.colors['error'],
            padx=20,
            pady=10
        )
        header_frame.pack(fill=tk.X)
        
        # Icon dan judul
        tk.Label(
            header_frame,
            text="⚠️",  # Warning emoji
            font=('Arial', 24),
            bg=self.colors['error'],
            fg='white'
        ).pack()
        
        tk.Label(
            header_frame,
            text="Pembatalan Pesanan",
            font=('Arial', 16, 'bold'),
            bg=self.colors['error'],
            fg='white'
        ).pack()
        
        tk.Label(
            header_frame,
            text=f"Pesanan #{self.pesanan_id}",
            font=('Arial', 10),
            bg=self.colors['error'],
            fg='white'
        ).pack()
        
    def create_warning_section(self):
        """Membuat bagian peringatan pembatalan"""
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
        ).pack()
        
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
        self.pesanan.tanggal_pesanan = datetime.fromisoformat(self.pesanan.tanggal_pesanan)
        # Data yang akan ditampilkan
        details = [
            ("ID Pesanan", self.pesanan_id),
            ("Tanggal", self.pesanan.tanggal_pesanan),
            ("Produk", self.product['nama_produk'] if self.product else "-"),
            ("Jumlah", self.pesanan.jumlah_dipesan),
            ("Total", f"Rp {self.pesanan.total_harga:,}")
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
            "Lainnya"
        ]
        
        self.reason_var = tk.StringVar()
        reason_cb = ttk.Combobox(
            reason_frame,
            textvariable=self.reason_var,
            values=reasons,
            width=30,
            state="readonly"
        )
        reason_cb.pack(fill=tk.X, pady=(0, 10))
        
        # Bind event perubahan alasan
        reason_cb.bind('<<ComboboxSelected>>', self.on_reason_change)
        
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
        
        # Tombol Konfirmasi
        self.confirm_button = tk.Button(
            button_frame,
            text="Konfirmasi Pembatalan",
            font=('Arial', 10, 'bold'),
            bg=self.colors['error'],
            fg='white',
            padx=20,
            pady=10,
            command=self.confirm_cancellation
        )
        self.confirm_button.pack(side=tk.RIGHT)
        
    def on_reason_change(self, event=None):
        """Handler untuk perubahan alasan pembatalan"""
        # Jika alasan "Lainnya" dipilih, fokus ke text area
        if self.reason_var.get() == "Lainnya":
            self.notes_text.focus()
        
    def confirm_cancellation(self):
        """Handler untuk konfirmasi pembatalan"""
        # Validasi input
        if not self.reason_var.get():
            messagebox.showwarning(
                "Peringatan",
                "Pilih alasan pembatalan"
            )
            return
            
        # Konfirmasi final
        if not messagebox.askyesno(
            "Konfirmasi Pembatalan",
            "Yakin ingin membatalkan pesanan ini?"
        ):
            return
            
        # Proses pembatalan
        try:
            # Catat alasan pembatalan
            reason = self.reason_var.get()
            if reason == "Lainnya" or self.notes_text.get("1.0", "end-1c").strip():
                reason += f"\nKeterangan: {self.notes_text.get('1.0', 'end-1c')}"
                
            # Batalkan pesanan
            success = self.controller.cancel_pesanan(self.pesanan_id)
            
            if success:
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

