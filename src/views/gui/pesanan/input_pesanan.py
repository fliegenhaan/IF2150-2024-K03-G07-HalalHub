import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from controllers.pesanan_controller import PesananController
from models.produk import Produk
from utils.database import DatabaseManager

class InputPesanan:
    def __init__(self, parent, colors, pesanan_id=None, callback=None):
        """
        Inisialisasi form input pesanan
        
        Args:
            parent: Widget parent untuk window ini
            colors: Dictionary berisi kode warna untuk UI
            pesanan_id: ID pesanan jika mode edit
            callback: Fungsi yang dipanggil setelah simpan/update
        """
        # Inisialisasi properti dasar
        self.parent = parent
        self.colors = colors
        self.pesanan_id = pesanan_id
        self.callback = callback
        self.controller = PesananController()
        self.db = DatabaseManager()
        
        # Buat window baru
        self.window = tk.Toplevel(self.parent)
        self.window.title("Edit Pesanan" if pesanan_id else "Input Pesanan Baru")
        self.window.geometry("600x700")
        self.window.configure(bg=self.colors['background'])
        
        # Inisialisasi komponen UI
        self.create_header()
        self.create_form()
        self.create_product_preview()
        self.create_summary()
        self.create_buttons()
        
        # Load data jika mode edit
        if pesanan_id:
            self.load_pesanan_data()
        
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
            text="Edit Pesanan" if self.pesanan_id else "Input Pesanan Baru",
            font=('Arial', 18, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        ).pack(side=tk.LEFT)
        
        # Tanggal dan waktu
        tk.Label(
            header_frame,
            text=datetime.now().strftime("%d %B %Y %H:%M"),
            font=('Arial', 10),
            bg=self.colors['primary'],
            fg='white'
        ).pack(side=tk.RIGHT)

    def create_form_field(self, parent, label, variable, disabled=False):
        """Membuat field form dengan label dan input"""
        container = tk.Frame(parent, bg=self.colors['background'])
        container.pack(fill=tk.X, pady=5)
        
        # Label field
        tk.Label(
            container,
            text=label,
            font=('Arial', 10),
            bg=self.colors['background'],
            fg=self.colors['text']
        ).pack(anchor='w')
        
        # Input field
        entry = ttk.Entry(
            container,
            textvariable=variable,
            state='disabled' if disabled else 'normal'
        )
        entry.pack(fill=tk.X)
        
        return entry

    def create_form(self):
        """Membuat form input data pesanan"""
        form_frame = tk.LabelFrame(
            self.window,
            text="Data Pesanan",
            font=('Arial', 10, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['text'],
            padx=20,
            pady=10
        )
        form_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # ID Pesanan (Auto-generated atau existing)
        self.id_pesanan = tk.StringVar(
            value=self.pesanan_id or f"PSN{datetime.now().strftime('%Y%m%d%H%M%S')}"
        )
        self.create_form_field(form_frame, "ID Pesanan:", self.id_pesanan, disabled=True)
        
        # ID Pelanggan
        self.id_pelanggan = tk.StringVar()
        self.create_form_field(form_frame, "ID Pelanggan:", self.id_pelanggan)
        
        # Pilihan Produk
        tk.Label(
            form_frame,
            text="Pilih Produk:",
            font=('Arial', 10),
            bg=self.colors['background'],
            fg=self.colors['text']
        ).pack(anchor='w', pady=(10, 0))
        
        # Ambil daftar produk dari database
        self.products = self.db.get_all_produk()
        product_names = [
            f"{p['nama_produk']} (Stok: {p['stok']})" 
            for p in self.products
        ]
        
        # Combobox produk
        self.product_var = tk.StringVar()
        self.product_cb = ttk.Combobox(
            form_frame,
            textvariable=self.product_var,
            values=product_names,
            width=40,
            state="readonly"
        )
        self.product_cb.pack(fill=tk.X, pady=(0, 10))
        
        # Bind event perubahan produk
        self.product_cb.bind('<<ComboboxSelected>>', self.on_product_select)
        
        # Jumlah pesanan
        tk.Label(
            form_frame,
            text="Jumlah:",
            font=('Arial', 10),
            bg=self.colors['background'],
            fg=self.colors['text']
        ).pack(anchor='w')
        
        # Spinbox untuk jumlah dengan validasi
        vcmd = (self.window.register(self.validate_quantity), '%P')
        self.quantity_var = tk.StringVar(value="1")
        self.quantity_spinbox = ttk.Spinbox(
            form_frame,
            from_=1,
            to=9999,
            textvariable=self.quantity_var,
            validate='all',
            validatecommand=vcmd,
            width=10
        )
        self.quantity_spinbox.pack(anchor='w')
        
        # Bind event perubahan jumlah
        self.quantity_var.trace_add('write', self.update_summary)

    def create_product_preview(self):
        """Membuat preview produk yang dipilih"""
        preview_frame = tk.LabelFrame(
            self.window,
            text="Detail Produk",
            font=('Arial', 10, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['text'],
            padx=20,
            pady=10
        )
        preview_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Informasi produk
        self.preview_labels = {
            'Nama': tk.StringVar(value="-"),
            'Kategori': tk.StringVar(value="-"),
            'Harga': tk.StringVar(value="-"),
            'Stok': tk.StringVar(value="-")
        }
        
        for label, var in self.preview_labels.items():
            container = tk.Frame(
                preview_frame,
                bg=self.colors['background']
            )
            container.pack(fill=tk.X, pady=2)
            
            tk.Label(
                container,
                text=f"{label}:",
                font=('Arial', 10),
                width=10,
                anchor='w',
                bg=self.colors['background'],
                fg=self.colors['text']
            ).pack(side=tk.LEFT)
            
            tk.Label(
                container,
                textvariable=var,
                font=('Arial', 10),
                bg=self.colors['background'],
                fg=self.colors['primary']
            ).pack(side=tk.LEFT, padx=5)

    def create_summary(self):
        """Membuat ringkasan pesanan"""
        summary_frame = tk.LabelFrame(
            self.window,
            text="Ringkasan Pesanan",
            font=('Arial', 10, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['text'],
            padx=20,
            pady=10
        )
        summary_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Total harga
        self.total_var = tk.StringVar(value="Rp 0")
        total_container = tk.Frame(
            summary_frame,
            bg=self.colors['background']
        )
        total_container.pack(fill=tk.X, pady=5)
        
        tk.Label(
            total_container,
            text="Total:",
            font=('Arial', 12, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['text']
        ).pack(side=tk.LEFT)
        
        tk.Label(
            total_container,
            textvariable=self.total_var,
            font=('Arial', 12, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['success']
        ).pack(side=tk.RIGHT)

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
            command=self.save_order
        ).pack(side=tk.RIGHT)

    def validate_quantity(self, value):
        """Validasi input jumlah pesanan"""
        if not value:
            return True
            
        try:
            quantity = int(value)
            if quantity > 0:
                selected_product = self.get_selected_product()
                if selected_product and quantity <= int(selected_product['stok']):
                    return True
        except ValueError:
            pass
            
        return False

    def on_product_select(self, event=None):
        """Handler saat produk dipilih"""
        product = self.get_selected_product()
        if not product:
            return
            
        # Update preview produk
        self.preview_labels['Nama'].set(product['nama_produk'])
        self.preview_labels['Kategori'].set(product['kategori'])
        self.preview_labels['Harga'].set(f"Rp {float(product['harga']):,}")
        self.preview_labels['Stok'].set(product['stok'])
        
        # Reset dan update jumlah
        self.quantity_var.set("1")
        self.update_summary()

    def get_selected_product(self):
        """Mendapatkan data produk yang dipilih"""
        selection = self.product_var.get()
        if not selection:
            return None
            
        product_name = selection.split(" (Stok:")[0]
        return next(
            (p for p in self.products if p['nama_produk'] == product_name),
            None
        )

    def update_summary(self, *args):
        """Memperbarui ringkasan pesanan"""
        product = self.get_selected_product()
        if not product:
            self.total_var.set("Rp 0")
            return
            
        try:
            quantity = int(self.quantity_var.get())
            total = quantity * float(product['harga'])
            self.total_var.set(f"Rp {total:,}")
        except ValueError:
            self.total_var.set("Rp 0")

    def load_pesanan_data(self):
        """Memuat data pesanan untuk mode edit"""
        # TODO: Implement loading pesanan data from database
        pesanan = self.controller.get_pesanan(self.pesanan_id)
        if not pesanan:
            messagebox.showerror(
                "Error",
                "Data pesanan tidak ditemukan"
            )
            self.window.destroy()
            return
            
        # Set form values
        self.id_pelanggan.set(pesanan.id_pelanggan)
        
        # Set produk
        product = next(
            (p for p in self.products if p['id_produk'] == pesanan.id_produk),
            None
        )
        if product:
            self.product_var.set(
                f"{product['nama_produk']} (Stok: {product['stok']})"
            )
            self.on_product_select()
            
        # Set jumlah
        self.quantity_var.set(str(pesanan.jumlah_dipesan))

    def save_order(self):
        """Menyimpan atau memperbarui pesanan"""
        # Validasi input
        if not self.id_pelanggan.get().strip():
            messagebox.showwarning(
                "Peringatan",
                "ID Pelanggan harus diisi"
            )
            return
            
        product = self.get_selected_product()
        if not product:
            messagebox.showwarning(
                "Peringatan",
                "Pilih produk terlebih dahulu"
            )
            return
            
        try:
            quantity = int(self.quantity_var.get())
        except ValueError:
            messagebox.showwarning(
                "Peringatan",
                "Jumlah pesanan tidak valid"
            )
            return
            
        # Siapkan data pesanan
        pesanan_data = {
            'id_pesanan': self.id_pesanan.get(),
            'id_pelanggan': self.id_pelanggan.get(),
            'id_produk': product['id_produk'],
            'jumlah_dipesan': quantity,
            'total_harga': float(product['harga']) * quantity
        }
        
        try:
            # Simpan atau update pesanan
            if self.pesanan_id:
                success = self.controller.update_pesanan(pesanan_data)
                message = "Pesanan berhasil diperbarui"
            else:
                success = self.controller.buat_pesanan(pesanan_data, Produk(**product))
                message = "Pesanan berhasil disimpan"
                
            if success:
                messagebox.showinfo("Sukses", message)
                if self.callback:
                    self.callback()
                self.window.destroy()
            else:
                messagebox.showerror(
                    "Error",
                    "Gagal menyimpan pesanan"
                )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Terjadi kesalahan: {str(e)}"
            )
