import tkinter as tk
from tkinter import ttk, messagebox
import re
from controllers.produk_controller import ProdukController
from datetime import datetime

class TambahProduk:
    def __init__(self, parent, colors, callback=None):
        """
        Inisialisasi window tambah produk
        
        Args:
            parent: Widget parent untuk window ini
            colors: Dictionary berisi kode warna untuk UI
            callback: Fungsi yang dipanggil setelah sukses menambah
        """
        self.parent = parent
        self.colors = colors
        self.callback = callback
        self.controller = ProdukController()
        
        # Buat window baru
        self.window = tk.Toplevel(self.parent)
        self.window.title("Tambah Produk Baru")
        self.window.geometry("500x600")
        self.window.configure(bg=self.colors['background'])
        
        # Inisialisasi komponen UI
        self.create_header()
        self.create_form()
        self.create_buttons()
        
        # Center window dan set modal
        self.window.transient(self.parent)
        self.window.grab_set()
        self.parent.wait_window(self.window)
        
    def create_header(self):
        """Membuat bagian header form"""
        header_frame = tk.Frame(
            self.window,
            bg=self.colors['primary'],
            padx=20,
            pady=10
        )
        header_frame.pack(fill=tk.X)
        
        # Judul form
        tk.Label(
            header_frame,
            text="Tambah Produk Baru",
            font=('Arial', 18, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        ).pack(side=tk.LEFT)
        
        # Auto-generated ID produk
        id_produk = f"PRD{datetime.now().strftime('%Y%m%d%H%M%S')}"
        tk.Label(
            header_frame,
            text=f"ID: {id_produk}",
            font=('Arial', 10),
            bg=self.colors['primary'],
            fg='white'
        ).pack(side=tk.RIGHT)
        
        self.id_produk = id_produk

    def create_form(self):
        """Membuat form input data produk"""
        form_frame = tk.LabelFrame(
            self.window,
            text="Data Produk",
            font=('Arial', 10, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['text'],
            padx=20,
            pady=10
        )
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Nama Produk
        tk.Label(
            form_frame,
            text="Nama Produk:",
            font=('Arial', 10),
            bg=self.colors['background'],
            fg=self.colors['text']
        ).pack(anchor='w', pady=(0, 5))
        
        self.nama_var = tk.StringVar()
        ttk.Entry(
            form_frame,
            textvariable=self.nama_var,
            width=50
        ).pack(fill=tk.X, pady=(0, 10))
        
        # Kategori
        tk.Label(
            form_frame,
            text="Kategori:",
            font=('Arial', 10),
            bg=self.colors['background'],
            fg=self.colors['text']
        ).pack(anchor='w', pady=(0, 5))
        
        categories = [
            "Pakaian Muslim Pria",
            "Pakaian Muslim Wanita",
            "Perlengkapan Ibadah",
            "Aksesoris Muslim"
        ]
        
        self.kategori_var = tk.StringVar()
        ttk.Combobox(
            form_frame,
            textvariable=self.kategori_var,
            values=categories,
            width=47,
            state="readonly"
        ).pack(fill=tk.X, pady=(0, 10))
        
        # Harga
        tk.Label(
            form_frame,
            text="Harga (Rp):",
            font=('Arial', 10),
            bg=self.colors['background'],
            fg=self.colors['text']
        ).pack(anchor='w', pady=(0, 5))
        
        # Frame untuk input harga dengan label Rp
        harga_frame = tk.Frame(
            form_frame,
            bg=self.colors['background']
        )
        harga_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            harga_frame,
            text="Rp",
            font=('Arial', 10),
            bg=self.colors['background'],
            fg=self.colors['text']
        ).pack(side=tk.LEFT)
        
        self.harga_var = tk.StringVar()
        vcmd = (self.window.register(self.validate_number), '%P')
        ttk.Entry(
            harga_frame,
            textvariable=self.harga_var,
            width=47,
            validate='key',
            validatecommand=vcmd
        ).pack(side=tk.LEFT, padx=(5, 0))
        
        # Stok
        tk.Label(
            form_frame,
            text="Stok Awal:",
            font=('Arial', 10),
            bg=self.colors['background'],
            fg=self.colors['text']
        ).pack(anchor='w', pady=(0, 5))
        
        self.stok_var = tk.StringVar(value="0")
        vcmd = (self.window.register(self.validate_number), '%P')
        ttk.Spinbox(
            form_frame,
            from_=0,
            to=9999,
            textvariable=self.stok_var,
            width=10,
            validate='key',
            validatecommand=vcmd
        ).pack(anchor='w', pady=(0, 10))
        
        # Deskripsi
        tk.Label(
            form_frame,
            text="Deskripsi:",
            font=('Arial', 10),
            bg=self.colors['background'],
            fg=self.colors['text']
        ).pack(anchor='w', pady=(0, 5))
        
        self.deskripsi_text = tk.Text(
            form_frame,
            height=5,
            width=47,
            font=('Arial', 10)
        )
        self.deskripsi_text.pack(fill=tk.X, pady=(0, 10))

    def create_buttons(self):
        """Membuat tombol-tombol aksi"""
        button_frame = tk.Frame(
            self.window,
            bg=self.colors['background']
        )
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Tombol Batal
        tk.Button(
            button_frame,
            text="Batal",
            font=('Arial', 10),
            bg=self.colors['error'],
            fg='white',
            padx=20,
            pady=10,
            command=self.window.destroy
        ).pack(side=tk.RIGHT, padx=5)
        
        # Tombol Simpan
        tk.Button(
            button_frame,
            text="Simpan",
            font=('Arial', 10, 'bold'),
            bg=self.colors['success'],
            fg='white',
            padx=20,
            pady=10,
            command=self.save_product
        ).pack(side=tk.RIGHT)

    def validate_number(self, value):
        """Validasi input angka"""
        if not value:
            return True
        return bool(re.match(r'^\d*$', value))

    def validate_form(self):
        """Validasi semua input form"""
        if not self.nama_var.get().strip():
            messagebox.showwarning(
                "Peringatan",
                "Nama produk harus diisi"
            )
            return False
            
        if not self.kategori_var.get():
            messagebox.showwarning(
                "Peringatan",
                "Pilih kategori produk"
            )
            return False
            
        if not self.harga_var.get():
            messagebox.showwarning(
                "Peringatan",
                "Harga produk harus diisi"
            )
            return False
            
        try:
            harga = float(self.harga_var.get())
            if harga <= 0:
                messagebox.showwarning(
                    "Peringatan",
                    "Harga produk harus lebih dari 0"
                )
                return False
        except ValueError:
            messagebox.showwarning(
                "Peringatan",
                "Harga tidak valid"
            )
            return False
            
        try:
            stok = int(self.stok_var.get())
            if stok < 0:
                messagebox.showwarning(
                    "Peringatan",
                    "Stok tidak boleh negatif"
                )
                return False
        except ValueError:
            messagebox.showwarning(
                "Peringatan",
                "Stok tidak valid"
            )
            return False
            
        return True

    def save_product(self):
        """Menyimpan data produk baru"""
        if not self.validate_form():
            return
            
        # Siapkan data produk
        product_data = {
            'id_produk': self.id_produk,
            'nama_produk': self.nama_var.get().strip(),
            'kategori': self.kategori_var.get(),
            'harga': float(self.harga_var.get()),
            'stok': int(self.stok_var.get()),
            'deskripsi': self.deskripsi_text.get("1.0", "end-1c").strip()
        }
        
        try:
            # Simpan produk menggunakan controller
            success = self.controller.tambah_produk(product_data)
            
            if success:
                messagebox.showinfo(
                    "Sukses",
                    "Produk berhasil ditambahkan"
                )
                if self.callback:
                    self.callback()
                self.window.destroy()
            else:
                messagebox.showerror(
                    "Error",
                    "Gagal menambahkan produk"
                )
                
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Terjadi kesalahan: {str(e)}"
            )
