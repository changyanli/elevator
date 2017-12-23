from deepqnetwork import DeepQNetwork
from RL_brain import DuelingDQN
from elev_sys import elev_sys
def train(env,RL):
    epoch_time = 30000
    start_learn = 16000
    learn_freq = 2000
    step=0
    env.get_data_info()
    last100time=[]
    last100avr=[]
    last100fin=[]
    last100index=0
    for epochs in range(epoch_time):
        #initial observation
        observation = env.reset()
        time = 0
        totalReward = 0
        while True:
            #RL choose action based on observation
            #action = RL.choose_action(observation)
            action = RL.choose_action_with_probability(observation,bias=env.control(time),epoch = epochs)
            #RL take action and get next observation and reward
            newobservation, reward, done, info = env._step(action,time)
            RL.store_transition(observation, action, reward, newobservation)
            if step > start_learn and step % learn_freq == 0 :
                RL.learn()
            totalReward += reward
            #swap observation
            observation = newobservation
            #break while loop when end of this epoch
            if done or time==10000:
                if epochs % 10 == 0:
                    print "Epoch "+str(epochs)+ " finished after "+str(time)+" step with average time "+str(env._time_reward(time)[0])+" and finished "+str(len(env.finishtime))+" people. Total reward:"+str(totalReward)
                if last100index < 100 :
                    last100time.append(time)
                    last100avr.append(env._time_reward(time)[0])
                    last100fin.append(len(env.finishtime))
                else :
                    last100time[last100index % 100] = time
                    last100avr[last100index % 100] = env._time_reward(time)[0]
                    last100fin[last100index % 100] = len(env.finishtime)
                last100index +=1
                if epochs % 20 == 0 and epochs > 100:
                    print "Last100 average finished after "+str(sum(last100time)/100)+" step with time "+str(sum(last100avr)/100)+" finished "+str(sum(last100fin)/100)+" people"
                break
            step +=1
            time +=1
    # end of training
    print 'Training over'
    env.get_data_info()
if __name__ == "__main__":
    env = elev_sys()
    #RL = DeepQNetwork(9,len(env._step(0,0)[0]))
    RL = DuelingDQN(9,len(env._step(0,0)[0]),memory_size=3000,dueling = True)
    train(env,RL)
