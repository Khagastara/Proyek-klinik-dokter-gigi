import psycopg2
import datetime
from tabulate import tabulate

def connect():
    return psycopg2.connect(
        database='Proyek klinik',
        user='postgres',
        password='082143',
        host='localhost',
        port=5432
        )

def add_pasien(nama):
    conn = connect()
    cur = conn.cursor()
    query_check =   """SELECT * FROM pasien
                    WHERE nama ilike %s"""
    cur.execute(query_check, (nama))
    existing_pasien = cur.fetchall()
    
    if existing_pasien:
        print(f"Pasien {nama} sudah ada di dalam data")
    else:
        while True:
            jenis_kelamin = ("Masukkan jenis kelamin pasien: (Laki-laki/Perempuan) ")
            if jenis_kelamin.lower() == 'laki-laki':
                jenis_kelamin = 'Laki-laki'
                break
            elif jenis_kelamin.lower() == 'perempuan':  
                jenis_kelamin = 'Perempuan'
                break
            else:
                print(f"Jenis kelamin {jenis_kelamin} invalid. Silahkan masukkan 'Laki-laki' atau 'Perempuan'")
        nomor_telepon = int(input("Masukkan nomor telepon Anda: "))
        alamat = input("Masukkan alamat Anda: ")
        query = """INSERT INTO pasien(nama, jenis_kelamin, nomor_telepon, alamat)
                VALUES(%s,%s,%s,%s)"""
        cur.execute(query, (nama, jenis_kelamin, nomor_telepon, alamat))
        conn.commit()
        read_pasien(nama)
        cur.close()
        conn.close()

def read_pasien(nama):
    conn = connect()
    cur = conn.cursor()
    query = """SELECT * FROM pasien
            WHERE nama ilike %s"""
    cur.execute(query, (nama))
    data = cur.fetchall()
    if data:
        col_names = [desc[0] for desc in cur.description]
        print(tabulate([data], headers=col_names, tablefmt="outline"))
    else:
        print(f"Tidak ada data yang telah ditemukan")
        
    cur.close()
    conn.close()
    
def read_rekam(nama):
    conn = connect()
    cur = conn.cursor()
    query = """SELECT p.nama, r.tanggal_pemeriksaan, r.diagnosis, r.hasil_pemeriksaan
            FROM pasien p
            JOIN rekam_medis r ON(p.id_pasien = r.id_pasien)
            WHERE p.nama ilike '%s'"""
    cur.execute(query, (nama))
    data = cur.fetchall()
    if data:
        col_names = [desc[0] for desc in cur.description]
        print(tabulate([data], headers=col_names, tablefmt="outline"))
    else:
        print("Tidak ada hasil rekam medis")
    cur.close()
    conn.close()
    
def read_pembayaran(nama):
    conn = connect()
    cur = conn.cursor()
    query = """SELECT pa.nama, pe.tanggal_pembayaran, re.daftar_obat, re.harga, m.metode_pembayaran, b.nama_bank
            FROM pasien pa
            JOIN detail_pembayaran d ON(pa.id_pasien = d.id_pasien)
            JOIN pembayaran pe ON(d.id_pembayaran = pe.id_pembayaran)
            JOIN resep_obat re ON(d.id_resep = re.id_resep)
            JOIN metode_pembayaran m ON(pe.id_metode = m.id_metode)
            JOIN bank b ON(pe.id_bank = b.id_bank)
            WHERE pa.nama ilike '%s'"""
    cur.execute(query, (nama))
    data = cur.fetchall()
    if data:
        col_names = [desc[0] for desc in cur.description]
        print(tabulate([data], headers=col_names, tablefmt="outline"))
    else:
        print("Tidak ada histori pembayaran")
    cur.close()
    conn.close()
    
