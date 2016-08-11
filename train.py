import sys

class Stop(object):
    def __init__(self, name, position, time_to_last, time_to_next, transfers=[]):
        self.name = name
        self.position = position
        self.transfers = transfers
        self.time_to_last = time_to_last
        self.time_to_next = time_to_next


class Train(object):
    def __init__(self, name, stops={}):
        self.name = name
        self.stops = []
        self.stop_order = {}
        for k, v in stops.items():
            self.stops.append(Stop(k, v['position'], v['time_to_last'], v['time_to_next'], v['transfers']))
            self.stop_order[k] = v['position']
        self.stops = sorted(self.stops, key = lambda x: x.position)


class SubwaySystem(object):
    def __init__(self, train_lines={}):
        self.train_lines = train_lines

    def add_train_line(self, name, stops):
        train = Train(name, stops)
        self.train_lines[name] = train

    def take_train(self, origin, destination, challenge=1):
        routes = []
        origin_options = []
        destination_options = []
        ## Which train to start at
        for k, v in self.train_lines.items():
            if origin in self.train_lines[k].stop_order.keys():
                origin_options.append(k)
        ## Which train can I end at
        for k, v in self.train_lines.items():
            if destination in self.train_lines[k].stop_order.keys():
                destination_options.append(k)
        ## Cycle through options, start from origin
        for train_name in origin_options:
            route_stops = []
            # find train
            train = subway.train_lines[train_name]
            # find stop
            origin_idx = train.stop_order[origin]
            origin_stop = train.stops[origin_idx - 1]
            route_stops.append(origin_stop.name)
            # is destination on same line
            if destination in train.stop_order.keys():
                time_count = 0
                dest_idx = train.stop_order[destination]
                dest_stop = train.stops[dest_idx - 1]
                # uptown or downtown
                if dest_idx > origin_idx:
                    # uptown
                    while(origin_idx < dest_idx):
                        origin_idx += 1
                        stop = train.stops[origin_idx - 1]
                        route_stops.append(stop.name)
                        time_count += stop.time_to_last
                else:
                    # downtown
                    while(origin_idx > dest_idx):
                        origin_idx -= 1
                        stop = train.stops[origin_idx - 1]
                        route_stops.append(stop.name)
                        time_count += stop.time_to_next
                routes.append([route_stops, time_count])
            # remove origin train from destination options and check for transfer options
            try:
                destination_options.remove(train.name)
            except:
                pass
            if len(destination_options) > 0:
                for dest_train in destination_options:
                    time_count = 0
                    transfer_train = self.train_lines[dest_train]
                    # check if train connects to origin train
                    for stop in transfer_train.stops:
                        if train.name in stop.transfers:
                            # find stop to transfer
                            transfer_idx = transfer_train.stop_order[stop.name]
                            origin_transfer_idx = train.stop_order[stop.name]
                            transfer_stop = transfer_train.stops[transfer_idx - 1]
                            # ride from start to transfer
                            # uptown or downtown
                            if origin_transfer_idx > origin_idx:
                                # uptown
                                while(origin_idx < origin_transfer_idx):
                                    origin_idx += 1
                                    stop = train.stops[origin_idx - 1]
                                    route_stops.append(stop.name)
                                    time_count += stop.time_to_last
                            else:
                                # downtown
                                while(origin_idx > origin_transfer_idx):
                                    origin_idx -= 1
                                    stop = train.stops[origin_idx - 1]
                                    route_stops.append(stop.name)
                                    time_count += stop.time_to_next
                            # ride on transfer train
                            transfer_dest_idx = transfer_train.stop_order[destination]
                            if transfer_dest_idx > transfer_idx:
                                # uptown
                                while(transfer_idx < transfer_dest_idx):
                                    transfer_idx += 1
                                    stop = transfer_train.stops[transfer_idx - 1]
                                    route_stops.append(stop.name)
                                    time_count += stop.time_to_last
                            else:
                                # downtown
                                while(transfer_idx > transfer_dest_idx):
                                    transfer_idx -= 1
                                    stop = transfer_train.stops[transfer_idx - 1]
                                    route_stops.append(stop.name)
                                    time_count += stop.time_to_next
                    routes.append([route_stops, time_count])
        ## Find optimal route based on challenge requirements
        if challenge == 1:
            route_lengths = {}
            for r in routes:
                route_lengths[len(r[0])] = routes.index(r)
            optimal_route = routes[route_lengths[min(route_lengths.keys())]][0]
            return optimal_route
        elif challenge == 2:
            route_lengths = {}
            for r in routes:
                route_lengths[r[1]] = routes.index(r)
            optimal_route = routes[route_lengths[min(route_lengths.keys())]]
            return  optimal_route


