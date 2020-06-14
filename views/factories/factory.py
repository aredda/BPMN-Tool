class Factory:

    CLASS = None

    #####
    ### factory method
    #####
    def get_instance(instanceName: str):
        # correct
        if Factory.CLASS == None:
            Factory.CLASS = Factory
        # retrieve the list of static methods
        staticmethods = [method for method in dir(Factory.CLASS) if '__' not in method]
        # retrieve the targeted instance
        if instanceName in staticmethods: return getattr(Factory.CLASS, instanceName)
        # otherwise return None
        return None