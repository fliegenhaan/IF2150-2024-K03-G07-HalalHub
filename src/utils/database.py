import csv
import os
from typing import List, Dict, Optional
from datetime import datetime
import pandas as pd

DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

class CSVHandler:
    """Handler untuk operasi dasar CSV"""
    
    @staticmethod
    def read_csv(file_path: str) -> List[Dict]:
        """Membaca file CSV dan mengembalikan list of dictionaries"""
        if not os.path.exists(file_path):
            return []
            
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                return list(reader)
        except Exception as e:
            print(f"Error reading CSV file: {str(e)}")
            return []
    
    @staticmethod
    def write_csv(file_path: str, data: List[Dict], fieldnames: List[str]) -> bool:
        """Menulis data ke file CSV"""
        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            return True
        except Exception as e:
            print(f"Error writing to CSV file: {str(e)}")
            return False
    
    @staticmethod
    @staticmethod
    def append_csv(file_path: str, data: Dict, fieldnames: List[str]) -> bool:
        """Menambahkan satu baris data ke file CSV"""
        try:
            file_exists = os.path.exists(file_path)
            with open(file_path, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=',')  
                if not file_exists:
                    writer.writeheader()  # Tulis header jika file belum ada
                writer.writerow(data)  # Tulis data ke file
            return True
        except Exception as e:
            print(f"Error appending to CSV file: {str(e)}")
            return False


