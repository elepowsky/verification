from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

import numpy as np
import time

import sys
import datetime

import socket

t = str(datetime.datetime.now())
trial_num = str(sys.argv[1])
max_step = str(sys.argv[2])
max_step = float(max_step)

th = [70,90,110,110,90,70] # higher value = closer approach

clear = True
new = True
pause_start = time.time()

start = time.time()
pause = 0
speed = 10 # (cm/s)
duration = max_step/speed # (s)

########################################################################
############   NAI DETECTOR   ############   RASPBERRY PI   ############
########################################################################

host = '##:##:##:##:##:##'
port = 7
backlog = 1
size = 1024
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((host,port))
s.listen(backlog)
print(f'Listening on {host}:{port}')

try:
    client, address = s.accept()
except:
    s.close()
    exit()
    
def receive(client):
    while True:
        try:
            data = client.recv(size)
            print(data.decode().strip())
            if data:
                break
        except:
            break

cmd = 'connect'
client.send(bytes(cmd, 'UTF-8'))
print('Sent: ', cmd, str(datetime.datetime.now()))
receive(client)

cmd = 'on'
client.send(bytes(cmd, 'UTF-8'))
print('Sent: ', cmd, str(datetime.datetime.now()))
receive(client)

########################################################################
############   NAI DETECTOR   ############   RASPBERRY PI   ############
########################################################################


robot = Create3(Bluetooth())


seconds = 3

filename = 'log_files/log_'+t[0:4]+t[5:7]+t[8:10]+'_step_'+str(int(max_step))+'_trial'+trial_num+'.txt'
log = open(filename,'a')

log.write('Speed (cm/s): ')
log.write(str(speed))
log.write('\n')

log.write('Max Step (cm): ')
log.write(str(max_step))
log.write('\n')

log.write('Measurement Time (s): ')
log.write(str(seconds))
log.write('\n')


def obstacle(sensors):
    print(sensors)
    for sensor, t in zip(sensors, th):
        if sensor > t:
            print('Obstacle detected!')
            return True
    return False


async def print_pos(robot):
    global log
    
    pos = await robot.get_position()
    log.write('Position: ')
    log.write(str(pos.x))
    log.write(',')
    log.write(str(pos.y))
    log.write('\n')
    print(pos.x, pos.y)
    
    
async def forward(robot):
    global speed
    
    await robot.set_lights_rgb(0, 255, 0)
    await robot.set_wheel_speeds(speed,speed)
    
    
async def stop(robot):
    
    await robot.set_wheel_speeds(0,0)
    await robot.set_lights_rgb(255, 0, 0)
    
    
async def hold(robot):
    
    await robot.set_wheel_speeds(0,0)
    await robot.set_lights_rgb(0, 0, 255)
    
    
@event(robot.when_bumped, [True, True]) # record collision to log
async def bumped(robot):
    global log
    
    print('')
    print('Collision Detected')
    print('')
    log = open(filename,'a')
    log.write('\n')
    log.write('Collision Detected\n')

        
@event(robot.when_bumped, [True, True]) # back up after collision
async def bumped(robot):
    global pause
    
    bump_start = time.time()
    await robot.set_lights_rgb(0, 0, 255)
    await robot.move(-10)
    pause += (time.time() - bump_start)


def measure(seconds):
    global client

    cmd = str(seconds)
    client.send(bytes(cmd, 'UTF-8'))
    print('Sent: ', cmd, str(datetime.datetime.now()))
    
    while True:
        try:
            data = client.recv(size)
            #print(data)
            if data:
                data = data.decode().strip()
                #print(data)
                if data.isnumeric():
                    total = int(data)
                    print('Received: ', total)
                    return total
                    break
        except:
            break


def algorithm(counts, B, max_step):
    if counts > B + 2.33*np.sqrt(B):
        step = np.random.uniform(low=0, high=0.1*max_step)
    else:
        step = np.random.uniform(low=0, high=max_step)
    return step
    

