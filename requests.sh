# !/bin/bash

for _ in 1 2 3
do
  curl -X POST -F 'image=@/home/widgeton/Disk/wqGZWA7ykRg.jpg' \
  "http://127.0.0.1:8001/process_image/?pipeline_id=146bde7b-2e23-447f-84e3-b1d6f7045b62"
done
