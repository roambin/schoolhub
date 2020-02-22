#!/bin/bash
cd backend
tar -zcf app.tar.gz app
tar -zcf public.tar.gz public
scp app.tar.gz public.tar.gz root@ten:/root/backend
ssh root@ten "cd backend; rm -rf app public; tar -zxf app.tar.gz; tar -zxf public.tar.gz; rm -f app.tar.gz public.tar.gz; chmod 777 ./public/app.sh; ./public/app.sh r"
rm -f app.tar.gz public.tar.gz
