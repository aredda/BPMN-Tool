from tunits.TestUnit_Event import run as event_test
from tunits.TestUnit_Task import run as task_test
from tunits.TestUnit_Gateway import run as gateway_test
from tunits.TestUnit_Artifacts import run as artifact_test
from tunits.TestUnit_DefaultSeq import run as seq_test
from tunits.TestUnit_Associations import run as assoc_test
from tunits.TestUnit_Process import run as process_test
from tunits.TestUnit_caseOne import run as case1_test
from tunits.TestUnit_caseTwo import run as case2_test
from tunits.TestUnit_caseThree import run as case3_test
from tunits.TestUnit_caseFour import run as case4_test
from tunits.TestUnit_caseFive import run as case5_test
from tunits.TestUnit_Definitions import run as def_test
from tunits.TestUnit_Definitions2 import run as def2_test
from tunits.TU_Window import run as win_test
from tunits.TU_MultipleWindow import run as mulwin_test
from views.windows.homewindow import HomeWindow
from views.windows.profilewindow import ProfileWindow
from helpers.windowmanager import WindowManager
# from tunits.TestUnit_Entities import run as entity_test
# from tunits.TestUnit_imageutility import run as imageutility_test
# from tunits.TestUnit_xmlutility import run as xmlutility_test

# Event Test Unit
# event_test()

# Task Test Unit
# task_test()

# Gateway Test Unit
# gateway_test()

# Artifacts Test Unit
# artifact_test()

# Default Sequence Flow Test
# seq_test()

# Data Assoc Test
# assoc_test()

# Process Test
# process_test()

# case One test
# case1_test()

# case Two test
# case2_test()

# case Three test
# case3_test()

# case Four test
# case4_test()

# case Five test
# case5_test()

# Definitions Test
# def_test()

# Definitions Test
# def2_test()

manager = WindowManager()
manager.run_tag('home')
manager.root.mainloop()

# mulwin_test()
