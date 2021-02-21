@echo off
del diemthi.html
set url="http://diemthi.24h.com.vn/?v_page=1&v_sbd=03000008&v_ten=&v_cum_thi=00"
curl %url%  >> diemthi.html
start diemthi.html
echo "The script has completed %url%"