import psycopg2
import datetime
import os
from tabulate import tabulate
import main as ma

def connect():
    return psycopg2.connect(
        database='Proyek klinik',
        user='postgres',
        password='082143',
        host='localhost',
        port=5432
        )
    
def add_staff(nama):
    os.system("cls")
    conn = connect()
    cur = conn.cursor()
    query_check =   """SELECT * FROM staff
                    WHERE nama ilike %s
                    ORDER BY id_staff ASC"""
    cur.execute(query_check, (nama,))
    existing_staff = cur.fetchall()
    
    if existing_staff:
        print(f"Selamat Datang, {nama}!")
    else:
        print("Silahkan membuat data Staff baru")
        jenis_kelamin = input("Masukkan jenis kelamin pasien: (Laki-laki/Perempuan) ")
        if jenis_kelamin.lower() == 'laki-laki':
            jenis_kelamin = 'Laki-laki'
        elif jenis_kelamin.lower() == 'perempuan':  
            jenis_kelamin = 'Perempuan'
        else:
            print(f"Jenis kelamin {jenis_kelamin} invalid. Silahkan masukkan 'Laki-laki' atau 'Perempuan'")
        nomor_telepon = int(input("Masukkan nomor telepon Anda: "))
        
        while True:
            konfirmasi = input("Apakah Anda yakin ingin menambah pasien sesuai dengan yang diinginkan? (yes/no): ")
            if konfirmasi.lower() == 'yes':
                conn.commit()
                print("Data Pasien baru telah dimasukkan.")
                query = """INSERT INTO staff(nama, jenis_kelamin, nomor_telepon)
                        VALUES(%s,%s,%s)"""
                cur.execute(query, (nama, jenis_kelamin, nomor_telepon))
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
                    break
                    
            elif konfirmasi.lower() == 'no':
                os.system("cls")
                conn.rollback()
                print("Membuat data Pasien baru telah dibatalkan.")
                break
            else:
                print("Pilihan invalid")
            
        print(f"Selamat Datang, Staff {nama}!")
        cur.close()
        conn.close()

# Melihat isi pasien
def read_pasien():
    os.system("cls")
    conn = connect()
    cur = conn.cursor()
    query = "SELECT * FROM pasien ORDER BY id_pasien ASC"
    cur.execute(query)
    data = cur.fetchall()
    col_names = [desc[0] for desc in cur.description]
    print(tabulate(data, headers=col_names, tablefmt="outline"))
    cur.close()
    conn.close()

# Melihat isi pembayaran
def read_pembayaran():
    os.system("cls")
    conn = connect()
    cur = conn.cursor()
    query = """SELECT dp.id_detail, pa.nama, r.daftar_obat, r.harga, pe.tanggal_pembayaran, me.metode_pembayaran, ba.nama_bank
               FROM detail_pembayaran dp
               JOIN pasien pa ON(dp.id_pasien = pa.id_pasien)
               JOIN resep_obat r ON(dp.id_resep = r.id_resep)
               JOIN pembayaran pe ON(dp.id_pembayaran = pe.id_pembayaran)
               JOIN metode_pembayaran me ON(pe.id_metode = me.id_metode)
               JOIN bank ba ON(pe.id_bank = ba.id_bank)
               ORDER BY dp.id_detail ASC"""
    cur.execute(query)
    data = cur.fetchall()
    col_names = [desc[0] for desc in cur.description]
    print(tabulate(data, headers=col_names, tablefmt="outline"))
    cur.close()
    conn.close()

# Melihat isi rekam medis
def read_rekam_medis():
    os.system("cls")
    conn = connect()
    cur = conn.cursor()
    query = "SELECT * FROM rekam_medis ORDER BY nomor_rekam ASC"
    cur.execute(query)
    data = cur.fetchall()
    col_names = [desc[0] for desc in cur.description]
    print(tabulate(data, headers=col_names, tablefmt="outline"))
    cur.close()
    conn.close()

def search_rekam_pasien():
    os.system("cls")
    conn = connect()
    cur = conn.cursor()
    read_rekam_medis()
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

