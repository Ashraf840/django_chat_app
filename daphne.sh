#!/bin/bash
source env/bin/activate
daphne -b 0.0.0.0 -p 8001 chatSystem.asgi:application