# Tugas 9

## Benchmarking

Benchmarking menggunakan `apachebencmark` dengan melakukan 1000 request secara bersamaan. Test script ada di berkas `test.sh`. Hasil dapat dilihat di `result.txt`

![Contoh hasil saat menjalankan skrip](./ss_test.png)

## Result

### Async

| # | Concurrency level | Time taken for test | Complete request | Failed request | Total transferred | Requests per second  | Time per request | Transfer rate     |
|---|-------------------|---------------------|------------------|----------------|-------------------|----------------------|------------------|-------------------|
| 1 | 1     | 0.610 seconds | 1000 | 0 | 29800 bytes | 1638.60 [#/sec] (mean) | 0.610 [ms] | 476.86 [Kbytes/sec] |
| 2 | 10    | 0.429 seconds | 1000 | 0 | 29800 bytes | 2332.03 [#/sec] (mean) | 0.429 [ms] | 678.66 [Kbytes/sec] |
| 3 | 50    | 0.432 seconds | 1000 | 0 | 29800 bytes | 2314.40 [#/sec] (mean) | 0.432 [ms] | 673.53 [Kbytes/sec] |
| 4 | 100   | 0.423 seconds | 1000 | 0 | 29800 bytes | 2363.00 [#/sec] (mean) | 0.423 [ms] | 687.67 [Kbytes/sec] |

### Thread

| # | Concurrency level | Time taken for test | Complete request | Failed request | Total transferred | Requests per second  | Time per request | Transfer rate     |
|---|-------------------|---------------------|------------------|----------------|-------------------|----------------------|------------------|-------------------|
| 1 | 1     | 0.610 seconds | 1000 | 0 | 29800 bytes | 0.91 [#/sec] (mean) | 1100.214 [ms] | 0.26 [Kbytes/sec] |
| 2 | 10    | FAILED | FAILED | FAILED | FAILED | FAILED | FAILED | FAILED |
| 3 | 50    | FAILED | FAILED | FAILED | FAILED | FAILED | FAILED | FAILED |
| 4 | 100   | FAILED | FAILED | FAILED | FAILED | FAILED | FAILED | FAILED |
