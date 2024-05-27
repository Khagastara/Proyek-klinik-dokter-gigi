CREATE TABLE dokter(
	id_dokter SERIAL PRIMARY KEY,
	nama VARCHAR(100) NOT NULL,
	jenis_kelamin VARCHAR(9) NOT NULL,
	nomor_telepon VARCHAR(12) UNIQUE
);

CREATE TABLE staff(
	id_staff SERIAL PRIMARY KEY,
	nama VARCHAR(100) NOT NULL,
	jenis_kelamin VARCHAR(9) NOT NULL,
	nomor_telepon VARCHAR(12) UNIQUE
);

CREATE TABLE bank(
	id_bank SERIAL PRIMARY KEY,
	nama_bank VARCHAR(10) NOT NULL
);

CREATE TABLE metode_pembayaran(
	id_metode SERIAL PRIMARY KEY,
	metode_pembayaran VARCHAR(10) NOT NULL
);

CREATE TABLE pasien(
	id_pasien SERIAL PRIMARY KEY,
	nama VARCHAR(100) NOT NULL,
	jenis_kelamin VARCHAR(9) NOT NULL,
	nomor_telepon VARCHAR(12) UNIQUE,
	alamat VARCHAR(100) NOT NULL
);

CREATE TABLE pembayaran(
	id_pembayaran SERIAL PRIMARY KEY,
	tanggal_pembayaran DATE NOT NULL,
	id_metode INT,
	id_bank INT,
CONSTRAINT fk_metode_pembayaran
	FOREIGN KEY ("id_metode")
	REFERENCES metode_pembayaran ("id_metode")
	ON DELETE CASCADE,
CONSTRAINT fk_bank
	FOREIGN KEY ("id_bank")
	REFERENCES bank ("id_bank")
	ON DELETE CASCADE
);

CREATE TABLE resep_obat(
	id_resep SERIAL PRIMARY KEY,
	id_dokter INT,
	daftar_obat VARCHAR(100) NOT NULL,
	jumlah_obat INT NOT NULL,
	harga INT NOT NULL,
CONSTRAINT fk_dokter
	FOREIGN KEY ("id_dokter")
	REFERENCES dokter ("id_dokter")
	ON DELETE CASCADE
);

CREATE TABLE detail_pembayaran(
	id_detail SERIAL PRIMARY KEY,
	id_pasien INT,
	id_resep INT,
	id_pembayaran INT,
CONSTRAINT fk_pasien
	FOREIGN KEY ("id_pasien")
	REFERENCES pasien ("id_pasien")
	ON DELETE CASCADE,
CONSTRAINT fk_resep_obat
	FOREIGN KEY ("id_resep")
	REFERENCES resep_obat ("id_resep")
	ON DELETE CASCADE,
CONSTRAINT fk_pembayaran
	FOREIGN KEY ("id_pembayaran")
	REFERENCES pembayaran ("id_pembayaran")
	ON DELETE CASCADE
);

CREATE TABLE rekam_medis(
	nomor_rekam SERIAL PRIMARY KEY,
	id_pasien INT,
	tanggal_pemeriksaan DATE NOT NULL,
	hasil_pemeriksaan VARCHAR(300) NOT NULL,
	diagnosis VARCHAR(100) NOT NULL,
	id_staff INT,
CONSTRAINT fk_staff
	FOREIGN KEY ("id_staff")
	REFERENCES staff ("id_staff")
	ON DELETE CASCADE,
CONSTRAINT fk_pasien
	FOREIGN KEY ("id_pasien")
	REFERENCES pasien ("id_pasien")
	ON DELETE CASCADE
);

INSERT INTO dokter(nama, jenis_kelamin, nomor_telepon)
VALUES ('Dewi Kusumawati', 'Perempuan', '087752657808');
select * from dokter;

INSERT INTO metode_pembayaran(metode_pembayaran)
VALUES ('Tunai'),
		('Non-Tunai');
select * from metode_pembayaran;
		
INSERT INTO staff(nama, jenis_kelamin, nomor_telepon)
VALUES ('Amara Kanya Maharani', 'Perempuan', '085748435663');
select * from staff;

INSERT INTO bank(nama_bank)
VALUES	('non-Bank'),
		('BRI'),
		('BCA'),
		('BNI'),
		('Mandiri'),
		('BSI');
SELECT * FROM bank;

INSERT INTO pasien(nama, jenis_kelamin, nomor_telepon, alamat)
VALUES 	('Adit', 'Laki-laki', '082324678212', 'Jl. Jawa VI'),
		('Agus', 'Laki-laki', '085678987987', 'Jl. Halmahera II'),
		('Yunita', 'Perempuan', '081234345687', 'Jl. Bangka III'),
		('Silvi', 'Perempuan', '085876908764', 'Jl. Nias I'),
		('Putri', 'Perempuan', '081545675467', 'Jl. Sumatra III');
SELECT * FROM pasien;

INSERT INTO pembayaran(tanggal_pembayaran, id_metode, id_bank)
VALUES 	('2024-5-14', 1, 1),
		('2024-5-16', 2, 3),
		('2024-5-20', 2, 2),
		('2024-5-21', 1, 1),
		('2024-5-21', 2, 2);
SELECT * FROM pembayaran;

INSERT INTO resep_obat(daftar_obat, jumlah_obat, harga, id_dokter)
VALUES	('Paracetamol', 10, 6000, 1),
		('Topcilin', 15, 10000, 1),
		('Neuralgin', 5, 25000, 1),
		('Cataflam', 21, 30000, 1),
		('Antalgin', 25, 15000, 1),
		('Asan Mefenamat', 10, 3000, 1);
SELECT * FROM resep_obat;

INSERT INTO detail_pembayaran(id_pasien, id_resep, id_pembayaran)
VALUES 	(1, 2, 1),
		(1, 6, 1),
		(2, 3, 2),
		(2, 5, 2),
		(2, 6, 2),
		(3, 1, 3),
		(3, 2, 3),
		(4, 6, 4),
		(4, 1, 4),
		(5, 1, 5),
		(5, 6, 5);
SELECT * FROM detail_pembayaran;


INSERT INTO rekam_medis(tanggal_pemeriksaan, id_pasien, hasil_pemeriksaan, diagnosis, id_staff)
VALUES	('2024-5-14', 1, 'Gigi lubang berwarna kehitaman pada oklusal dan proksimal gigi, tes perkusi negative, tes tekan negative, tes dingin positif.', 'Karies mencapai enamel gigi', 1),
		('2024-5-16', 2, 'Muncul benjolan berisi cairan berwarna bening, putih, kebiruan, atau kemerahan.', 'Kista mulut', 1),
		('2024-5-20', 3, 'Gusi gigi yang berwarna merah, lunak, atau bengkak', 'Gingivitis', 1),
		('2024-5-21', 4, 'Penumpukan plak di gigi', 'Periodontitis', 1),
		('2024-5-21', 5, 'Bengkak pada kelenjar getah bening di leher', 'Pulpitis', 1);
SELECT * FROM rekam_medis