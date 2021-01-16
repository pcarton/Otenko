FROM python

ENV LOG_LEVEL="DEBUG"

COPY email.py /otenko/email.py

ENTRYPOINT [ "python", "/otenko/email.py" ]