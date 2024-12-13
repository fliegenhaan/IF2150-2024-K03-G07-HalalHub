from dataclasses import dataclass
from typing import Optional

@dataclass
class Produk:
    """
    Model untuk manajemen produk
    """
    id_produk: str
    nama_produk: str
    kategori: str
    harga: float
    stok: int
    deskripsi: str = ""
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def input_id_produk(self, id_produk: str) -> None:
        """Memasukkan ID produk baru"""
        self.id_produk = id_produk
        
    def input_nama_produk(self, nama: str) -> None:
        """Memasukkan nama produk baru"""
        self.nama_produk = nama
        
    def input_harga(self, harga: float) -> None:
        """Memasukkan harga produk baru"""
        if harga < 0:
            raise ValueError("Harga tidak boleh negatif")
        self.harga = harga
        
    def input_stok(self, stok: int) -> None:
        """Memasukkan jumlah stok produk"""
        if stok < 0:
            raise ValueError("Stok tidak boleh negatif")
        self.stok = stok
        
    def update_id_produk(self, id_baru: str) -> None:
        """Memperbarui ID produk"""
        self.id_produk = id_baru
        
    def update_nama_produk(self, nama_baru: str) -> None:
        """Memperbarui nama produk"""
        self.nama_produk = nama_baru
        
    def update_harga(self, harga_baru: float) -> None:
        """Memperbarui harga produk"""
        if harga_baru < 0:
            raise ValueError("Harga tidak boleh negatif")
        self.harga = harga_baru
        
    def update_stok(self, stok_baru: int) -> None:
        """Memperbarui jumlah stok produk"""
        if stok_baru < 0:
            raise ValueError("Stok tidak boleh negatif")
        self.stok = stok_baru