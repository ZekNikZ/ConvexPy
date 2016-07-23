# ConvexPy
ConvexPy is the Python re-write of the programming langauge [Convex](https://github.com/GamrCorps/Convex), also created by me. ConvexPy is designed to be faster, more efficient, more accurate, and more. You can view the documentation [here].

##Running ConvexPy
Run `convex.py` as any normal Python **3.4+** script:

    python convex.py
This will give an error, as you need to add some command-line flags. Here is a list:

    -help: display the usage information of this program.
    -h: display the usage information of this program.
    -?: display the usage information of this program.
    -accuracy <digits>: changes the accuracy for mathematical operations and constants.
    -a <digits>: changes the accuracy for mathematical operations and constants.
    -file <file>: runs the program specified in the file at the path provided, using the CP-1252 encoding.
    -f <file>: runs the program specified in the file at the path provided, using the CP-1252 encoding.
    -code <code>: runs the code provided.
    -c <code>: runs the code provided.
    -shell: starts an interactive Convex independent shell.
    -s: starts an interactive Convex independent shell.
    -repl: starts an interactive Convex REPL shell.
    -r: starts an interactive Convex REPL shell.
    -safe: disables file IO, Python eval, and operators with internet access.
    -sm: disables file IO, Python eval, and operators with internet access.
    -debug: prints the stack in list form after program execution.
    -d: prints the stack in list form after program execution.
For example, to open a ConvexPy shell, run the following command:

    python convex.py -shell