class DatabaseManager:
    """Manager untuk operasi database menggunakan CSV"""
    
    def __init__(self, base_path=None):
        """
        Initialize DatabaseManager dengan struktur file berikut:
        - produk.csv: Menyimpan data produk
        - pesanan.csv: Menyimpan data pesanan
        - transaksi.csv: Menyimpan data transaksi
        """
        self.base_path = base_path or DEFAULT_DB_PATH
        self.csv_handler = CSVHandler()
        
        os.makedirs(self.base_path, exist_ok=True)
        
        # Definisi struktur file CSV
        self.file_paths = {
            'produk': os.path.join(self.base_path, 'produk.csv'),
            'pesanan': os.path.join(self.base_path, 'pesanan.csv'),
            'transaksi': os.path.join(self.base_path, 'transaksi.csv')
        }
        
        # Definisi field untuk setiap CSV
        self.field_definitions = {
            'produk': [
                'id_produk', 
                'nama_produk', 
                'kategori',
                'harga', 
                'stok',
                'created_at',
                'updated_at'
            ],
            'pesanan': [
                'id_pesanan',
                'id_pelanggan',
                'id_produk',
                'jumlah_dipesan',
                'total_harga',
                'status',
                'tanggal_pesanan'
            ],
            'transaksi': [
                'id_transaksi',
                'id_pesanan',
                'total_harga',
                'metode_pembayaran',
                'tanggal_transaksi'
            ]
        }
        
        # Inisialisasi file CSV jika belum ada
        self._initialize_csv_files()
    
    def _initialize_csv_files(self) -> None:
        """Membuat file CSV jika belum ada"""
        os.makedirs(self.base_path, exist_ok=True)
        
        for file_type, file_path in self.file_paths.items():
            if not os.path.exists(file_path):
                self.csv_handler.write_csv(
                    file_path,
                    [],
                    self.field_definitions[file_type]
                )

    # Operasi Produk
    def get_all_produk(self) -> List[Dict]:
        """Mengambil semua data produk"""
        return self.csv_handler.read_csv(self.file_paths['produk'])

    def get_produk(self, id_produk: str) -> Optional[List[Dict]]:
        """Mengambil data produk berdasarkan ID"""
        products = self.get_all_produk()
        return [product for product in products if product['id_produk'] == id_produk]
    
    def add_produk(self, produk_data: Dict) -> bool:
        """Menambahkan produk baru"""
        try:
            # Validasi data
            required_fields = ['nama_produk', 'kategori', 'harga', 'stok']
            for field in required_fields:
                if not produk_data.get(field):
                    print(f"Missing required field: {field}")
                    return False

            # Pastikan file ada
            if not os.path.exists(self.file_paths['produk']):
                print("Database file not found")
                return False

            # Gunakan ID yang ada atau generate baru
            new_id = produk_data.get('id_produk') or f"PRD{datetime.now().strftime('%Y%m%d%H%M%S')}"
            now = datetime.now().isoformat()

            record = {
                'id_produk': new_id,
                'nama_produk': produk_data.get('nama_produk'),
                'kategori': produk_data.get('kategori'),
                'harga': float(produk_data.get('harga', 0)),
                'stok': int(produk_data.get('stok', 0)),
                'created_at': now,
                'updated_at': now
            }

            return self.csv_handler.append_csv(
                self.file_paths['produk'],
                record,
                self.field_definitions['produk']
            )

        except Exception as e:
            print(f"Error adding product: {str(e)}")
            return False

    def update_produk(self, id_produk: str, updated_data: Dict) -> bool:
        """Memperbarui data produk"""
        try:
            products = self.get_all_produk()
            updated = False
            now = datetime.now().isoformat()

            for product in products:
                if product['id_produk'] == id_produk:
                    # Only update fields that are in field_definitions
                    valid_fields = {
                        k: v for k, v in updated_data.items() 
                        if k in self.field_definitions['produk']
                    }

                    # Ensure all required fields exist
                    updated_product = {
                        'id_produk': product['id_produk'],
                        'nama_produk': valid_fields.get('nama_produk', product['nama_produk']),
                        'kategori': valid_fields.get('kategori', product['kategori']),
                        'harga': valid_fields.get('harga', product['harga']),
                        'stok': valid_fields.get('stok', product['stok']),
                        'created_at': product.get('created_at', now),
                        'updated_at': now
                    }

                    # Replace the old product data with updated data
                    products[products.index(product)] = updated_product
                    updated = True
                    break

            if updated:
                return self.csv_handler.write_csv(
                    self.file_paths['produk'],
                    products,
                    self.field_definitions['produk']
                )
            return False

        except Exception as e:
            print(f"Error updating product: {str(e)}")
            return False

    def delete_produk(self, id_produk: str) -> bool:
        """Menghapus produk"""
        products = self.get_all_produk()
        initial_length = len(products)
        products = [p for p in products if p['id_produk'] != id_produk]
        
        if len(products) < initial_length:
            return self.csv_handler.write_csv(
                self.file_paths['produk'],
                products,
                self.field_definitions['produk']
            )
        return False
    
    # Operasi Pesanan
    def get_all_pesanan(self) -> List[Dict]:
        """Mengambil semua data pesanan"""
        return self.csv_handler.read_csv(self.file_paths['pesanan'])
    
    def add_pesanan(self, pesanan_data: Dict) -> bool:
        """Menambahkan pesanan baru"""
        try:
            # Validasi data
            required_fields = ['id_pesanan', 'id_pelanggan', 'id_produk', 'jumlah_dipesan', 'total_harga', 'status', 'tanggal_pesanan']
            for field in required_fields:
                if field not in pesanan_data:
                    print(f"Missing required field: {field}")
                    return False
    
            # Pastikan file ada
            if not os.path.exists(self.file_paths['pesanan']):
                print("Database file not found")
                return False
    
            record = {
                'id_pesanan': pesanan_data['id_pesanan'],
                'id_pelanggan': pesanan_data['id_pelanggan'], 
                'id_produk': pesanan_data['id_produk'],
                'jumlah_dipesan': int(pesanan_data['jumlah_dipesan']),
                'total_harga': float(pesanan_data['total_harga']),
                'status': pesanan_data['status'],
                'tanggal_pesanan': pesanan_data['tanggal_pesanan']
            }
    
            return self.csv_handler.append_csv(
                self.file_paths['pesanan'],
                record,
                self.field_definitions['pesanan']
            )
            
        except Exception as e:
            print(f"Error adding order: {str(e)}")
            return False

        
    def update_pesanan_status(self, id_pesanan: str, status: str) -> bool:
        """Memperbarui status pesanan"""
        pesanan_list = self.get_all_pesanan()
        updated = False
        
        for pesanan in pesanan_list:
            if pesanan['id_pesanan'] == id_pesanan:
                pesanan['status'] = status
                updated = True
                break
                
        if updated:
            return self.csv_handler.write_csv(
                self.file_paths['pesanan'],
                pesanan_list,
                self.field_definitions['pesanan']
            )
        return False
    
    def update_pesanan(self, updated_data: Dict) -> bool:
        """Memperbarui data pesanan"""
        try:
            pesanan_list = self.get_all_pesanan()
            updated = False
            
            for pesanan in pesanan_list:
                if pesanan['id_pesanan'] == updated_data['id_pesanan']:
                    # Update data yang diperlukan
                    pesanan.update({
                        'id_pelanggan': updated_data.get('id_pelanggan', pesanan['id_pelanggan']),
                        'id_produk': updated_data.get('id_produk', pesanan['id_produk']),
                        'jumlah_dipesan': updated_data.get('jumlah_dipesan', pesanan['jumlah_dipesan']),
                        'total_harga': updated_data.get('total_harga', pesanan['total_harga']),
                        'status': updated_data.get('status', pesanan['status']),
                        'tanggal_pesanan': updated_data.get('tanggal_pesanan', pesanan['tanggal_pesanan'])
                    })
                    updated = True
                    break
                
            if updated:
                return self.csv_handler.write_csv(
                    self.file_paths['pesanan'],
                    pesanan_list,
                    self.field_definitions['pesanan']
                )
            return False
        
        except Exception as e:
            print(f"Error updating order: {str(e)}")
            return False
    
    # Operasi Transaksi
    def get_all_transaksi(self) -> List[Dict]:
        """Mengambil semua data transaksi"""
        return self.csv_handler.read_csv(self.file_paths['transaksi'])
    
    def add_transaksi(self, transaksi_data: Dict) -> bool:
        """Menambahkan transaksi baru"""
        return self.csv_handler.append_csv(
            self.file_paths['transaksi'],
            transaksi_data,
            self.field_definitions['transaksi']
        )
    
    # Laporan dan Analisis
    def generate_laporan_penjualan(self, start_date: datetime, end_date: datetime) -> Dict:
        """Membuat laporan penjualan untuk periode tertentu"""
        try:
            # Load all transactions, orders, and products
            transaksi_list = self.get_all_transaksi()
            pesanan_list = self.get_all_pesanan()
            produk_list = self.get_all_produk()

            if not transaksi_list:
                return {
                    'total_penjualan': 0,
                    'jumlah_transaksi': 0,
                    'transaksi_list': []
                }

            filtered_data = []
            total_penjualan = 0

            for transaksi in transaksi_list:
                try:
                    # Cari data pesanan terkait
                    pesanan = next(
                        (p for p in pesanan_list if p['id_pesanan'] == transaksi['id_pesanan']),
                        None
                    )

                    if pesanan:
                        # Cari data produk terkait
                        produk = next(
                            (p for p in produk_list if p['id_produk'] == pesanan['id_produk']),
                            None
                        )

                    tanggal = datetime.fromisoformat(transaksi['tanggal_transaksi'])

                    if start_date <= tanggal <= end_date:
                        data = {
                            'id_transaksi': transaksi['id_transaksi'],
                            'tanggal_transaksi': transaksi['tanggal_transaksi'],
                            'id_pelanggan': pesanan['id_pelanggan'] if pesanan else '-',
                            'nama_produk': produk['nama_produk'] if produk else '-',
                            'jumlah': pesanan['jumlah_dipesan'] if pesanan else 1,
                            'total_harga': float(transaksi['total_harga']),
                            'metode_pembayaran': transaksi.get('metode_pembayaran', 'Tunai')
                        }

                        filtered_data.append(data)
                        total_penjualan += float(transaksi['total_harga'])

                except (KeyError, ValueError) as e:
                    print(f"Error processing transaction: {str(e)}, Transaction ID: {transaksi.get('id_transaksi')}")
                    continue

            return {
                'total_penjualan': total_penjualan,
                'jumlah_transaksi': len(filtered_data),
                'transaksi_list': filtered_data
            }

        except Exception as e:
            print(f"Error generating sales report: {str(e)}")
            return {
                'total_penjualan': 0,
                'jumlah_transaksi': 0,
                'transaksi_list': []
            }
    
    def get_produk_terlaris(self, limit: int = 5) -> List[Dict]:
        """Mendapatkan daftar produk terlaris"""
        df_pesanan = pd.DataFrame(self.get_all_pesanan())
        if df_pesanan.empty:
            return []
            
        # Hitung total penjualan per produk
        produk_terlaris = df_pesanan.groupby('id_produk').agg({
            'jumlah_dipesan': 'sum'
        }).reset_index().sort_values('jumlah_dipesan', ascending=False)
        
        return produk_terlaris.head(limit).to_dict('records')

    def get_stok_menipis(self, batas_minimum: int = 10) -> List[Dict]:
        """Mendapatkan daftar produk dengan stok menipis"""
        df_produk = pd.DataFrame(self.get_all_produk())
        if df_produk.empty:
            return []
            
        # Filter produk dengan stok di bawah batas
        df_produk['stok'] = pd.to_numeric(df_produk['stok'])
        stok_menipis = df_produk[df_produk['stok'] <= batas_minimum]
        
        return stok_menipis.to_dict('records')