#Name: Haozhe Wang  Student NO: 117101193
import time
import random

TIME_QUANTA=3

'''
This class is representation of all of the queues(blocked queue, ready queue)
encapsulates the functionality of the queue
'''
class Queue():
    def __init__(self):
        self._queue = []

    # add item to the back of the queue
    def enqueue(self,process):
        self._queue.append(process)

    # remove the item from the start of the queue
    def dequeue(self):
        if self.length() != 0:
            return self._queue.pop(0)

    # return the number of elements in the queue
    def length(self):
        return len(self._queue)
    # return the first element of the queue
    def first(self):
        if self.length() !=0:
            return self._queue[0]
    # return a meaningful queue representation
    def __str__(self):
        if self.length() == 0:
            return '[empty]'
        processes=self._queue[0].__str__()
        for k in self._queue[1:]:
            processes += ' <-- '
            processes+=k.__str__()
        return processes

"""
An encapsulation of all the required states used for describing IO operations
"""
class IOoperation():
    def __init__(self,IO_startTime,IO_timeSpan):
        # represents the IO starting point(time)
        self._IO_startTime = IO_startTime
        # represents how long will the IO operation last
        self._IO_timeSpan = IO_timeSpan

    # getter of the IO_startTime property
    def getIO_startTime(self):
        return self._IO_startTime

    # setter of the IO_startTime property
    def setIO_startTime(self,IO_startTime):
        self._IO_startTime=IO_startTime

    # getter of the IO_timeSpan property
    def getIO_timeSpan(self):
        return self._IO_timeSpan

    # setter of the IO_timeSpan property
    def setIO_timeSpan(self,IO_timeSpan):
        self._IO_timeSpan=IO_timeSpan
    IO_startTime=property(getIO_startTime,setIO_startTime)
    IO_timeSpan=property(getIO_timeSpan,setIO_timeSpan)

'''
This is the representation of one process
This class includes states for the process and the process required behaviour
'''
class Process():
    # define state variables(easier for using)
    READY = 'ready'
    BLOCKED = 'blocked'
    RUNNING = 'running'
    CREATED = 'created'
    TERMINATED = 'terminated'
    def __init__(self,id,timeRequired,IO_startTime,IO_timeSpan):
        self._id=id
        self._state=Process.CREATED
        #required timeslices of the process
        self._timeRequired=timeRequired
        #create description of the process IO operation
        self._IO=IOoperation(IO_startTime,IO_timeSpan)
    #change the process state(READY,BLOCKED...)
    def changeState(self,state):
        self._state=state

    #decreament required time slice of the process
    def decreamentTime(self):
        self._timeRequired-=1

    #decreament the remaining time of the process' IO operation
    def decreamentBlockTime(self,t):
        self._IO._IO_timeSpan-=t

    #return true if the process has finished
    def ifFinish(self):
        if self._timeRequired <= 0:
            return True
        else:
            return False

    #return true if the process now needs IO operation
    def ifIOStart(self):
        if self._IO._IO_startTime == self._timeRequired:
            return True
        else:
            return False

    #after IO operation finshed, set the IO start time to negative as a representation of finished IO
    def resetIO(self):
        #indicates IO finish
        self._IO._IO_startTime=-1

    # getter of the IO_timeSpan property
    def getIOSpan(self):
        return self._IO._IO_timeSpan

    # get the process Id
    def getId(self):
        return self._id

    # return a meaningful representation of the process
    def __str__(self):
        blockMsg=''
        if self._state==Process.BLOCKED:
            blockMsg=' | Block time remaining: %d'%(self._IO.IO_timeSpan)
        return '%s(runtime remaining: %d%s)'%(self._id,self._timeRequired,blockMsg)

    IO_timeSpan=property(getIOSpan)
    id=property(getId)

