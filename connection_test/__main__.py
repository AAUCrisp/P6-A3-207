import client
import server
import sys

if "--client" in sys.argv: client.main()
elif "--server" in sys.argv: server.main()
else: print("Run with either --client or --server flag")