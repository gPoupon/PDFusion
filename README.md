# PDFusion
A tool to easily collect & merge multi-paged/sided documents scanned from a flatbed scanner for easier consumption by a document management system (like Paperless-ngx).

The Problem:

I want to scan multi-page documents using my old flatbed scanner, using it's "Scan to PC" functionality, so that I don't need to trigger scans from a computer. While I can scan pages individually, Paperless-ngx has no was to merge documents scanned in this way. Thus, a multi-page document will appear as many separate documents if just fed into Paperless-ngx natively.

The Solution:

Use the Scan to PC functionality to scan/upload documents into a monitored folder on a server. As soon as a new document is detected, start a timer (say, 2 minutes). When the timer runs out, merge all the files in the monitored directory and send it along to the Paperless-ngx consumption directory. By having a timer, you can individually scan documents/pages 1 by 1 and effectively turn them into 1 PDF. Every time a new scan is detected, the timer gets reset to give you enough time to continue scanning as many items as you want for that 1 PDF.

After the timer expires, any newly-scanned items will go towards building a 2nd merged document, and the pattern repeats.

Example Docker Compose:
```yaml
pdfusion:
    image: ghcr.io/gpoupon/pdfusion:main
    container_name: pdfusion
    environment:
      - MAX_WAIT_TIME=60
      - TZ:"America/Toronto"
    volumes:
      - scans:/tmp/input # The directory where your scanner puts scanned PDFs
      - paperless-consume:/tmp/output # The consume directory for Paperless-NGX (i.e. the output of PDFusion)
    restart: always
```

Feel free to create issues if you encounter any.