if __name__ == "__main__":
    subway = SubwaySystem()
    subway.add_train_line("1",
                          {"Canal":{'transfers':[], 'position':1, 'time_to_last':0, 'time_to_next':2},
                           "Houston":{'transfers':[], 'position':2, 'time_to_last':2, 'time_to_next':1},
                           "Christopher":{'transfers':[], 'position':3, 'time_to_last':1, 'time_to_next':4},
                           "14th":{'transfers':["F","L","M","2","3"], 'position':4, 'time_to_last':4,'time_to_next':0}
                           })
    subway.add_train_line("F",
                          {"West 4th":{'transfers':["A","B","C","D","E","M"], 'position':1, 'time_to_last':0, 'time_to_next':3},
                           "14th":{'transfers':["L","M","1",'2',"3"], 'position':2, 'time_to_last':3, 'time_to_next':3},
                           "23rd":{'transfers':[],'position':3, 'time_to_last':3, 'time_to_next':4},
                           "34th":{'transfers':["B","D", "M","Q","R"], 'position':4, 'time_to_last':4, 'time_to_next':0}
                           })
    while(True):
        choice = raw_input('''
            Welcome to the Subway. What would you like to do?

            [1] Add a train
            [2] Ride train : Challenge 1
            [3] Ride train : Challenge 2
        ''')
        if choice == '1':
            position = 0
            stops = {}
            train_name = raw_input('''
                What is the name of the train you would like to add?
            ''')
            choice = "y"
            print "Let's add some stops!"
            while(choice.lower() == 'y'):
                position += 1
                stop_name = raw_input('''
                What is the name of the stop?
                ''')
                transfers = raw_input('''
                What are the transfer trains at this stop if any?
                Please delimit them by commas.
                ''')
                if transfers == "":
                    transfers = []
                else:
                    transfers = transfers.split(',')
                print transfers
                time_to_last = raw_input('''
                What is the time it takes to get to the stop before this one?
                If it is the first stop just enter 0.
                ''')
                time_to_next = raw_input('''
                What is the time it takes to get to the stop after this one?
                If it is the last stop just enter 0.
                ''')
                stops[stop_name] = {'transfers':transfers, 'position':position
                    , 'time_to_last':time_to_last, 'time_to_next':time_to_next}
                choice = raw_input('''
                Would you like to add another stop? (y/n)
                ''')
            subway.add_train_line(stop_name, stops)
        elif choice == '2':
            origin_found = False
            dest_found = False
            while(origin_found == False):
                origin = raw_input('''
                What is the starting station?
                ''')
                for k, v in subway.train_lines.items():
                    if origin in subway.train_lines[k].stop_order.keys():
                        origin_found = True
                        break
                if origin_found == False:
                    print "That isn't a valid station name. Try again."
            while(dest_found == False):
                destination = raw_input('''
                What is the destination station?
                ''')
                for k, v in subway.train_lines.items():
                    if destination in subway.train_lines[k].stop_order.keys():
                        dest_found = True
                        break
                if dest_found == False:
                    print "That isn't a valid station name. Try again."
            print subway.take_train(origin, destination, 1)
        elif choice == '3':
            origin_found = False
            dest_found = False
            while(origin_found == False):
                origin = raw_input('''
                What is the starting station?
                ''')
                for k, v in subway.train_lines.items():
                    if origin in subway.train_lines[k].stop_order.keys():
                        origin_found = True
                        break
                if origin_found == False:
                    print "That isn't a valid station name. Try again."
            while(dest_found == False):
                destination = raw_input('''
                What is the destination station?
                ''')
                for k, v in subway.train_lines.items():
                    if destination in subway.train_lines[k].stop_order.keys():
                        dest_found = True
                        break
                if dest_found == False:
                    print "That isn't a valid station name. Try again."
            print subway.take_train(origin, destination, 2)
        else:
            print "That isn't a valid choice. Choose again."

