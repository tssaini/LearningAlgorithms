from random import randint
import operator


class Environment:
    """The k arm bandit"""
    def __init__(self, numOfArms):
        self.numOfArms = numOfArms

        # make a list of probabilities
        list = []
        for i in range(0, numOfArms):
            list.append(randint(0,100)/100.0)
        self.list = list


    def interact(self, action):
        """Allows an agent to interact with the environment by selecting an action"""
        rewardProb = self.list[action]
        if randint(0, 100) / 100.0 <= rewardProb:
            return 1
        else:
            return 0

    def get_num_arms(self):
        return self.numOfArms

    def get_list(self):
        return self.list

    def isOptimalAction(self, action):

        # find the max prob
        opt_action, opt_act_val = max(enumerate(self.list), key=operator.itemgetter(1))

        if opt_action == action:
            return True
        else:
            return False


def distro_select(probDistro):
    numOfOutcomes = len(probDistro)
    range_var = [0.0]*numOfOutcomes

    range_var[0] = probDistro[0]
    for i in range(1, numOfOutcomes):
        range_var[i] = range_var[i-1] + probDistro[i]

    x = randint(0, 100) / 100.0

    for i in range(1, numOfOutcomes):
        if x < range_var[i]:
            return i
    return -1


class Agent:
    k = 10 # number of arms

    def __init__(self, numOfTests):
        self.numOfTests = numOfTests
        self.env = Environment(Agent.k)

    def run_greedy(self):
        list_action_val = [0.0]*Agent.k
        list_numb_action = [0]*Agent.k

        ep_val = 0.1

        # number of times optimal action was chosen. For output
        opt_action_chosen= 0
        total_reward = 0

        for i in range(1, self.numOfTests+1):

            # Run the ep-greedy algorithm
            rand = randint(0, 100) / 100.0

            if rand > ep_val:
                # pick the max option
                action, action_value = max(enumerate(list_action_val), key=operator.itemgetter(1))
            else:
                # random action
                action = randint(0, 9)
                action_value = list_action_val[action]

            result = self.env.interact(action)

            # update the number of times this action is performed
            list_numb_action[action] += 1

            # update the probability
            list_action_val[action] = round(list_action_val[action] + (1 / (list_numb_action[action])) * (result - list_action_val[action]), 2)

            # amount of times award received. For output
            total_reward += result

            if self.env.isOptimalAction(action):
                opt_action_chosen +=1

            if i % 100 == 0:
                # print the number of times optimal action was chosen and avg reward collected over time
                print "Optimal Action Chosen: "+ str(opt_action_chosen) + ", Avg Reward: "+str(total_reward / float(i))
                opt_action_chosen = 0
            # print self.env.get_list() , list_action_val, action, result


    def run_learning_automata(self):
        # make a list of probabilities that add to 0
        list_action_val = [round(1.0/Agent.k,4)]*Agent.k

        alpha = 0.1
        beta = 0.1

        # number of times optimal action was chosen. For output
        opt_action_chosen = 0
        total_reward = 0

        for i in range(1, self.numOfTests+1):

            # pick optimal option
            # action, action_value = max(enumerate(list_action_val), key=operator.itemgetter(1))

            action = distro_select(list_action_val)-1

            result = self.env.interact(action)

            if result == 1:
                # R-I algorithm
                # update probability of the action chosen
                list_action_val[action] = list_action_val[action] + alpha * (1- list_action_val[action])

                # update probability of other action
                for j in range(0, len(list_action_val)):
                    if j != action:
                        list_action_val[j] = (1 - alpha) * list_action_val[j]
            else:
                # R-P algorithm
                list_action_val[action] = (1 - beta) * list_action_val[action]
                for j in range(0, len(list_action_val)):
                    if j != action:
                        list_action_val[j] = beta/(Agent.k-1) + (1-beta)*list_action_val[j]

            # amount of times award received. For output
            total_reward += result

            if self.env.isOptimalAction(action):
                opt_action_chosen += 1

            if i % 100 == 0:
                # print the number of times optimal action was chosen and avg reward collected over time
                print "Optimal Action Chosen: "+ str(opt_action_chosen) + ", Avg Reward: "+str(total_reward / float(i))
                opt_action_chosen = 0
            # print self.env.get_list(), list_action_val, action, result


a = Agent(1000)
print "The epsilon-greedy algorithm"
a.run_greedy()
print ""
print "The linear reward-inaction and linear reward-penalty algorithm"
a.run_learning_automata()

