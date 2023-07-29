import json
import os
from multiprocessing import Process 
import time

class Prisoner():
    #prisonerid = None
    #listofpapertaken = []
    #numberofboxesopened=0
    #PassorFail=False

    def update_addpapertolist(self, numonpaper):
        self.listofpapertaken.append(numonpaper)
        return

    def check_numberonlatestpapertaken(self):
        if(str(self.listofpapertaken[-1]) == self.prisonerid):
            #print('Match!')
            self.PassorFail=True
        if(self.numberofboxesopened==5 and self.listofpapertaken[-1] != self.prisonerid):
            self.PassorFail=False
        return

    def update_openbox(self, boxnumonpaper):
        self.numberofboxesopened+=1
        self.update_addpapertolist(str(boxnumonpaper))
        self.check_numberonlatestpapertaken()
        return

    def resetallvalues_toreuse(self):
        self.listofpapertaken=[]
        self.numberofboxesopened=0
        self.PassorFail=False

    def __init__(self, prisonerid):
        #print('New Prisoner Created')
        self.prisonerid = str(prisonerid)
        self.listofpapertaken = []
        self.numberofboxesopened=0
        self.PassorFail=False
        print("This Prisoner's ID is #",self.prisonerid)

    def __del__(self):
        print('Prisoner completed challenge')

class Boxwithpaper():
    

    def update_numberinbox(self, papernumber):
        self.numberinbox = str(papernumber)
        return

    def resetallvalues_toreuse(self):
        self.numberinbox=None

    def __init__(self, boxid):
        #print('New Box Created')
        self.boxid = str(boxid)
        self.numberinbox=None
        print("This Box's ID is #",self.boxid)

    def __del__(self):
        print('Box sreved its purpose')

#Test Case Generation and storage/retrieval

# nums=[0,1,2,3,4,5,6,7,8,9]
# https://stackoverflow.com/questions/6284396/permutations-with-unique-values see MiniQuark solution to permutation
def generatenumberonpapertoputinbox(nums):
    if(len(nums)==1):
        yield (nums[0],)
    unique_set = set(nums)
    for first_num in unique_set:
        remaining_num = list(nums)
        remaining_num.remove(first_num)
        for j in generatenumberonpapertoputinbox(remaining_num):
            yield (first_num,) + j

def storetestcases(l1):
    filename='testcases.json'
    with open(filename, 'w') as outfile:
        json.dump(l1, outfile, sort_keys=False, indent=4, ensure_ascii=False)
    return

#works, contains 10! = 3628800 cases
def generate_and_store_testacses_returntestcaselist():
    filename='testcases.json'
    cwd = os.getcwd()
    full_path = os.path.join(cwd, filename)
    if(os.path.isfile(full_path)==True):
        print('testcase exist, loading into list')
        f = open(full_path)
        testcases = list(json.load(f))
        return testcases
    else:
        print('testcase does not exist, generating')
        nums=[0,1,2,3,4,5,6,7,8,9]
        l1 = list(generatenumberonpapertoputinbox(nums))
        storetestcases(l1)
        return l1


# Different Solutions
#strats will return probability of success

#try first five go for odd numbers, last five go for even numbers
#0 1 2 3 4 5 6 7 8 9 means 0 is odd 1 is even lol
def strat1(p_list, b_list, testcases):
    print('Starting Strat 1')
    successcount=0
    #load each list of values
    for scenario in testcases:
        #load values into box
        for ind, val in enumerate(scenario):
            b_list[ind].update_numberinbox(val)
            #print("box {} has # {}".format(ind,val))

        #first five opens all odd boxes
        for _ in range(0,int(len(p_list)/2)):
            #should open 0,2,4,6,8 which are odd boxes
            for j in range(0,len(b_list),2):
                if(p_list[_].PassorFail==True):
                    pass
                else:
                    p_list[_].update_openbox(b_list[j].numberinbox)
                    #print('prisoner #{} opened box number#{} \ncontains: number #{}'.format(_,j,b_list[j].numberinbox))
        #next five opens all even boxes
        for _ in range(5,len(p_list)):
            #opens 1,3,5,7,9
            for j in range(1,len(b_list),2):
                if(p_list[_].PassorFail==True):
                    pass
                else:
                    p_list[_].update_openbox(b_list[j].numberinbox)
                    #print('prisoner #{} opened box number#{} \ncontains: number #{}'.format(_,j,b_list[j].numberinbox))
        #reset values in obj
        successcount+=check_solutionpassorfail(p_list)

        for i in range(len(p_list)):
            p_list[i].resetallvalues_toreuse()
            b_list[i].resetallvalues_toreuse()
        #print(idex)

    a = resultofstrat(successcount)
    with open('strat1 result.txt', 'w') as f:
        f.write(str(a))
    print('Ending Strat 1')
    return




