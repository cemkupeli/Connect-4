Connect4:
	echo "#!/bin/bash" > Connect4
	echo "pypy3 test_connect4.py \"\$$@\"" >> Connect4
	chmod u+x Connect4