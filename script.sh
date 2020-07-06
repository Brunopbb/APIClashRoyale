#!/bin/bash

python3 /home/bruno/Documentos/clash/APIClashRoyale/ClashAPI.py

git add .

git commit -m "Atualização" >> run.log

git push origin master