#try inverse strat 1
def strat2(p_list, b_list, testcases):
    print('Starting Strat 2')
    successcount=0
    #load each list of values
    for scenario in testcases:
        #load values into box
        for ind, val in enumerate(scenario):
            b_list[ind].update_numberinbox(val)
            #print("box {} has # {}".format(ind,val))

        #first five opens all even boxes
        for _ in range(0,int(len(p_list)/2)):
            #should open 1,3,5,7,9 which are even boxes 
            for i in range(1,len(b_list),2):
                if(p_list[_].PassorFail==True):
                    pass
                else:
                    p_list[_].update_openbox(b_list[i].numberinbox)
                #print('Prisoner {} opened number {}'.format(_,str(i)))
            
        #last five opens all odd boxes
        for _ in range(5,len(p_list)):
            #opens 0,2,4,6,8
            for i in range(0,len(p_list),2):
                if(p_list[_].PassorFail==True):
                    pass
                else:
                    p_list[_].update_openbox(b_list[i].numberinbox)
                #print('Prisoner {} opened number {}'.format(_,str(i)))
        #add to statistic of pass, adds 0 if fail
        successcount+=check_solutionpassorfail(p_list)
        #reset all prisoners for next loop, only needed for prisoners, box vals can be redefined
        for i in range(len(p_list)):
            p_list[i].resetallvalues_toreuse()
            b_list[i].resetallvalues_toreuse()
        #print(idex)

    a = resultofstrat(successcount)
    with open('strat2 result.txt', 'w') as f:
        f.write(str(a))
    print('Starting Strat 2')
    return

#try if your number is odd or even go for odd or even
def strat3(p_list, b_list, testcases):
    print('Starting Strat 3')
    successcount=0
    #load each list of values
    for scenario in testcases:
        #load values into box
        for ind, val in enumerate(scenario):
            b_list[ind].update_numberinbox(val)

        #odd people open odd boxes 0 2 4 6 8
        for _ in range(0,len(p_list),2):
            #should open 0,2,4,6,8 which are odd boxes
            for j in range(0,len(b_list),2):
                if(p_list[_].PassorFail==True):
                    pass
                else:
                    p_list[_].update_openbox(b_list[j].numberinbox)
                    #print('prisoner #{} opened box number#{} \ncontains: number #{}'.format(_,j,b_list[j].numberinbox))

        #even opens all even boxes 1 3 5 7 9
        for _ in range(1,len(p_list),2):
            #opens 1,3,5,7,9
            for j in range(1,len(b_list),2):
                if(p_list[_].PassorFail==True):
                    pass
                else:
                    p_list[_].update_openbox(b_list[j].numberinbox)
                    #print('prisoner #{} opened box number#{} \ncontains: number #{}'.format(_,j,b_list[j].numberinbox))
        #reset values in obj
        successcount+=check_solutionpassorfail(p_list)

        for i in range(len(p_list)):
            p_list[i].resetallvalues_toreuse()
            b_list[i].resetallvalues_toreuse()
        #print(idex)

    a = resultofstrat(successcount)
    with open('strat3 result.txt', 'w') as f:
        f.write(str(a))
    print('Ending Strat 3')
    return

