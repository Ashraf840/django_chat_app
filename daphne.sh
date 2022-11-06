#!/bin/bash
source env/bin/activate
daphne -b 0.0.0.0 -p 8001 textextraction.asgi:application