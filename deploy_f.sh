#!/bin/bash
cd frontend
npm run build:prod
cd ..
tar -zcf dist.tar.gz dist
scp dist.tar.gz root@ten:/root
ssh root@ten "rm -rf dist; tar -zxf dist.tar.gz; rm -f dist.tar.gz; cd backend; ./public/app.sh r"
rm -f dist.tar.gz