iteration = 0
@event(robot.when_play) # main event loop for random walk
async def play(robot):
    global start, pause, duration, log, clear, pause_start, max_step, seconds, client, iteration
    
    GO = True
    
    while GO is not False:
        
        try:
            
            log = open(filename,'a')
            log.write('\n')
            print('')
            print('')
            await print_pos(robot)
        
            if clear:
                sensors = (await robot.get_ir_proximity()).sensors
                log.write('IR Readings: ')
                log.write(str(sensors))
                log.write('\n')
                if obstacle(sensors):
                    pause_start = time.time()
                    clear = False
                    await stop(robot)
                    await robot.set_lights_rgb(255, 0, 0)
                    log.write('Obstacle Detected\n')
                    
            if clear:
                await forward(robot)
                if (time.time() - start) >= (duration + pause):
                    log.write('Time Elapsed: ')
                    log.write(str(time.time() - start))
                    log.write('\n')
                    print('Time Elapsed: ',(time.time() - start))
                    log.write('Changing Direction\n')

                    ########################################################################
                    ############   NAI DETECTOR   ############   RASPBERRY PI   ############
                    ########################################################################
                    
                    await hold(robot)
                    print('Measuring...')
                    total = measure(seconds)
                    
                    iteration += 1
                    print(iteration)
                    if iteration > 1000:
                        GO = False
                    
                    ########################################################################
                    ############   NAI DETECTOR   ############   RASPBERRY PI   ############
                    ########################################################################
                    
                    print(total/seconds)
                    log.write('Detected Counts: ')
                    log.write(str(total))
                    log.write('\n')
                    
                    print('Changing direction')
                    angle = np.random.rand(1)*360
                    if angle <= 180:
                        await robot.turn_left(angle)
                    else:
                        angle = 360 - angle
                        await robot.turn_right(angle)
                    step = algorithm(total/seconds, 25, max_step)
                    duration = step/speed
                    log.write('Next Step: ')
                    log.write(str(step))
                    log.write('\n')
                    log.write('Next Duration: ')
                    log.write(str(duration))
                    log.write('\n')
                    print('Set step (duration): ',step,' (',duration,')')
                    pause = 0
                    start = time.time()
                    
            else:
                sensors = (await robot.get_ir_proximity()).sensors
                if obstacle(sensors):
                    angle = np.random.rand(1)*360
                    if angle <= 180:
                        await robot.turn_left(angle)
                    else:
                        angle = 360 - angle
                        await robot.turn_right(angle)
                else:
                    pause += (time.time() - pause_start)
                    log.write('Paused Time: ')
                    log.write(str(pause))
                    log.write('\n')
                    print('Paused time: ',pause)
                    clear = True
                    await robot.set_lights_rgb(0, 255, 0)
                
            if GO is False:
                cmd = 'off'
                client.send(bytes(cmd, 'UTF-8'))
                print('Sent: ', cmd, str(datetime.datetime.now()))
                await stop(robot)
                receive(client)
                cmd = 'quit'
                client.send(bytes(cmd, 'UTF-8'))
                print('Sent: ', cmd, str(datetime.datetime.now()))
                time.sleep(1)
                client.close()
                s.close()
        
        except KeyboardInterrupt:
            cmd = 'off'
            client.send(bytes(cmd, 'UTF-8'))
            print('Sent: ', cmd, str(datetime.datetime.now()))
            await stop(robot)
            receive(client)
            cmd = 'quit'
            client.send(bytes(cmd, 'UTF-8'))
            print('Sent: ', cmd, str(datetime.datetime.now()))
            time.sleep(1)
            client.close()
            s.close()
            GO = False
            
        except:
            cmd = 'off'
            client.send(bytes(cmd, 'UTF-8'))
            print('Sent: ', cmd, str(datetime.datetime.now()))
            await stop(robot)
            receive(client)
            cmd = 'quit'
            client.send(bytes(cmd, 'UTF-8'))
            print('Sent: ', cmd, str(datetime.datetime.now()))
            time.sleep(1)
            client.close()
            s.close()
            GO = False
            
            
robot.play()
log.close()
