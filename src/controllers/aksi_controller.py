from typing import List, Optional
from models.aksi import Aksi

class AksiController:
    """Controller untuk manajemen aksi sistem"""
    
    def __init__(self):
        self.aksi = Aksi(
            pilih_aksi="",
            daftar_aksi=[
                "Tambah Produk",
                "Edit Produk",
                "Hapus Produk",
                "Lihat Pesanan",
                "Input Pesanan",
                "Batalkan Pesanan",
                "Lihat Laporan",
                "Kelola Stok"
            ]
        )
        
    def tampilkan_menu_aksi(self) -> List[str]:
        """
        Menampilkan daftar aksi yang tersedia
        """
        return self.aksi.tampilkan_aksi()
        
    def pilih_aksi(self, aksi: str) -> Optional[str]:
        """
        Memilih aksi dari daftar yang tersedia
        """
        return self.aksi.pilih_aksi(aksi)
        
    def validasi_aksi(self, aksi: str) -> bool:
        """
        Memvalidasi apakah aksi tersedia
        """
        return aksi in self.aksi.daftar_aksi
        
    def get_aksi_kategori(self, kategori: str) -> List[str]:
        """
        Mendapatkan daftar aksi berdasarkan kategori
        """
        kategori_mapping = {
            "produk": ["Tambah Produk", "Edit Produk", "Hapus Produk"],
            "pesanan": ["Lihat Pesanan", "Input Pesanan", "Batalkan Pesanan"],
            "laporan": ["Lihat Laporan"],
            "stok": ["Kelola Stok"]
        }
        return kategori_mapping.get(kategori.lower(), [])