import psycopg2
import datetime
import os
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
    os.system("cls")
    conn = connect()
    cur = conn.cursor()
    query_check =   """SELECT * FROM pasien
                    WHERE nama ilike %s"""
    cur.execute(query_check, (nama,))
    existing_pasien = cur.fetchall()
    
    if existing_pasien:
        print(f"Selamat Datang, {nama}!")
    else:
        print("Silahkan membuat data Pasien baru")
        jenis_kelamin = input("Masukkan jenis kelamin pasien: (Laki-laki/Perempuan) ")
        if jenis_kelamin.lower() == 'laki-laki':
            jenis_kelamin = 'Laki-laki'
        elif jenis_kelamin.lower() == 'perempuan':  
            jenis_kelamin = 'Perempuan'
        else:
            print(f"Jenis kelamin {jenis_kelamin} invalid. Silahkan masukkan 'Laki-laki' atau 'Perempuan'")
        nomor_telepon = int(input("Masukkan nomor telepon Anda: "))
        alamat = input("Masukkan alamat Anda: ")
        konfirmasi = input("Apakah Anda yakin ingin menambah pasien sesuai dengan yang diinginkan? (yes/no): ")
        
        if konfirmasi.lower() == 'yes':
            conn.commit()
            print("Data Pasien baru telah dimasukkan.")
            query = """INSERT INTO pasien(nama, jenis_kelamin, nomor_telepon, alamat)
                    VALUES(%s,%s,%s,%s)"""
            cur.execute(query, (nama, jenis_kelamin, nomor_telepon, alamat))
            conn.commit()
            os.system("cls")
            print("\nDetail Pembayaran Terbaru:")
            query_latest =  """SELECT * FROM pasien WHERE nama ILIKE %s
                            ORDER BY id_pasien DESC
                            LIMIT 1"""
            cur.execute(query_latest, (nama,))
            latest_pasien = cur.fetchone()
            
            if latest_pasien:
                print("\nDetail Pasien Terbaru:")
                col_names = [desc[0] for desc in cur.description]
                print(tabulate([latest_pasien], headers=col_names, tablefmt="outline"))
                
        else:
            os.system("cls")
            conn.rollback()
            print("Membuat data Pasien baru telah dibatalkan.")
            
        print(f"Selamat Datang, {nama}!")
        cur.close()
        conn.close()

def read_pasien(nama):
    os.system("cls")  # Clear the screen
    conn = connect()
    cur = conn.cursor()
    query = f"""SELECT * FROM pasien WHERE nama ILIKE '{nama}'"""
    cur.execute(query)
    data = cur.fetchall()
    
    if data:
        col_names = [desc[0] for desc in cur.description]
        print(tabulate(data, headers=col_names, tablefmt="outline"))
    else:
        print(f"Tidak ada data yang telah ditemukan untuk pasien bernama '{nama}'")
    
    cur.close()
    conn.close()
    
def read_rekam(nama):
    os.system("cls")
    conn = connect()
    cur = conn.cursor()
    query = f"""SELECT p.nama, r.tanggal_pemeriksaan, r.diagnosis, r.hasil_pemeriksaan
            FROM pasien p
            JOIN rekam_medis r ON(p.id_pasien = r.id_pasien)
            WHERE p.nama ilike '{nama}'"""
    cur.execute(query)
    data = cur.fetchall()
    if data:
        col_names = [desc[0] for desc in cur.description]
        print(tabulate(data, headers=col_names, tablefmt="outline"))
    else:
        print("Tidak ada hasil rekam medis")
    cur.close()
    conn.close()
    
def read_pembayaran(nama):
    os.system("cls")
    conn = connect()
    cur = conn.cursor()
    query = f"""SELECT pa.nama, pe.tanggal_pembayaran, re.daftar_obat, re.harga, m.metode_pembayaran, b.nama_bank
            FROM pasien pa
            JOIN detail_pembayaran d ON(pa.id_pasien = d.id_pasien)
            JOIN pembayaran pe ON(d.id_pembayaran = pe.id_pembayaran)
            JOIN resep_obat re ON(d.id_resep = re.id_resep)
            JOIN metode_pembayaran m ON(pe.id_metode = m.id_metode)
            JOIN bank b ON(pe.id_bank = b.id_bank)
            WHERE pa.nama ilike '{nama}'"""
    cur.execute(query)
    data = cur.fetchall()
    if data:
        col_names = [desc[0] for desc in cur.description]
        print(tabulate(data, headers=col_names, tablefmt="outline"))
    else:
        print("Tidak ada histori pembayaran")
    cur.close()
    conn.close()
    
