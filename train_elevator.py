from deepqnetwork import DeepQNetwork
from RL_brain import DuelingDQN
from elev_sys import elev_sys
import sys
def train(env,RL,num=0):
    epoch_time = 30000
    start_learn = 2400
    learn_freq = 500
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
            if num % 2 == 0 :
                action = RL.choose_action(observation)
            else :
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
                    print(epochs,time,env._time_reward(time)[0],len(env.finishtime),totalReward)
                    #print "Epoch "+str(epochs)+ " finished after "+str(time)+" step with average time "+str(env._time_reward(time)[0])+" and finished "+str(len(env.finishtime))+" people. Total reward:"+str(totalReward)
                if last100index < 100 :
                    last100time.append(time)
                    last100avr.append(env._time_reward(time)[0])
                    last100fin.append(len(env.finishtime))
                else :
                    last100time[last100index % 100] = time
                    last100avr[last100index % 100] = env._time_reward(time)[0]
                    last100fin[last100index % 100] = len(env.finishtime)
                last100index +=1
                if epochs % 100 == 0 and epochs >= 100:
                    print("last100",sum(last100time)/100.,sum(last100avr)/100.,sum(last100fin)/100.)
                if epochs % 1000 == 0 :
                    RL.save(num)
                    #print "Last100 average finished after "+str(sum(last100time)/100)+" step with time "+str(sum(last100avr)/100)+" finished "+str(sum(last100fin)/100)+" people"
                break
            step +=1
            time +=1
    # end of training
    print 'Training over'
    env.get_data_info()
if __name__ == "__main__":
    if len(sys.argv) == 1 :
        num = 0
    else:
        num = (int)(sys.argv[1])
    env = elev_sys(num=num,oddeven=False)
    if num / 2 < 1 :
        #RL = DeepQNetwork(9,len(env._step(0,0)[0]),batch_size=64,e_greedy_increment=0.001)
        RL = DuelingDQN(9,len(env._step(0,0)[0]),memory_size=10000,dueling = False,e_greedy_increment=0.00005)
    else:
        RL = DuelingDQN(9,len(env._step(0,0)[0]),memory_size=10000,dueling = True,e_greedy_increment=0.0001)
    #RL.load(3)
    train(env,RL,num=num)
    RL.save(num)
