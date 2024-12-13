from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class Laporan:
    """
    Model untuk laporan penjualan
    """
    total_penjualan_all_time: float = 0
    periode_awal: Optional[datetime] = None
    periode_akhir: Optional[datetime] = None
    
    def lihat_laporan_penjualan(self, pesanan_list: List[Dict]) -> dict:
        """Menampilkan laporan penjualan berdasarkan periode"""
        if not self.periode_awal or not self.periode_akhir:
            return {"error": "Periode laporan belum diatur"}
            
        total_penjualan = 0
        filtered_pesanan = []
        
        for pesanan in pesanan_list:
            tanggal_pesanan = pesanan.get("tanggal_pesanan")
            if (tanggal_pesanan >= self.periode_awal and 
                tanggal_pesanan <= self.periode_akhir and 
                pesanan.get("status") == "Selesai"):
                total_penjualan += pesanan.get("total_harga", 0)
                filtered_pesanan.append(pesanan)
                
        return {
            "periode_awal": self.periode_awal,
            "periode_akhir": self.periode_akhir,
            "total_penjualan": total_penjualan,
            "pesanan_list": filtered_pesanan
        }
