#!/usr/bin/env python
import roslib;
#roslib.load_manifest('smach_MonitorState_example')
import rospy
import smach
import smach_ros

from std_msgs.msg import Empty

class bar(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['bar_succeeded'])
    def execute(self, userdata):
        rospy.sleep(3.0)
        return 'bar_succeeded'

def monitor_cb(ud, msg):
    return False

def main():
    rospy.init_node("monitor_example")

    sm = smach.StateMachine(outcomes=['DONE'])
    with sm:
        #MonitorState:
        #def __init__(self, topic, msg_type, cond_cb, max_checks=-1)
        smach.StateMachine.add('FOO', smach_ros.MonitorState("/sm_reset", Empty, monitor_cb),
            transitions={'invalid':'BAR', 'valid':'BAR', 'preempted':'FOO'})
        smach.StateMachine.add('BAR',bar(), transitions={'bar_succeeded':'DONE'})

    print("Starting introspection server")
    sis = smach_ros.IntrospectionServer('smach_server', sm, '/SM_ROOT')
    print("Starting sis")
    sis.start()
    print("Executing state machine")
    sm.execute()
    print("Spinning")
    rospy.spin()
    print("Stopping sis")
    sis.stop()

if __name__=="__main__":
    main()