# Seating-Chart
## Algorithm for finding optimal reservations for a group of seats

This program is designed to help place groups of people in the ideal seats available in a two dimensional seating chart
of rows and columns. Given a group number, the program will keep track of available seating blocks and minimize the 
combined [manhattan distance](https://en.wiktionary.org/wiki/Manhattan_distance) of the group from the front center seat. There are a few rules:

-the group seats must all be consecutive without gaps (i.e. for a group request of 5, these 5 seats must all be next to eachother) <br>
-the group seats cannot span multiple columns (must be contained in one row)

Also, there are a few other useful functions

-seating chart may be initialized to any number of rows and columns <br>
-seating chart will return if a specific seat is reserved or not <br>
-will output the final group placement seats one seating is arranged, along with total remaining seats

Currently, the program is setup to read a text file from stdin with the following format:

R1C4 R1C8 R2C3 <br>
4 <br>
3 <br>
7 <br>
4 <br>

The first line represents the reserved (unavailable) seats indicating the row and column values. Every subsequent 
line represents an integer of a group request of seats.