'''
This class represents the Interrupt event
The class will simulate how interrupt be generated, and provide the interrupt handler function
'''
class Interrupt():
    def __init__(self):
        #interrupt value represents a random outside condition
        self._interruptValue=random.randint(1,10)

    #when the interrupt value equals to certain number, return true, representing the interrupt should occur
    def ifInterrupt(self,value):
        if self._interruptValue == value:
            return True
        return False

    # reset the interrupt value, as representation of changing of outside world
    def initInterrupt(self):
        self._interruptValue = random.randint(1, 10)

    #run interrupt handler
    def runInterruptHandler(self):
        print('Running Interrupt Handler')
        time.sleep(1)

'''
This class represents the idle process
The class will provide idle process' functionality
'''
class IdleProcess():
    def __init__(self):
        self._process='Idle Process'

    # return the representation of idle process
    def __str__(self):
        return self._process

    # function of running idle process
    def runIdleProcess(self):
        print('Idle Process is running...')

'''
This is a stack class (representation of a memory space for suspended processes)
'''
class Stack():
    def __init__(self):
        self._stack=[]

    # push an item onto the top of the stack
    def push(self,process):
        self._stack.append(process)

    # pop an item from the top of the stack
    def pop(self):
        if self.length() != 0:
            process=self._stack.pop()
            return process

    # return the number of elements of the stack
    def length(self):
        return len(self._stack)

    #return the top element of the stack
    def top(self):
        if self.length() != 0:
            return self._stack[-1]

    #give a meaningful output of the stack
    def __str__(self):
        if self.length() == 0:
            return '[empty]'

        processes = self._stack[0].__str__()
        for k in self._stack[1:]:
            processes += ' <-- '
            processes += k.__str__()
        return processes

