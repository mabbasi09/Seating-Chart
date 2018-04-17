file = open('sampleInput.txt', 'r')

def seatFinderDriver(input, rows, columns):
	for lines in file:
		#rows and columns can be variable length, but this particular problem they are set
		rows = 3
    	columns = 11

    	#seperate file contents into chunks of data
    	input = input.split("\n")

    	reservedSeats = input[0].split(" ")
    	input[0] = reservedSeats
    
    print(input)
