#!/bin/bash
python3 server.py & python3 run_clients.py

#lsof -i :7788