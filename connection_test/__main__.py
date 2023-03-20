import sys
sys.path.append("../P6-A3-207")

import server
import client

if "--client" in sys.argv: client.main()
elif "--server" in sys.argv: server.main()
else: print("Run with either --client or --server flag")