# import other stuff
import random
import numpy as np
# import own classes
from deepq import DeepQ
import elev_sys as system
env = system.elev_sys()
epochs = 10000
steps = 10000
updateTargetNetwork = 5000
explorationRate = 1
minibatch_size = 128
learnStart = 500
learningRate = 0.00025
discountFactor = 0.99
memorySize = 1000000

last100Scores = [0] * 100
last100ScoresIndex = 0
last100Filled = False

renderPerXEpochs = 50
shouldRender = False

deepQ = DeepQ(len(env._step(0,0)[0]),9, memorySize, discountFactor, learningRate, learnStart)
deepQ.initNetworks([])

stepCounter = 0

# number of reruns
for epoch in xrange(epochs):
    observation = env.reset()
    print (explorationRate)
    # number of timesteps
    for t in xrange(steps):
        #if epoch % renderPerXEpochs == 0 and shouldRender:
        #    env.render()
        qValues = deepQ.getQValues(observation)

        action = deepQ.selectAction(qValues, explorationRate)
        newObservation, reward, done, info = env._step(action,t)
        deepQ.addMemory(observation, action, reward, newObservation, done)

        if stepCounter >= learnStart:
            if stepCounter <= updateTargetNetwork:
                deepQ.learnOnMiniBatch(minibatch_size, False)
            else :
                deepQ.learnOnMiniBatch(minibatch_size, True)

        observation = newObservation

        if done:
            if(len(env.finishtime)>0):
                print("Finish Total ",len(env.finishtime)," with average time",round(sum(env.finishtime)/len(env.finishtime),4))
            else :
                print("Finish nobody")
            last100Scores[last100ScoresIndex] = env._time_reward(t)[0]
            last100ScoresIndex += 1
            if last100ScoresIndex >= 100:
                last100Filled = True
                last100ScoresIndex = 0
            if not last100Filled:
                print ("Episode ",epoch," finished after {} timesteps".format(t+1)," with average time",last100Scores[last100ScoresIndex-1])
            else :
                print ("Episode ",epoch," finished after {} timesteps".format(t+1)," with average time",last100Scores[last100ScoresIndex-1]," last 100 average: ",(sum(last100Scores)/len(last100Scores)))
            break

        stepCounter += 1
        if stepCounter % updateTargetNetwork == 0:
            deepQ.updateTargetNetwork()
            print ("updating target network")

    explorationRate *= 0.995
    explorationRate = max (0.05, explorationRate)
