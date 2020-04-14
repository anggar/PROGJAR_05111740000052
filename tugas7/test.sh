for c in 1 5 10
do
    echo "Test for 10 requests with " $c " concurrency"
    ab -n 10 -c $c http://127.0.0.1:10001/ | \
    grep "Time taken\|Complete req\|Failed req\|Requests per\
            \|Time per\|Transfer rate"
    echo
done

for c in 1 10 30 50
do
    echo "Test for 50 requests with " $c " concurrency"
    ab -n 50 -c $c http://127.0.0.1:10001/ | \
    grep "Time taken\|Complete req\|Failed req\|Requests per\
            \|Time per\|Transfer rate"
    echo
done

for c in 1 10 50 100
do
    echo "Test for 100 requests with " $c " concurrency"
    ab -n 100 -c $c http://127.0.0.1:10001/ | \
    grep "Time taken\|Complete req\|Failed req\|Requests per\
            \|Time per\|Transfer rate"
    echo            
done
