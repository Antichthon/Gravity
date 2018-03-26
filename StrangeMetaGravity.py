import numpy

def gravity(initialDistance, simLength, object_size):
    #This code models the particles' behavior when they are put at
    #"initialDistance" distance apart, and the program is allowed to run for
    #"simLength" number of ticks. Keep in mind that ticks are a measure
    #of external time, not internal time!
    tick = 0
    locx = 0
    locy = initialDistance
    #Each entry in the following list represents a unit of internal time,
    #and the distance between the particles during that unit of time.
    #I could have made seperate jump histories for particle x and
    #particle y, but they are so similiar I don't see the need.
    jump_history = []
    #The following four lists keep track of the positions of the
    #information packets sent between the two particles. their inital values
    #are to prevent the need to run the program for "initialDistance" number of ticks
    #before the particles can start communicating.
    informationxpos = [initialDistance - packetx for packetx in range(initialDistance)]
    informationxneg = [packetx for packetx in range(initialDistance)]
    informationypos = [initialDistance - packety for packety in range(initialDistance)]
    informationyneg = [packety for packety in range(initialDistance)]
    #The following list takes record of the distance between the particles
    #at the beginning of every tick. It represents distance over external time,
    #which should always average to around "initialDistance." A good test for the
    #noise in the system.
    distance_history = []
    while tick < simLength:
        restart = True
        distance = abs(locx - locy)
        distance_history.append(distance)
        while restart == True:
            #this loop is in case the particles switch sides with each other while their positions are being updated.
            xposRestart = 0
            xnegRestart = 0
            yposRestart = 0
            ynegRestart = 0
            if locx <= locy:
                for element in list(informationxpos):
                    #Checks if an information packet from particle x has reached particle y.
                    if locy <= element:
                        xposRestart = 1
                        informationxpos.remove(element) #destroys used information packets.
                        for _ in range(object_size):
                            locy_sum = 0
                            movey = numpy.random.randint(1,3) #The coinflip!
                            if movey == 1:
                                locy_sum += 1
                            else:
                                locy_sum -= 1
                        locy += locy_sum/object_size
                        #These next two lines move all packets originating from y one step.
                        informationypos[:] = [packety + 1 for packety in informationypos]
                        informationyneg[:] = [packety - 1 for packety in informationyneg]
                        informationypos.append(locy) #creates a new information packet from particle y traveling in the positive direction.
                        informationyneg.append(locy) #Same as above, but in the negative direction.
                        jump_history.append(abs(locx-locy))
                    else:
                        xposRestart = 0
                        
                for element in list(informationyneg):
                    #Same as above but for information packets from y.
                    if locx >= element:
                        ynegRestart = 1
                        informationyneg.remove(element)
                        for _ in range(object_size):
                            locx_sum = 0
                            movex = numpy.random.randint(1,3)
                            if movex == 1:
                                locx_sum -= 1      
                            else:
                                locx_sum += 1
                        locx += locx_sum/object_size
                        informationxpos[:] = [packetx + 1 for packetx in informationxpos]
                        informationxneg[:] = [packetx - 1 for packetx in informationxneg]
                        informationxpos.append(locx)
                        informationxneg.append(locx)
                        jump_history.append(abs(locx-locy))
                    else:
                        ynegRestart = 0
                        
            elif locx >= locy:
                #The same as the two chunks of code above, but in case x and y pass each other.
                for element in list(informationxneg):
                    if locy >= element:
                        xnegRestart = 1
                        informationxneg.remove(element)
                        for _ in range(object_size):
                            locy_sum = 0
                            movey = numpy.random.randint(1,3)
                            if movey == 1:
                                locy_sum += 1
                            else:
                                locy_sum -= 1
                        locy += locy_sum/object_size
                        informationypos[:] = [packety + 1 for packety in informationypos]
                        informationyneg[:] = [packety - 1 for packety in informationyneg]
                        informationypos.append(locy)
                        informationyneg.append(locy)
                        jump_history.append(abs(locx-locy))
                    else:
                        xnegRestart = 0
                        
                for element in list(informationypos):
                    if locx <= element:
                        yposRestart = 1
                        informationypos.remove(element)
                        for _ in range(object_size):
                            locx_sum = 0
                            movex = numpy.random.randint(1,3)
                            if movex == 1:
                                locx_sum -= 1   
                            else:
                                locx_sum += 1
                        locx += locx_sum/object_size
                        informationxpos[:] = [packetx + 1 for packetx in informationxpos]
                        informationxneg[:] = [packetx - 1 for packetx in informationxneg]
                        informationxpos.append(locx)
                        informationxneg.append(locx)
                        jump_history.append(abs(locx-locy))
                    else:
                        yposRestart = 0
            if xposRestart + xnegRestart + yposRestart + ynegRestart == 0:
                restart = False
        tick += 1

    return [distance_history, jump_history, locx, locy]

def Gravity_Average(iterations, initialDistance, simLength, object_size):
    #This code takes the results of Gravity given the arguments "initialDistance" and
    #"simLength" and averages the results for "iterations" number of iterations.
    distance_history_sum = 0
    distance_history_length = 0
    jump_history_sum = 0
    jump_history_length = 0
    distance_final_sum = 0
    jump_final_sum = 0
    locx_sum = 0
    locy_sum = 0
    timer = 0 
    for _ in range(iterations):
        result = gravity(initialDistance, simLength, object_size)
        distance_history_sum += sum(result[0])
        distance_history_length += len(result[0])
        jump_history_sum += sum(result[1])
        jump_history_length += len(result[1])
        distance_final_sum += result[0][-1]
        #Note that the number of entries in jump history varies, so the
        #index of the final jump is different from iteration to iteration.
        #it might be more beneficial to compare all the jumps of a specific
        #iteration.
        jump_final_sum += result[1][-1]
        locx_sum += result[2]
        locy_sum += result[3]
        timer += 1
        print(timer) #For keeping track of how the program is running.

    distance_average =  distance_history_sum / distance_history_length
    jump_history_average = jump_history_sum / jump_history_length
    distance_final_average = distance_final_sum/iterations
    jump_final_average = jump_final_sum/iterations
    locx_average = locx_sum/iterations
    locy_average = locy_sum/iterations

    print(distance_average)
    print(jump_history_average)
    print(distance_final_average)
    print(jump_final_average)
    print(locx_average)
    print(locy_average)

    
#Call to function. 10000 is a good iterator. for results that don't take forever,
#I suggest the "initialDistance" be 100, but a larger "initialDistance" value generally creates less noise.
#Watch how the jump history average decreases as "simLength" increases! I don't recommend
#simLength values higher than 10; the simulation snowballs quickly. The object
#parameter lets you simulate a bundle of connected particles instead of
#just one. higher object sizes require higher simLength values.
Gravity_Average(10000, 100, 5, 1) 
