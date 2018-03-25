import numpy
import sys

def gravity(initialDistance, simLength):
    #This code models the particles' behavior when they are put at
    #"initialDistance" distance apart, and the program is allowed to run for
    #"simLength" number of ticks. Keep in mind that ticks are a measure
    #of external time, not internal time!
    locx = 0
    locy = initialDistance
    tick = 0
    #Each entry in the following list represents a unit of internal time,
    #and the distance between the particles during that unit of time.
    #I could have made seperate jump histories for particle x and
    #particle y, but they are so similiar I don't see the need.
    jump_history = []
    #The following two lists keep track of the positions of the
    #information packets sent between the two particles. their inital values
    #are to prevent the need to run the program for "initialDistance" number of ticks
    #before the particles can start communicating.
    informationxpos = [initialDistance - packetx for packetx in range(initialDistance)]
    informationxneg = [_ for _ in range(initialDistance)]
    informationypos = [initialDistance - packety for packety in range(initialDistance)]
    informationyneg = [_ for _ in range(initialDistance)]
    #The following list takes record of the distance between the particles
    #at the beginning of every tick. It represents distance over external time,
    #which should always average to around "initialDistance." A good test for the
    #noise in the system.
    distance_history = []
    while tick < simLength:
        restart = True
        informationxpos.append(locx)#creates a new information packet from particle x traveling in the positive direction.
        informationxneg.append(locx)#Same as above, but in the negative direction.
        informationypos.append(locy)#Same as the above two, but now for particle y.
        informationyneg.append(locy)
        distance = abs(locx - locy)
        distance_history.append(distance)
        while restart == True:
            #this loop is in case the particles switch sides with each other while their positions are being updated.
            #It also lets the particles catch packets in the cases where a packet further down the list has jumped ahead
            #of a packet earlier in the list, which does happen.
            xposRestart = 0
            xnegRestart = 0
            yposRestart = 0
            ynegRestart = 0
            if locx <= locy:
                for element in list(informationxpos):
                    #Checks if an information packet from particle x has reached particle y.
                    if locy <= element:
                        xposRestart = 1
                        movey = numpy.random.randint(1,3) #The coinflip!
                        jump_history.append(abs(locx-locy))
                        informationxpos.remove(element) #destroys used information packets.
                        if movey == 1:
                            locy += 1
                        else:
                            locy -= 1
                    else:
                        xposRestart = 0
                        
                for element in list(informationyneg):
                    #Same as above but for information packets from y.
                    if locx >= element:
                        xnegRestart = 1
                        movex = numpy.random.randint(1,3)
                        jump_history.append(abs(locx-locy))
                        informationyneg.remove(element)
                        if movex == 1:
                            locx -= 1      
                        else:
                            locx += 1
                    else:
                        xnegRestart = 0
                        
            elif locx >= locy:
                #The same as the two chunks of code above, but in case x and y pass each other.
                for element in list(informationxneg):
                    if locy >= element:
                        ynegRestart = 1
                        movey = numpy.random.randint(1,3)
                        jump_history.append(abs(x-y))
                        informationxneg.remove(element)
                        if movey == 1:
                            locy += 1
                        else:
                            locy -= 1
                    else:
                        ynegRestart = 0
                        
                for element in list(informationypos):
                    if locx <= element:
                        yposRestart = 1
                        movex = numpy.random.randint(1,3)
                        jump_history.append(abs(x-y))
                        informationypos.remove(element)
                        if movex == 1:
                            locx -= 1   
                        else:
                            locx += 1
                    else:
                        yposRestart = 0

            if xposRestart + xnegRestart + yposRestart + ynegRestart == 0:
                restart = False

        #These four following entries each move the information packets
        #one step.
        informationxpos[:] = [_ + 1 for _ in informationxpos]
        informationxneg[:] = [_ - 1 for _ in informationxneg]
        informationypos[:] = [_ + 1 for _ in informationypos]
        informationyneg[:] = [_ - 1 for _ in informationyneg]
        tick += 1

    return [distance_history, jump_history, locx, locy]


def Gravity_Average(iterations, initialDistance, simLength):
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
        result = gravity(initialDistance, simLength)
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
#Watch how the jump history average decreases very slightly as "simLength" increases! the noise also
#increases as simLength increases. as for very large simLengths, the data show strange patterns I've yet to understand,
#Such as the average entry in jump history decreasing, but the average value of the final jump paradoxically increasing.
Gravity_Average(10000, 100, 200) 
