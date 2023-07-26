class Prisoner():

    prisonerid = 0
    listofpapertaken = []
    numberofboxesopened=0
    PassorFail=False

    def update_addpapertolist(self, numonpaper):
        self.listofpapertaken.append(int(numonpaper))
        return

    def check_numberonlatestpapertaken(self):
        if(self.listofpapertaken[-1] == self.prisonerid):
            self.PassorFail=True
        return

    def update_openbox(self, boxnumonpaper):
        self.numberofboxesopened+=1
        self.update_addpapertolist(boxnumonpaper)
        self.check_numberonlatestpapertaken()
        return

    def resetallvalues_toreuse(self):
        self.listofpapertaken=[]
        self.numberofboxesopened=0
        self.PassorFail=False

    def __init__(self, idgiven):
        print('New Prisoner Created')
        self.prisonerid = idgiven
        print("This Prisoner's ID is #",self.prisonerid)

    def __del__(self):
        print('Prisoner completed challenge')

class Boxwithpaper():

    numberinbox=0

    def update_numberinbox(self, papernumber):
        self.numberinbox = papernumber
        return

    def __init__(self):
        print('New Box Created')

    def __del__(self):
        print('Box sreved its purpose')

def generatenumberonpapertoputinbox():
    pass

def check_solutionpassorfail(prisonerlist):
    #Pass by default
    #if anyone fails all fails
    #returns 1 if pass to add to count of pass, 0 if fail
    resaftercheck=True
    for prisonee in prisonerlist:
        if(prisonee.PassorFail==False):
            resaftercheck=False
    count = 1 if resaftercheck else 0
    return count 

def resultofstrat():
    pass

#strats will return probability of success

#try first five go for odd numbers, last five go for even numbers
def strat1():
    pass

#try inverse strat 1
def strat2():
    pass

#try if your number is odd or even go for odd or even
def strat3():
    pass

#try inverse strat 3
def strat4():
    pass

#try your own number then pointer style solution
def strat5():
    pass



def main():
    print('Start')
    prisonerlist=[Prisoner(i) for i in range(1,11)]
    boxlist=[Boxwithpaper() for i in range(1,11)]

    a= check_solutionpassorfail(prisonerlist)
    print(a)
    print('End')
    return


if __name__ == "__main__":
    main()

