import copy
import random
import numpy as np


# multi queue data structure
class Multi_Queue(object):
    # queue
    def __init__(self):
        self.items = []

    # queue is empty or not
    def is_empty(self):
        return self.items == []

    def queue_in(self, item):
        # customer step in queue
        self.items.append(item)
        # customer step out queue

    def queue_out(self):
        #customer step out queue
        return self.items.pop(0)

    def queue_size(self):
        # return the queue len
        return len(self.items)

    def get_queue_first(self):
        # get the first custome in the queue
        if self.is_empty():
            return False
        else:
            return self.items[0]

    def get_cust_info(self):
        return self.items


class Customer:
    def __init__(self, t=-1):
        self.server_time = t  # 顾客所需要的服务时间
        self.waiting_time = 0



# 找出目前等待总时间最短的窗口号码
def min_queue(agents, agent_num):
    #return the shortest length of queue
    min_size_queue = 9999
    min_agent = 9999
    for i in range(agent_num):
        if agents[i].is_empty():
            return i
        else:
            len_q = agents[i].queue_size()
        if len_q < min_size_queue:
            min_size_queue = len_q
            min_agent = i
    return min_agent


# 模拟函数
def multi_que(agent_num: int, servTime: int, initial_cust_list,new_customer_come):
    total_wait = 0
    total_cust = 0


    agents = [Multi_Queue() for _ in range(agent_num)]  # 生成一个有n个链队列的列表，即每个链队列都是每个窗口的队列
    for z in range(len(initial_cust_list)):
        shortest_queue = min_queue(agents, agent_num)
        init_cu = initial_cust_list[z]
        customer = Customer(init_cu)
        agents[shortest_queue].queue_in(customer)
    for now in range(servTime):  # 遍历每一个时刻
        print("现在是第", now, "时刻")
        empty_not = 1
        for k in range(agent_num):
            if agents[k].queue_size() > 1 :
                empty_not = 0

        if empty_not == 1:
            break
        if now % new_customer_come == 0:
            print("有顾客来了！")
            shortest_queue = min_queue(agents, agent_num)
            cu_ser_time = random.randint(1, 15)  # 这里假设顾客的所需服务时间为[1,20)
            customer = Customer(cu_ser_time)
            agents[shortest_queue].queue_in(customer)
            print("TA的窗口是%s，TA所需服务时间是%s" % (shortest_queue, cu_ser_time))
            print("第%s个客人到第%s个窗口排队中..." % (now, shortest_queue))
        else:
            print("此刻没有客人来！")
        for i in range(agent_num):
            if not agents[i].is_empty():
                if agents[i].get_queue_first().server_time == 0:
                    agents[i].queue_out()
                    if not agents[i].is_empty():
                        print("curr_time:",agents[i].get_queue_first().waiting_time)
                        total_wait = total_wait +agents[i].get_queue_first().waiting_time
                        total_cust +=1
                    #agents[i].get_queue_first().server_time = agents[i].get_queue_first().server_time - 1
                    print("第%s个窗口的客人已经离开" % (i))
                else:
                    agents[i].get_queue_first().server_time = agents[i].get_queue_first().server_time - 1
                for j in range(1,agents[i].queue_size()):
                    agents[i].get_cust_info()[j].waiting_time = agents[i].get_cust_info()[j].waiting_time + 1
                    #print(agents[i].get_cust_info()[j].waiting_time)


        for i in range(agent_num):
            list = []
            for j in agents[i].get_cust_info():
                list.append(j.server_time)
            print("第%s个窗口的目前排队状态：%s" % (i, list))
        print("————————————————第%s时刻结束————————————————" % (now))
    print(total_wait/total_cust,total_wait,total_cust)


def single_queue(queue, agent_num, new_customer_come):
    total_time = 0
    agent = np.zeros(agent_num)
    waiting_time_all = np.zeros(queue.shape[0])
    queue_len = 0
    sum_wait = 0
    # queue simulation
    while len(queue) != 0 and total_time <= 500:
        if total_time % new_customer_come == 0:
            queue = np.append(queue, random.randint(1, 15))
            waiting_time_all = np.append(waiting_time_all, 0)
        for j in range(agent_num):
            if agent[j] == 0:
                #print(len(queue))
                agent[j] = queue[0]
                # print("before:",queue.shape[0])
                queue = np.delete(queue, 0)
                sum_wait = sum_wait + waiting_time_all[0]
                waiting_time_all = np.delete(waiting_time_all, 0)
                queue_len +=1
                # print("after:", queue.shape[0])
                # print("agent:",agent)

        for z in range(agent_num):
            if agent[z] > 0:
                # print("before:", agent)
                agent[z] -= 1
                # print("after:", agent.shape[0])
        total_time += 1
        # print("hi",waiting_time_all +1)
        waiting_time_all = waiting_time_all + 1
    print(agent.sum())
    print(total_time)

    return total_time , sum_wait / queue_len,sum_wait,queue_len


def multiple_queue(total_cu, agent_num):
    total_time = 0
    agent = np.zeros(agent_num)
    queue = np.zeros((agent_num, total_cu / agent_num))
    for i in range(agent_num):
        for j in range(queue[i].shape[0]):
            queue[i][j] = random.randint(1, 15)

    for z in range(agent_num):
        if agent[z] == 0:
            agent[z] = queue[z][0]
            queue = np.delete(queue[z], 0)

    for z in range(agent_num):
        if agent[z] > 0:
            # print("before:", agent)
            agent[z] -= 1
            # print("after:", agent.shape[0])
    total_time += 1

    return total_time



if __name__ == '__main__':
    length_queue = 10
    # the original queue
    queue_ini = np.zeros(length_queue)
    for i in range(length_queue):
        queue_ini[i] = random.randint(1, 15)
    queue = copy.deepcopy(queue_ini)

    new_customer_come = 2  # the time for a new customer to come
    # print(queue)
    # queue = np.append(queue,random.randint(1, 15))
    # print(queue)
    # print("time")
    # single queue for the system


    # multi queue
    agent_num = 4
    cu_per_q = int(length_queue / agent_num)
    multi = np.zeros((agent_num, cu_per_q))
    last_cu = length_queue % agent_num
    for i in range(3):
        for j in range(multi[i].shape[0]):
            multi[i][j] = random.randint(1, 15)
    # multi[2] = np.append(multi[0],random.randint(1, 15))

    print(multi)
    print(np.delete(multi[0], 0))
    queue = copy.deepcopy(queue_ini)
    multi_que(3, 500,queue,new_customer_come)

    single = single_queue(queue, 3, new_customer_come)
    print("time:", single)
    pass