def add_rekam(nama):
    os.system("cls")
    conn = connect()
    cur = conn.cursor()
    query_get_id_staff = f"SELECT id_staff FROM staff WHERE nama ILIKE '{nama}'"
    cur.execute(query_get_id_staff)
    id_staff = cur.fetchone()
    id_staff = id_staff[0]
    
    read_pasien()
    pasien = input("Pilih nama pasien untuk membuat rekam medis: ")
    query_get_id_pasien = f"SELECT id_pasien FROM pasien WHERE nama ILIKE '{pasien}'"
    cur.execute(query_get_id_pasien)
    id_pasien = cur.fetchone()
    id_pasien = id_pasien[0]
    
    tanggal_pemeriksaan = datetime.date.today()
    hasil_pemeriksaan = input("Jelaskan hasil pemeriksaan pada pasien: ")
    diagnosis = input("Masukkan nama diagnosis pada pasien: ")
    query = "INSERT INTO rekam_medis(id_pasien, tanggal_pemeriksaan, hasil_pemeriksaan, diagnosis, id_staff) VALUES(%s, %s, %s, %s, %s)"
    cur.execute(query, (id_pasien, tanggal_pemeriksaan, hasil_pemeriksaan, diagnosis, id_staff))
    
    while True:
        konfirmasi = input("Apakah Anda yakin ingin menyimpan transaksi ini? (yes/no): ")
        if konfirmasi.lower() == 'yes':
            conn.commit()
            query_rekam_latest =    f"""SELECT p.id_pasien, p.nama, r.tanggal_pemeriksaan, r.hasil_pemeriksaan, r.diagnosis
                                    FROM pasien p
                                    JOIN rekam_medis r ON(r.id_pasien = p.id_pasien)
                                    WHERE p.id_pasien = '{id_pasien}'"""
            cur.execute(query_rekam_latest)
            data = cur.fetchall()
            col_names = [desc[0] for desc in cur.description]
            print("Rekam Medis baru telah selesai")
            print(tabulate(data, headers=col_names, tablefmt="outline"))
            break
        elif konfirmasi.lower() == 'no':
            conn.rollback()
            print("Rekam medis dibatalkan")
            break
        else:
            print("Pilihan invalid")
    
    read_rekam_medis()
    cur.close()
    conn.close()

def update_rekam(nama):
    os.system("cls")
    conn = connect()
    cur = conn.cursor()
    query_get_id_staff = f"SELECT id_staff FROM staff WHERE nama ILIKE '{nama}'"
    cur.execute(query_get_id_staff)
    id_staff = cur.fetchone()
    
    id_staff = id_staff[0]
    
    read_rekam_medis()
    nomor_rekam = int(input(f"Masukkan nomor_rekam yang ingin di update: "))
    
    print("Pilih atribut yang ingin diperbarui: ")
    print("1. Hasil Pemeriksaan")
    print("2. Diagnosis")
    pilihan = int(input("Masukkan pilihan: "))
    
    if pilihan == 1:
        update = input("Masukkan hasil pemeriksaan yang diubah: ")
        update_attribut = 'hasil_pemeriksaan'
        
    elif pilihan == 2:
        update = input("Masukkan diagnosis yang diubah: ")
        update_attribut = 'diagnosis'

    else:
        print("Pilihan invalid")
        cur.close()
        conn.close()
        return
    
    while True:
        konfirmasi = input("Apakah Anda yakin ingin menyimpan transaksi ini? (yes/no): ")
        if konfirmasi.lower() == 'yes':
            conn.commit()
            query = f"UPDATE rekam_medis SET {update_attribut} = '{update}' WHERE nomor_rekam = '{nomor_rekam}'"
            cur.execute(query)
            conn.commit()
            os.system("cls")
            
            update_rekam = f"SELECT * from rekam_medis WHERE nomor_rekam = '{nomor_rekam}'"
            cur.execute(update_rekam)
            data = cur.fetchall()               
            col_names = [desc[0] for desc in cur.description]
            print("Update Rekam Medis telah selesai")
            print(tabulate(data, headers=col_names, tablefmt="outline"))
            break
            
        elif konfirmasi.lower() == 'no':
            conn.rollback()
            print("Update Rekam Medis Dibatalkan")
            break
        
        else:
            print("Pilihan invalid")
                
    conn.commit()
    print(f"Total baris yang diperbarui: {cur.rowcount}")
    cur.close()
    conn.close()
    
def delete_rekam():
    os.system("cls")
    conn = connect()
    cur = conn.cursor()
    read_rekam_medis()
    nomor_rekam = input('Masukkan nomor rekam yang ingin dihapus: ')
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
    os.system("cls")
    nama = input("Masukkan nama staff: ")
    add_staff(nama)
    while True:
        print("Selamat Datang, Staff")
        print("\n" + "+" + "-"*50 + "+")
        print("|" + " " * 22 + "Menu" + " " * 24 + "|")
        print("+" + "-"*50 + "+")
        print("| {:<48} |".format("1. Melihat data Pasien"))
        print("| {:<48} |".format("2. Melihat Data Pembayaran Pasien"))
        print("| {:<48} |".format("3. Melihat Data Rekam Medis Pasien"))
        print("| {:<48} |".format("4. Mencari Pasien dari Data Rekam Medis"))
        print("| {:<48} |".format("5. Menambah Data Rekam Medis Pasien"))
        print("| {:<48} |".format("6. Memperbarui Data Rekam Medis Pasien"))
        print("| {:<48} |".format("7. Menghapus Data Rekam Medis Pasien"))
        print("| {:<48} |".format("8. Logout"))
        print("| {:<48} |".format("9. Pergi ke Main"))
        print("+" + "-"*50 + "+")
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
            add_rekam(nama)
        elif pilihan == 6:
            update_rekam(nama)
        elif pilihan == 7:
            delete_rekam()
        elif pilihan == 8:
            print("Logout dari program")
            break
        elif pilihan == 9:
            ma.main()
        else:
            print("Pilihan invalid")
            
if __name__ == "__main__":
    menuStaff()
