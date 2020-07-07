#!/bin/bash

python3 /home/bruno/Documentos/clash/APIClashRoyale/ClashAPI.py

cd /home/bruno/Documentos/clash/APIClashRoyale/ && git add . 

cd /home/bruno/Documentos/clash/APIClashRoyale/ && git commit -m "Atualização" 

cd /home/bruno/Documentos/clash/APIClashRoyale/ && git push origin master 

echo "###############################################" >> run.log
echo "Hora e data da ultima atualização: " >> run.log
date >> run.log  
echo "###############################################" >> run.log