def add_transaksi(nama):
    os.system("cls")
    conn = connect()
    cur = conn.cursor()
    query_get_id_pasien = f"SELECT id_pasien FROM pasien WHERE nama ILIKE '{nama}'"
    cur.execute(query_get_id_pasien)
    id_pasien = cur.fetchone()

    if not id_pasien:
        print(f"Pasien dengan nama '{nama}' tidak ditemukan.")
        cur.close()
        conn.close()
        return

    id_pasien = id_pasien[0]
    
    print("Pilih Resep Obat:")
    cur.execute("SELECT id_resep, daftar_obat, jumlah_obat, harga FROM resep_obat")
    resep_data = cur.fetchall()
    print(tabulate(resep_data, headers=["ID Resep", "Daftar Obat", "Jumlah", "Harga"], tablefmt="outline"))
    
    total_input = int(input("Masukkan jumlah jenis obat yang ingin dibeli: "))
    id_resep_list = []
    for _ in range(total_input):
        id_resep = int(input("Masukkan ID resep yang ingin dibeli: "))
        id_resep_list.append(id_resep)
        print(f"Transaksi untuk resep ID {id_resep} berhasil ditambahkan.")
        
    # Choose payment method
    print("Metode Pembayaran:")
    cur.execute("SELECT * FROM metode_pembayaran")
    method_data = cur.fetchall()
    col_names = [desc[0] for desc in cur.description]
    print(tabulate(method_data, headers=col_names, tablefmt="outline"))
    tanggal_pembayaran = datetime.date.today()
    
    while True:
        id_metode = int(input("Pilih ID metode pembayaran: "))
        if id_metode == 1:
            id_bank = 6  # non-Bank
            bank_method =   """INSERT INTO pembayaran(tanggal_pembayaran, id_metode, id_bank)
                                    VALUES(%s,%s,%s) RETURNING id_pembayaran"""
            cur.execute(bank_method, (tanggal_pembayaran, id_metode, id_bank))
            conn.commit() 
            break
        elif id_metode == 2:
            os.system("cls")
            bank =  """SELECT * FROM bank
                    WHERE id_bank < 6"""
            cur.execute(bank)
            bank_data = cur.fetchall()
            col_names = [desc[0] for desc in cur.description]
            print("Transaksi Bank")
            print(tabulate(bank_data, headers=col_names, tablefmt="outline"))
            while True:
                id_bank = int(input("Silahkan untuk memilih transfer bank: "))
                if 1 <= id_bank <= 5:
                    bank_method =   """INSERT INTO pembayaran(tanggal_pembayaran, id_metode, id_bank)
                                    VALUES(%s,%s,%s) RETURNING id_pembayaran"""
                    cur.execute(bank_method, (tanggal_pembayaran, id_metode, id_bank))
                    conn.commit()                    
                    break     
                else:
                    print("Pilihan tidak ada")
                    cur.close()
                    conn.close() 
            break
        else:
            print("Metode pembayaran tidak valid.")
            cur.close()
            conn.close()
            
    id_pembayaran = cur.fetchone()[0] 
    
    for id_resep in id_resep_list:
        detail_resep = "INSERT INTO detail_pembayaran(id_pasien, id_resep, id_pembayaran) VALUES (%s, %s, %s) RETURNING id_detail"
        cur.execute(detail_resep, (id_pasien, id_resep, id_pembayaran))   
    # Confirmation
    while True:
        konfirmasi = input("Apakah Anda yakin ingin menyimpan transaksi ini? (yes/no): ")
        if konfirmasi.lower() == 'yes':
            conn.commit()
            query_latest =  f"""SELECT pa.nama, d.id_detail, pe.tanggal_pembayaran, re.daftar_obat, re.harga, m.metode_pembayaran, b.nama_bank
                            FROM pasien pa
                            JOIN detail_pembayaran d ON(pa.id_pasien = d.id_pasien)
                            JOIN pembayaran pe ON(d.id_pembayaran = pe.id_pembayaran)
                            JOIN resep_obat re ON(d.id_resep = re.id_resep)
                            JOIN metode_pembayaran m ON(pe.id_metode = m.id_metode)
                            JOIN bank b ON(pe.id_bank = b.id_bank)
                            WHERE pa.nama ilike '{nama}'
                            ORDER BY pe.tanggal_pembayaran DESC
                            LIMIT '{total_input}'"""
            cur.execute(query_latest)
            conn.commit()
            data = cur.fetchall()
            col_names = [desc[0] for desc in cur.description]
            print("Pembayaran berhasil ditambahkan.")
            print(tabulate(data, headers=col_names, tablefmt="outline"))
            break
        else:
            conn.rollback()
            print("Transaksi dibatalkan.")

    cur.close()
    conn.close()
    
def menuPasien():
    os.system("cls")
    nama = input("Masukkan nama pasien: ")
    add_pasien(nama)
    while True:
        print("\n" + "+" + "-"*40 + "+")
        print("|" + " " * 18 + "Menu" + " " * 18 + "|")
        print("\n" + "+" + "-"*40 + "+")
        print("| 1. Melihat Data Pasien (Anda)" + " " * 10 + "|")
        print("| 2. Melihat Data Rekam Medis Anda" + " " * 7 + "|")
        print("| 3. Histori Pembayaran" + " " * 18 + "|")
        print("| 4. Membayar Transaksi" + " " * 18 + "|")
        print("| 5. Logout " + " " * 29 + "|")
        print("+" + "-"*40 + "+")
        pilihan = int(input("Masukkan pilihan: "))
        
        if pilihan == 1:
            read_pasien(nama)
        elif pilihan == 2:
            read_rekam(nama)
        elif pilihan == 3:
            read_pembayaran(nama)
        elif pilihan == 4:
            add_transaksi(nama)
        elif pilihan == 5:
            os.system("cls")
            print("Logout dari program")
            break
        else:
            os.system("cls")
            print("Pilihan invalid")

if __name__ == "__main__":
    menuPasien()
    
