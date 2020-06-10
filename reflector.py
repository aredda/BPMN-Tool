class A:

    def hello():
        print ('hello')

# print ([x for x in dir(A) if str(x).startswith('__') == False])

from views.factories.formmodalfactory import FormModalFactory

print (FormModalFactory.get_modal('InviteModal'))