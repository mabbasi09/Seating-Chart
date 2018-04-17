#!/usr/bin/python
import sys

#open txt file and store contents as string
file = open('sampleInput.txt', 'r')
input = file.read()

class SeatFinderDriver: 
    
    #initialize program and define class level variables to be shared between functions
	def __init__(self, rows, columns):
		self.rows = rows
		self.columns = columns
        
        #data structure to record seating arrangment, outer list of rows, inner list of columns
		self.seats = []
        
        #keeps track of total seats reserved and open
		self.totalSeats = rows * columns
		self.seatsReserved = 0
        
        #this will contain seating data for each row for quick lookup when trying to seat groups
		self.rowSeatData = {}

		#contains results of each group, row number, and seat positions
		self.results = {}

		#contains the data from above, but in correct format for output
		self.groupOutput = {}

		#will store input in the format we want
		self.input = ""

		self.groupKeys = {}
        
	#implement seating arrangments and track reservations and group requests for given input
	def createSeats(self, input):
		rows = self.rows
		columns = self.columns
		seats = self.seats
		
        #split lines of input into elements in list
		input = input.split("\n")

		#split first line to store list or reservations
		reservedSeats = input[0].split(" ")
		input[0] = reservedSeats

		#keep a class level copy for use with other functions
		self.input = input
        
        #initialize rows and columns, "V" means seat is vacant
		for rowIndex in range(rows):
			seats.append(["V"] * columns)
            
            #keep track of available seat info for each row
			self.rowSeatData[rowIndex + 1] = []
            
		#initialize reserved seats before all other groups
		for seat in reservedSeats:
			#each reserved seat has row num at index 1, column num at index 3 eg. "R1C4"
			rowNum = int(seat[1])
			colNum = int(seat[3])

			self.rowSeatData[rowNum].append(colNum)
            
            #mark indices of data structure as R for reserved and increment counter
			self.seats[rowNum - 1][colNum - 1] = "R"
			self.seatsReserved += 1
			self.totalSeats -= 1
            
		## called from getOptimalSeats to calculate Manhattan distance for one seat at a time
		def getManhattanDistance(point, target):
				#make sure values are ints
				point["row"] = int(point["row"])
				point["column"] = int(point["column"])
				target["row"] = int(target["row"])
				target["column"] = int(target["column"])

				# absolute value of each seat from target seat
				distance = 0
				rowDiff = abs(point["row"] - target["row"])
				colDiff = abs(point["column"] - target["column"])

				return rowDiff + colDiff

		###ALGORITHM STEPS###
		"""
		takes as input one group request at a time, returning results.
		Function is ran for each group request, minimizing distance from front center seat 
		and returns unavailable if consecutive seating not possible for group
		"""
		# 1) look at each row, starting from top, find empty consecutive seats that equal group number
		# 2) calculate sum of each seats Manhattan distance from front middle seat
		# 3) store the group positions, with distance and row data in a container
		# 4) compare the total distance of each group, then assign the minimum to the group member
		# 5) update the seating chart with these positions, increment reserved seats, decrement total seats
		# 6) format the seat positions as a range of seats e.g. "R1C5 - R1C10" and output
		def getOptimalSeats(group):
			#convert to int
			group = int(group)

			#stores data for open groups found in each row, per given group request
			groupCollection = []

			#will start looking at first row for available seats
			# for row in range(len(self.seats)):
			for rowIndex, row in enumerate(self.seats):

				#how many seats left in each row after reservations
				currRowOpenings = len(self.seats[rowIndex]) - len(self.rowSeatData[rowIndex + 1])

				#since groups cannot span 2 rows, return false if group is too big for row
				#groups also have a limit of 10
				if (group > currRowOpenings) or (group > 10):
					self.results[group] = "Not Available"
					self.groupOutput[group] = "Group " + str(group) + ": " "Not Available"
					return False

				### Seating Chart Format ###
					 #column number
				#     ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10','11']
				#row 1['R', 'V', 'V', 'R', 'V', 'V', 'V', 'V', 'V', 'V', 'V']
				#row 2['V', 'V', 'V', 'V', 'R', 'V', 'V', 'V', 'V', 'V', 'V']
				#row 3['V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V']

		        # set to middle seat index
				middle = int(self.columns + 1) / 2

				#best seat is front middle seat of chart
				bestSeat = {"row": 1, "column": middle}

				#tracks how many seats in a consecutive sequence for given group number
				seatsFound = 0

				#temporarily holds seat position values in each group until reserved seat is found or group amount found
				temps = []

				#used to store row number as key
				rowKey = str(rowIndex + 1)

				#look at every chair in row
				for i, chair in enumerate(row):
					i+=1

					#Make sure chair is available
					if (chair != "R") and (chair != "T"):

						#temporarily holds seat properties until group is formed
						seatValues = {"row": rowKey, "column": i}

						#holds the current sequence of consecutive seats
						temps.append(seatValues)
						seatsFound += 1

						#if consecutive sequence equals group number
						if seatsFound == group:
							#used to find "best" group
							groupDistance = 0

							#sum distance of each seat in that group
							for seat in temps:
								groupDistance += getManhattanDistance(seat, bestSeat)

							#this group is now an option for placement, store in collection to compare later
							groupData = {"positions": temps, "distance": groupDistance, "group_row": rowKey}
							groupCollection.append(groupData)

							#reset the sequence and temporary seat holder
							seatsFound = 0
							temps = []
					#Chair is already reserved or taken
					else:
						#if occupied seat found, consecutive sequence is broken and must start over
						temps = []
						seatsFound = 0

					#END of iterating through seats
			#END of iterating through rows
			
			if len(groupCollection) == 0:
				#if seating chart was completely filled and no consecutive seats found
				self.results[group] = "Group " + str(group) + ": " "Not Available"
				self.groupOutput[group] = "Group " + str(group) + ": " "Not Available"
				return False

			#initialize a group to compare distances and find best group
			bestSeatsDistance = groupCollection[0]["distance"]
			bestSeats = groupCollection[0]["positions"]
			bestSeatsRow = groupCollection[0]["group_row"]

			#get minimum distance of all group options for given group request
			for groupOption in groupCollection:
				if groupOption["distance"] < bestSeatsDistance:
					bestSeatsDistance = groupOption["distance"]
					bestSeats = groupOption["positions"]

			#Finally, we assign the best seats for selected group in our seating chart
			# "T" means taken
			for seatFound in bestSeats:
				seatRow = seatFound["row"] - 1
				seatCol = seatFound["column"] - 1

				self.seats[seatRow][seatCol] = "T"
				self.totalSeats -= 1
				self.seatsReserved += 1

			# print("Group no. " + str(group) + " now has seats at ")
			# print(str(bestSeats))

			# assign best group to results, group number is key
			self.results[group] = {"row": bestSeatsRow, "positions": bestSeats}

			#Lastly, store range of seats found as output
			rowResult = ""
			seatPositions = self.results[group]["positions"]

			if len(seatPositions) > 1:
				rowResult += "Group " + str(group) + ": " 
				rowResult += "R" + str(seatPositions[0]["row"]) + "C" + str(seatPositions[0]["column"]) + " - "
				rowResult += "R" + str(seatPositions[0]["row"]) + "C" + str(seatPositions[-1]["column"])
				self.groupOutput[group] = rowResult
			elif len(seatPositions) == 1:
				print("one seat only")
				rowResult += "Group " + str(group) + ": " 
				rowResult += "R" + str(seatPositions[0]["row"]) + "C" + str(seatPositions[-1]["column"])
				self.groupOutput[group] = rowResult
			
			
			print(rowResult)
			print("\n")

		#END of getOptimalSeats function

		# getOptimalSeats(5)

		#run algorithm on every group seating request
		for group in input[1:]: #only run on 2nd thru last lines of input
			getOptimalSeats(group)

		print("----------------------------")

	#END of createSeats function

	#check if a particular seat is reserved given row and column number
	def isReserved(self, row, column):

		#error checking
		if (row == 0) or (row > self.rows):
			return "Row is out of range"
		elif (column == 0) or (column > self.columns):
			return "Column is out of range"
		elif (type(row) != int) or (type(column) != int):
			return "Please enter an integer"

		#prevent off by one error for seat chart index
		#"V" is vacant
		if self.seats[row - 1][column - 1] == "V":
			return False

		return True

	#output to stdout
	def print_seats(self):
		#reference to seats data structure
		seats = self.seats

		#print seating chart, optional
		for row in seats:
			print (row)

		print("There are " + str(self.totalSeats) + " seats available")
		print("There are " + str(self.seatsReserved) + " seats reserved")
		print("\n")
		print("R is reserved") 
		print("T is taken")
		print("V is vacant")
		for result in self.groupOutput:
			sys.stdout.write(self.groupOutput[result])
			sys.stdout.write("\n")
		
# initialize driver and pass in rows and columns
#will work with any number of rows and columns
puppetShow = SeatFinderDriver(3, 11)

#fill reserved seats and group requests
puppetShow.createSeats(input)

#prints true
puppetShow.isReserved(1, 5)
#prints false
puppetShow.isReserved(1, 1)

#display output
puppetShow.print_seats()

# more tests
# someMoreSeats = SeatFinderDriver(4, 6)
# someMoreSeats.createSeats(input)
# someMoreSeats.isReserved(3, 7)
# someMoreSeats.print_seats()

file.close()
