import json

class StateMachine:

    def __init__(self):
        self.handlers = {}
        self.startState = None
        self.endStates = []
        self.detailList = []

    def add_state(self,name,handler,end_state = 0):
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)


    def set_start(self,name):
        self.startState = name.upper()

    def process(self,cargo):
        originCargo = cargo
        self.detailList = []
        try:
            handler = self.handlers[self.startState]
        except:
            raise Exception("must call .set_start() before .run()")
        if not self.endStates:
            raise Exception("at least one state must be an end_state")

        verified = True

        while True:
            try:
                (newState,cargo,returnList) = handler(cargo,self.detailList)
                print(newState,cargo,returnList)
                if newState.upper() in self.endStates:
                    break
                else:
                    handler = self.handlers[newState.upper()]

            except Exception as e:
                import traceback
                traceback.print_exc()
                print("Error Parse:",originCargo,"handler:",handler)
                verified = False
                break

        returnDict = {}
        if verified:
            for part in self.detailList:
                state,value = part
                if state not in returnDict:
                    returnDict[state] = []
                returnDict[state].append(value)

        print(originCargo + ": " + json.dumps(returnDict,ensure_ascii=False))