def add_transaksi(nama):
    conn = connect()
    cur = conn.cursor()
    query_get_id_pasien = "SELECT id_pasien FROM pasien WHERE nama ILIKE %s"
    cur.execute(query_get_id_pasien, (nama))
    id_pasien = cur.fetchone()
    
    if not id_pasien:
        print(f"Pasien dengan nama '{nama}' tidak ditemukan.")
        cur.close()
        conn.close()
        return
    
    id_pasien = id_pasien[0]
    method = "SELECT * FROM metode_pembayaran"
    cur.execute(method)
    method_data = cur.fetchall()
    col_names = [desc[0] for desc in cur.description]
    print("Metode Pembayaran")
    print(tabulate([method_data], headers=col_names, tablefmt="outline")) 
    id_metode = int(input("Pilih id metode pembayaran: "))
    tanggal_pembayaran = datetime.date.today()
    while True:
        if id_metode == 1:
            bank = 1
            bank_method =   """INSERT INTO pembayaran(tanggal_pembayaran, id_metode, id_bank)
                            VALUES(%s,%s,%s)"""
            cur.execute(bank_method, (tanggal_pembayaran, id_metode, bank))
            conn.commit()
            break
        elif id_metode == 2:
            bank = 'BRI'
            bank_method =  """INSERT INTO pembayaran(tanggal_pembayaran, id_metode, id_bank)
                            VALUES(%s,%s,%s)"""
            cur.execute(bank_method, (tanggal_pembayaran, id_metode, bank))
            conn.commit()
            break
        elif id_metode == 3:
            bank = 'BCA'
            bank_method =  """INSERT INTO pembayaran(tanggal_pembayaran, id_metode, id_bank)
                            VALUES(%s,%s,%s)"""
            cur.execute(bank_method, (tanggal_pembayaran, id_metode, bank))
            conn.commit()
            break
        elif id_metode == 4:
            bank = 'BNI'
            bank_method =  """INSERT INTO pembayaran(tanggal_pembayaran, id_metode, id_bank)
                            VALUES(%s,%s,%s)"""
            cur.execute(bank_method, (tanggal_pembayaran, id_metode, bank))
            conn.commit()
            break
        elif id_metode == 5:
            bank = 'Mandiri'
            bank_method =  """INSERT INTO pembayaran(tanggal_pembayaran, id_metode, id_bank)
                            VALUES(%s,%s,%s)"""
            cur.execute(bank_method, (tanggal_pembayaran, id_metode, bank))
            conn.commit()
            break   
        elif id_metode == 6:
            bank = 'BSI'
            bank_method =   """INSERT INTO pembayaran(tanggal_pembayaran, id_metode, id_bank)
                            VALUES(%s,%s,%s)"""
            cur.execute(bank_method, (tanggal_pembayaran, id_metode, bank))
            conn.commit()
            break  
        else:
            print("Pilihan tidak ada")
    id_pembayaran = cur.fetchone()[0]
    resep_obat = "SELECT id_resep, daftar_obat, jumlah_obat, harga FROM resep_obat"
    cur.execute(resep_obat)
    resep_data = cur.fetchall()
    col_names = [desc[0] for desc in cur.description]
    print("Resep Obat:")
    print(tabulate([resep_data], headers=col_names, tablefmt="outline")) 
    total_input = int(input(f"Mau membeli berapa jenis obat?: "))
    for i in range(total_input):
        print(tabulate([resep_data], headers=col_names, tablefmt="outline")) 
        id_resep = int(input(f"Masukkan id resep yang ingin dibeli: "))
        beli_resep =    """INSERT INTO pembayaran(id_pasien, id_resep, id_pembayaran)
                        VALUES(%s,%s,%s)"""
        cur.execute(beli_resep, (id_pasien, id_resep, id_pembayaran))
        print(f"Transaksi untuk resep ID {id_resep} berhasil ditambahkan.")
    konfirmasi = input("Apakah Anda yakin ingin menyimpan transaksi ini? (yes/no): ")
    if konfirmasi.lower() == 'yes':
        conn.commit()
        print("Pembayaran berhasil ditambahkan.")
        query_latest = """SELECT pa.nama, pe.tanggal_pembayaran, re.daftar_obat, re.harga, m.metode_pembayaran, b.nama_bank
                                  FROM pasien pa
                                  JOIN detail_pembayaran d ON(pa.id_pasien = d.id_pasien)
                                  JOIN pembayaran pe ON(d.id_pembayaran = pe.id_pembayaran)
                                  JOIN resep_obat re ON(d.id_resep = re.id_resep)
                                  JOIN metode_pembayaran m ON(pe.id_metode = m.id_metode)
                                  JOIN bank b ON(pe.id_bank = b.id_bank)
                                  WHERE pa.id_pasien = %s
                                  ORDER BY pe.tanggal_pembayaran DESC
                                  LIMIT 1"""
        cur.execute(query_latest, (id_pasien))
        latest_payment = cur.fetchone()
        if latest_payment:
            print("\nDetail Pembayaran Terbaru:")
            col_names = [desc[0] for desc in cur.description]
            print(tabulate([latest_payment], headers=col_names, tablefmt="outline"))
    else:
        conn.rollback()
        print("Transaksi dibatalkan.")

    cur.close()
    conn.close()
    
def menuPasien():
    while True:
        nama = input("Masukkan nama pasien: ")
        print(f"Selamat datang pasien {nama}")
        print("\nMenu:")
        print("1. Konfirmasi Data Pasien (Anda)")
        print("2. Melihat Data Pasien (Anda)")
        print("3. Melihat Data Rekam Medis Anda")
        print("4. Histori Pembayaran")
        print("5. Membayar Transaksi")
        print("6. Logout")
        pilihan = int(input("Masukkan pilihan: "))
        
        if pilihan == 1:
            add_pasien()
        elif pilihan == 2:
            read_pasien()
        elif pilihan == 3:
            read_rekam()
        elif pilihan == 4:
            read_pembayaran()
        elif pilihan == 5:
            add_transaksi()
        elif pilihan == 6:
            print("Logout dari program")
            break
        else:
            print("Pilihan invalid")

if __name__ == "__main__":
    menuPasien()