# Lightweight static viewer for the Ratchet dataset.
# Nginx serves index.html + the JSONL data files (bind-mounted by compose).
FROM nginx:1.27-alpine

COPY index.html /usr/share/nginx/html/index.html
COPY viewer.js  /usr/share/nginx/html/viewer.js
COPY viewer.css /usr/share/nginx/html/viewer.css
COPY nginx.conf /etc/nginx/conf.d/default.conf
