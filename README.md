This is a simple subway system designed in Python. The setup was to create
a system that allows for the allocation of trains and the stops associated.
After that the challenge required that I find the optimal route to get
where I need to go, first by least amount of stops then by travel time.
My code completely solves this as it takes into account the different
possible trains that you can transfer to as well as if the original
train goes straight there. It's easy to expand upon my code as I use
object-oriented design extinsively. The stops are even ordered correctly
by position in the beginning when the object is created. I tested my solution
by adding a couple train lines and switching the stops so that it was forced to
go in different directions(uptown/downtown) and run through all the different
transfer options. All in all I believe this a well designed and scalable
piece of subway code (look out MTA, you've got competition...not really).

HOW TO RUN:

Open terminal and navigate to file directory then enter in "python train.py".
This will take you through an interactive interface in your terminal.
You will be prompted with the choices of adding a train line, riding
the train using the challenge #1 logic or the challenge #2 logic.
After making your choice you will be taken through a series of
prompts to collect the necessary information for riding the train
or adding a line. Have fun!