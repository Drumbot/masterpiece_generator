masterpiece_generator
=====================

Simple ngram model trainer which generates output text based on input data

# How to use it
Just run the program with arguments -l, -i and -o, for length of output and input and output files

ex: $ python masterpiece\_generator.py -l 200 -i my\_training\_file.txt -o my\_output\_file.txt

###TODO
- Add an argument to model\_trainer to control the value of _n_ in _ngram_
- Add command line option to give user option to give a whole directory of text files, instead of requiring a single text file

