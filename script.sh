#!/bin/bash

python3 /home/bruno/Documentos/clash/APIClashRoyale/ClashAPI.py

git add .

git commit -m "Atualização" >> /home/bruno/Documentos/clash/APIClashRoyale/run.log

git push origin master >> /home/bruno/Documentos/clash/APIClashRoyale/run.log


