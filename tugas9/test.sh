req=1000

for port in 45000 46000
do
    for c in 1 10 50 100
    do
        echo "Test for " $req " requests with " $c " concurrency"
        ab -n $req -c $c http://127.0.0.1:$port/ | \
        grep "Time taken\|Complete req\|Failed req\|Total trans
                \|Requests per\|Time per\|Transfer rate"
        echo
    done
done
