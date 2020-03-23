# Pemrograman Jaringan

> Anggar Wahyu Nur W.

> 05111740000052

## Protokol

Sarana komunikasi antara klien dan server akan menggunakan format JSON dengan format

```json
{"cmd": "command", "data": "data"}
```

## Fitur

+ Meletakkan berkas
+ Mengambil berkas
+ Melihat daftar berkas

## Tata Cara

```sh
python3 client.py [OPTION]... COMMAND [COMMAND_ARG] 
```

#### Options

+ `--host` alamat *host* yang dipakai
+ `--post` *port* yang digunakan

### Request

### Response