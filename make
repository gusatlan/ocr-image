#!/bin/bash
docker build -t dockerregistry:5000/ocr-image-app:1.0.0 .
docker build -t dockerregistry:5000/ocr-image-app:latest .
docker push dockerregistry:5000/ocr-image-app:1.0.0
docker push dockerregistry:5000/ocr-image-app:latest

