from deepqnetwork import DeepQNetwork
from elev_sys import elev_sys
def train(env,RL):
    epoch_time = 5000
    start_learn = 400
    learn_freq = 20
    step=0
    env.get_data_info()
    for epoch in range(epoch_time):
        #initial observation
        observation = env.reset()
        time = 0
        while True:
            #RL choose action based on observation

            #action = RL.choose_action(observation)
            if epoch < 1000:
                action = RL.choose_action_with_probability(observation,bias=env.control(time),epoch=epoch)
            else:
                action = RL.choose_action_with_probability(observation)
            #RL take action and get next observation and reward
            newobservation, reward, done, info = env._step(action,time)
            RL.store_transition(observation, action, reward, newobservation)
            if step > start_learn and step % learn_freq == 0 :
                RL.learn()
            #swap observation
            observation = newobservation
            #break while loop when end of this epoch
            if done or time==10000:
                print "Epoch "+str(epoch)+ " finished after "+str(time)+" step with average time "+str(env._time_reward(time)[0])+" and finished "+str(len(env.finishtime))+" people"
                break
            step +=1
            time +=1
    # end of training
    print 'Training over'
if __name__ == "__main__":
    env = elev_sys()
    RL = DeepQNetwork(9,len(env._step(0,0)[0]))
    train(env,RL)