'''
This is the class of scheduler
'''
class Scheduler():
    def __init__(self):
        print('Scheduler initializing...\n')
        time.sleep(1)

        self._readyQueue=Queue()
        self._blockedQueue=Queue()
        self._interruptedStack=Stack()
        #assume this attribute represents the system is on
        self._powerOn=True
        #this attribute indicates the process running in the cpu
        self._cpu=None
        self._interrupt=Interrupt()
        self._idleProcess=IdleProcess()

    # create a new process and add the process to the ready queue
    def createProcess(self,processId,timeRequired, IO_startTime=-1, IO_timeSpan=0):
        process=Process(processId,timeRequired,timeRequired-IO_startTime,IO_timeSpan)
        print('%s is created' % (process.id))
        self.addReadyProcess(process)

    # turn the powerOn state to False as a representation of shutting down the system
    def powerOFF(self):
        self._powerOn=False

    # add process to the ready queue
    def addReadyProcess(self,process):
        process.changeState(process.READY)
        self._readyQueue.enqueue(process)
        print('%s is added to the ready queue'%(process.id))

    # take out the process from the cpu and add it to the blocked queue
    def addBlockedProcess(self):
        process=self.preemptProcess()
        process.changeState(process.BLOCKED)
        self._blockedQueue.enqueue(process)
        print('%s requires I/O operation --> is moved to the block queue'%(process.id))

    # run interrupt handler and then restore the process back to the cpu
    def addSuspended(self):
        process = self.preemptProcess()
        # push the process temporary onto the interrupt stack
        self._interruptedStack.push(process)
        # interruption taking control of the cpu
        self._cpu=self._interrupt
        # run interrupt handler
        self._cpu.runInterruptHandler()
        print('\tInterruption Stack: %s' % (self._interruptedStack))
        # restore the process, which is on the interrupt stack, back to cpu
        self.runProcess()

    # this method will take charge of selecting appropriate process to the cpu
    def runProcess(self):
        # to see if there is suspended process in the interrupt stack
        if self._interruptedStack.length() != 0:
            # if there is suspended process, pop the process form the stack and restore if back to the cpu
            self._cpu = self._interruptedStack.pop()
            # now self._cpu must have the suspended process
            print('Interrupt Handler finished --> %s is restored'%(self._cpu.id))
            print('%s is running in the CPU'%(self._cpu.id))
        # to see if there is an process ready to execute
        elif self._readyQueue.length() != 0:
            process=self._readyQueue.dequeue()
            process.changeState(process.RUNNING)
            self._cpu=process
            print('%s is moved to the CPU'%(process.id))
        # if there is no process in the ready queue, but have process in the blocked queue
        elif self._blockedQueue.length() !=0:
            self._cpu = self._idleProcess
            self._cpu.runIdleProcess()
        # if there is no any process to be executed, run idle process and terminate system
        else:
            self._cpu=self._idleProcess
            self._cpu.runIdleProcess()
            print('********System Sleep!*******')
            self._powerOn = False

    # take out the process which is in the cpu
    def preemptProcess(self):
        process=self._cpu
        self._cpu=None
        return process

    # decrease the IO time of the first process in the blocked queue
    def checkBlockedQueue(self,t):
        process= self._blockedQueue.first()
        if process:
            process.decreamentBlockTime(t)
            # if the process IO operation is finished
            if process.IO_timeSpan <= 0:
                self._blockedQueue.dequeue()
                process.resetIO()
                self.addReadyProcess(process)
                print('%s IO finished, moved to the ready queue'%(process.id))

    # this is the main flow of the scheduler
    # this will run processes in round robin algorithm, and make every processes time-sharing
    def schedule(self):
        # total_runTime represents the time of cpu has been running since it started
        total_runTime=0
        while self._readyQueue.length() != 0 or self._blockedQueue.length() != 0:
            print('-'*100)
            self.runProcess()
            for i in range(TIME_QUANTA):
                total_runTime += 1
                print('\nTotal runtime: %d' % (total_runTime))
                print('\tReady Queue Processes: %s' % (self._readyQueue))
                print('\tBlocked Queue Processes: %s' % (self._blockedQueue))
                print('\tRunning Process: %s' % (self._cpu))
                # decrement the IO operation time in the blocked queue
                self.checkBlockedQueue(1)
                if isinstance(self._cpu, Process):
                    # check if the current process in the cpu needs IO
                    if self._cpu.ifIOStart():
                        self.addBlockedProcess()
                        break
                    # check if interrupt occurs
                    self._interrupt.initInterrupt()
                    if self._interrupt.ifInterrupt(5):
                        self.addSuspended()

                    # the process in the cpu successfully ran one time slice
                    self._cpu.decreamentTime()
                    print('%s is successfully finished one time slice:\n\t%s'%(self._cpu.id,self._cpu))

                    # if process haven't finished after the time quanta ends
                    if not self._cpu.ifFinish() and i == TIME_QUANTA-1:
                        print('%s is not finished' % (self._cpu.id))
                        self.addReadyProcess(self._cpu)
                        self.preemptProcess()

                    # if the process finishes its execution and terminates
                    elif self._cpu.ifFinish():
                        print('%s is finished' % (self._cpu.id))
                        process=self.preemptProcess()
                        process.changeState(process.TERMINATED)
                        break
        # When there is no any process will run in the cpu, cpu will run idle process and then turn the system off
        print('='*100)
        print('=' * 100)
        self.runProcess()
    # provide an api for outside so that system will know if system can be powered off
    def getSchedulerState(self):
        return self._powerOn

class Test():
    def __init__(self):
        self._scheduler = Scheduler()
        self.createProcess()
        self.runProcess()
    # create new processes
    def createProcess(self):
        self._scheduler.createProcess('process1', 4, 2, 4)
        self._scheduler.createProcess('process2', 8)
        self._scheduler.createProcess('process3', 10)
        self._scheduler.createProcess('process4', 6, 1, 30)
    # run scheduler
    def runProcess(self):
        # while the scheduler not finishes all of its operations
        while self._scheduler.getSchedulerState():
            self._scheduler.schedule()

test=Test()
