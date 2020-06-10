class Factory:

    CLASS = None

    #####
    ### factory method
    #####
    def get_modal(modalName: str):
        # correct
        if Factory.CLASS == None:
            Factory.CLASS = Factory
        # retrieve the list of static methods
        staticmethods = [method for method in dir(Factory.CLASS) if 'Modal' in method]
        # retrieve the targeted modal
        if modalName in staticmethods: return getattr(Factory.CLASS, modalName)
        # otherwise return None
        return None