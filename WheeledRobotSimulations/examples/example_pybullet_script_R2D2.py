import pybullet as p
import time
import pybullet_data
physicsClient = p.connect(p.GUI) # options: p.GUI, p.DIRECT
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-10)
planeId = p.loadURDF("plane.urdf")
startPos = [0, 0, 1]
startOrientation = p.getQuaternionFromEuler([0,0,0])
boxId = p.loadURDF("r2d2.urdf", startPos, startOrientation)

startPos_Orn = p.resetBasePositionAndOrientation(boxId, startPos, startOrientation)

for i in range(1000):
	p.stepSimulation()
	time.sleep(1./240.)

cubePos, cubeOrn = p.getBasePositionAndOrientation(boxId)
print(cubePos, cubeOrn)
p.disconnect()


