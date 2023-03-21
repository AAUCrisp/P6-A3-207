import sys
import os
sys.path.append(f"../{os.path.abspath('.').split('/').pop()}")

import server
import client

if "--client" in sys.argv: client.main()
elif "--server" in sys.argv: server.main()
else: print("Run with either --client or --server flag")