#try inverse strat 3
def strat4(p_list, b_list, testcases):
    print('Starting Strat 4')
    successcount=0
    #load each list of values
    for scenario in testcases:
        #load values into box
        for ind, val in enumerate(scenario):
            b_list[ind].update_numberinbox(val)

        #odd people open even boxes 0 2 4 6 8
        for _ in range(0,len(p_list),2):
            #should open 1,3,5,7,9 which are odd boxes
            for j in range(1,len(b_list),2):
                if(p_list[_].PassorFail==True):
                    pass
                else:
                    p_list[_].update_openbox(b_list[j].numberinbox)
                    #print('prisoner #{} opened box number#{} \ncontains: number #{}'.format(_,j,b_list[j].numberinbox))

        #even opens all even boxes 1 3 5 7 9
        for _ in range(1,len(p_list),2):
            #opens  0,2,4,6,8
            for j in range(0,len(b_list),2):
                if(p_list[_].PassorFail==True):
                    pass
                else:
                    p_list[_].update_openbox(b_list[j].numberinbox)
                    #print('prisoner #{} opened box number#{} \ncontains: number #{}'.format(_,j,b_list[j].numberinbox))
        #reset values in obj
        successcount+=check_solutionpassorfail(p_list)

        for i in range(len(p_list)):
            p_list[i].resetallvalues_toreuse()
            b_list[i].resetallvalues_toreuse()
        #print(idex)

    a = resultofstrat(successcount)
    with open('strat4 result.txt', 'w') as f:
        f.write(str(a))
    print('Ending Strat 4')
    return

#try your own number then pointer style solution
def strat5(prisonerlist, boxlist, testcase):
    print('Starting Strat 5')
    successcount=0
    #load each list of values
    for scenario in testcase:
        #load values into box
        for ind, val in enumerate(scenario):
            boxlist[ind].update_numberinbox(val)

        #loop through every prisoner obj
        for _ in range(len(prisonerlist)):
            #check number in own box, if same means a win, else go to next box
            numinboxpoint=boxlist[_].numberinbox
            prisonerlist[_].update_openbox(numinboxpoint)
            # 4 boxes left
            for i in range(4):
                if(prisonerlist[_].PassorFail==True):
                    break
                else:
                    numinboxpoint = boxlist[int(numinboxpoint)].numberinbox
                    prisonerlist[_].update_openbox(numinboxpoint)

        successcount+=check_solutionpassorfail(prisonerlist)

        for i in range(len(prisonerlist)):
            prisonerlist[i].resetallvalues_toreuse()
            boxlist[i].resetallvalues_toreuse()
        #print(idex)

    a = resultofstrat(successcount)
    with open('strat5 result.txt', 'w') as f:
        f.write(str(a))
    print('Ending Strat 5')
    return

#Evaluation for how effective solution is

#Evaluates after each individual testcase, then reset values and go next
def check_solutionpassorfail(prisonerlist):
    for i in range(len(prisonerlist)):
        #one fails all fails
        if(prisonerlist[i].PassorFail==False):
            return 0
        else:
            pass

    #if loop finishes means all pass
    else:
        return 1

def resultofstrat(success):
    res=success/3628800
    resper=res*100
    msg = 'Success rate\n{} number of cases passed\n{} probabilty of success ({})'.format(success,res,resper)
    print(msg)
    return msg



def main():
    starttime=time.process_time()
    print('Start')
    prisonerlist=[Prisoner(i) for i in range(10)]
    boxlist=[Boxwithpaper(i) for i in range(10)]
    testcase = generate_and_store_testacses_returntestcaselist()
    p1=Process(target=strat1, args=(prisonerlist,boxlist,testcase))
    p2=Process(target=strat2, args=(prisonerlist,boxlist,testcase))
    p3=Process(target=strat3, args=(prisonerlist,boxlist,testcase))
    p4=Process(target=strat4, args=(prisonerlist,boxlist,testcase))
    p5=Process(target=strat5, args=(prisonerlist,boxlist,testcase))
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
    print(time.process_time()-starttime)
    print('End')
    return


if __name__ == "__main__":
    main()

