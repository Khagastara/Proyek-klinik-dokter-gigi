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

# Melihat isi pasien
def read_pasien():
    conn = connect()
    cur = conn.cursor()
    query = "SELECT * FROM pasien"
    cur.execute(query)
    data = cur.fetchall()
    col_names = [desc[0] for desc in cur.description]
    print(tabulate(data, headers=col_names, tablefmt="outline"))
    cur.close()
    conn.close()

# Melihat isi pembayaran
def read_pembayaran():
    conn = connect()
    cur = conn.cursor()
    query = """SELECT dp.id_detail, pa.nama, r.daftar_obat, r.harga, pe.tanggal_pembayaran, me.metode_pembayaran, ba.nama_bank
               FROM detail_pembayaran dp
               JOIN pasien pa ON(dp.id_pasien = pa.id_pasien)
               JOIN resep_obat r ON(dp.id_resep = r.id_resep)
               JOIN pembayaran pe ON(dp.id_pembayaran = pe.id_pembayaran)
               JOIN metode_pembayaran me ON(pe.id_metode = me.id_metode)
               JOIN bank ba ON(pe.id_bank = ba.id_bank)"""
    cur.execute(query)
    data = cur.fetchall()
    col_names = [desc[0] for desc in cur.description]
    print(tabulate(data, headers=col_names, tablefmt="outline"))
    cur.close()
    conn.close()

# Melihat isi rekam medis
def read_rekam_medis():
    conn = connect()
    cur = conn.cursor()
    query = "SELECT * FROM rekam_medis"
    cur.execute(query)
    data = cur.fetchall()
    col_names = [desc[0] for desc in cur.description]
    print(tabulate(data, headers=col_names, tablefmt="outline"))
    cur.close()
    conn.close()

def search_rekam_pasien():
    conn = connect()
    cur = conn.cursor()
    search_pasien = input("Masukkan nama pasien yang dicari: ")
    query = """SELECT p.id_pasien, p.nama, r.nomor_rekam, r.tanggal_pemeriksaan, r.hasil_pemeriksaan, r.diagnosis
            FROM pasien p
            JOIN rekam_medis r ON(p.id_pasien = r.id_pasien)
            WHERE p.nama ILIKE %s"""
    cur.execute(query, (f"%{search_pasien}%",))
    data = cur.fetchall()
    if data:
        col_names = [desc[0] for desc in cur.description]
        print(tabulate(data, headers=col_names, tablefmt="outline"))
    else:
        print(f"Tidak ada {search_pasien} di dalam rekam medis tersebut")
    cur.close()
    conn.close()

def add_rekam():
    conn = connect()
    cur = conn.cursor()
    read_pasien()
    id_pasien = int(input(f"Masukkan id pasien yang sesuai dengan nama pasien: "))
    tanggal_pemeriksaan = datetime.date.today()
    hasil_pemeriksaan = (f"Jelaskan hasil pemeriksaan pada pasien: ")
    diagnosis = (f"Masukkan nama diagnosis pada pasien: ")
    id_staff = 1
    query = f"INSERT INTO rekam_medis(id_pasien, tanggal_pemeriksaan, hasil_pemeriksaan, diagnosis) VALUES(%s, %s, %s, %s)"
    cur.execute(query, (id_pasien, tanggal_pemeriksaan, hasil_pemeriksaan, diagnosis, id_staff))
    conn.commit()
    read_rekam_medis()
    cur.close
    conn.close()

def update_rekam():
    conn = connect()
    cur = conn.cursor()
    read_rekam_medis()
    nomor_rekam = int(input(f"Masukkan nomor_rekam yang ingin di update: "))
    
    print("Pilih atribut yang ingin diperbarui: ")
    print("1. Hasil Pemeriksaan")
    print("2. Diagnosis")
    pilihan = int(input("Masukkan pilihan: "))
    
    if pilihan == 1:
        update = input("Masukkan hasil pemeriksaan yang diubah: ")
        query = "UPDATE rekam_medis SET hasil_pemeriksaan = %s WHERE nomor_rekam = %s"
    elif pilihan == 2:
        update = input("Masukkan diagnosis yang diubah: ")
        query = "UPDATE rekam_medis SET diagnosis = %s WHERE nomor_rekam = %s"
    else:
        print("Pilihan invalid")
        cur.close()
        conn.close()
        return
    
    cur.execute(query, (update, nomor_rekam))
    conn.commit()
    print(f"Total baris yang diperbarui: {cur.rowcount}")
    read_rekam_medis(cur)
    cur.close()
    conn.close()
    
def delete_rekam():
    conn = connect()
    cur = conn.cursor()
    read_rekam_medis()
    nomor_rekam = input('Masukkan nomor rekam yang ingin dihapus: ')
    query_delete = f"DELETE FROM rekam_medis WHERE nomor_rekam = {nomor_rekam}"
    konfirmasi = input(f"Apakah Anda yakin ingin menghapus dengan nomor rekam {nomor_rekam} ini?: (yes/no)")
    if konfirmasi.lower() == 'yes':
        query_delete = f"DELETE FROM rekam_medis WHERE nomor_rekam = {nomor_rekam}"
        cur.execute(query_delete, (nomor_rekam))
    elif konfirmasi.lower() == 'no':
        print("Penghapusan dibatalkan")
    else:
        print(f"Pilihan invalid")
        cur.close()
        conn.close()
        return    
    
    cur.execute(query_delete)
    print(f"Total baris yang diubah: {cur.rowcount}")
    conn.commit()  
    cur.close()
    conn.close()
    
def menuStaff():
    while True:
        print("Selamat Datang, Staff")
        print("\nMenu:")
        print("1. Melihat data Pasien")
        print("2. Melihat Data Pembayaran Pasien")
        print("3. Melihat Data Rekam Medis Pasien")
        print("4. Mencari Pasien dari Data Rekam Medis")
        print("5. Menambah Data Rekam Medis Pasien")
        print("6. Memperbarui Data Rekam Medis Pasien")
        print("7. Menghapus Data Rekam Medis Pasien")
        print("8. Logout")
        pilihan = int(input("Masukkan pilihan: "))
        
        if pilihan == 1:
            read_pasien()
        elif pilihan == 2:
            read_pembayaran()
        elif pilihan == 3:
            read_rekam_medis()
        elif pilihan == 4:
            search_rekam_pasien()
        elif pilihan == 5:
            add_rekam()
        elif pilihan == 6:
            update_rekam()
        elif pilihan == 7:
            delete_rekam()
        elif pilihan == 8:
            print("Logout dari program")
            break
        else:
            print("Pilihan invalid")
            
if __name__ == "__main__":
    menuStaff()
