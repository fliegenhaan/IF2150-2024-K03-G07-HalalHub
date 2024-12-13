from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Pesanan:
    """
    Model untuk manajemen pesanan
    """
    id_pesanan: str
    id_pelanggan: str
    id_produk: str
    jumlah_dipesan: int
    total_harga: float  # Tambahkan field total_harga
    status: str = "Pending"  # Pending/Selesai/Dibatalkan
    tanggal_pesanan: str = datetime.now().isoformat()  
    
    def get_pesanan(self) -> dict:
        """Mengambil data pesanan"""
        return {
            "id_pesanan": self.id_pesanan,
            "id_pelanggan": self.id_pelanggan,
            "id_produk": self.id_produk,
            "jumlah_dipesan": self.jumlah_dipesan,
            "total_harga": self.total_harga,
            "status": self.status,
            "tanggal_pesanan": self.tanggal_pesanan
        }
        
    def set_pesanan(self, data: dict) -> None:
        """Menambahkan data pesanan baru"""
        self.id_pesanan = data.get("id_pesanan", self.id_pesanan)
        self.id_pelanggan = data.get("id_pelanggan", self.id_pelanggan)
        self.id_produk = data.get("id_produk", self.id_produk) 
        self.jumlah_dipesan = data.get("jumlah_dipesan", self.jumlah_dipesan)
        self.total_harga = data.get("total_harga", self.total_harga)
        self.status = data.get("status", self.status)
        
    def cancel_pesanan(self) -> None:
        """Membatalkan pesanan"""
        if self.status == "Selesai":
            raise ValueError("Tidak dapat membatalkan pesanan yang sudah selesai")
        self.status = "Dibatalkan"
        
    def mark_as_done(self) -> None:
        """Menandai pesanan sebagai selesai"""
        if self.status == "Dibatalkan":
            raise ValueError("Tidak dapat menyelesaikan pesanan yang sudah dibatalkan")
        self.status = "Selesai"