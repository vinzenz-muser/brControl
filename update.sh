#!/bin/bash

cd dashboard
npm run build
cd ..
rm -rf admin/static/dash
cp -r dashboard/dist admin/static/dash
