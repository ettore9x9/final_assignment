#! /usr/bin/env python

import rospy
import actionlib
import curses

from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

class autonomous_driving():

    def __init__(self, stdscr):

        self.goal_counter = 0
        self.feedback_counter = 0
        self.is_active = False
        self.stdscr = stdscr

        self.title = R"""    c to cancel goal
    n to insert a new goal
"""

        # Creates the MoveBaseActionClient
        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)

    def active_cb(self):
        self.stdscr.addstr(17, 38, "Action Server is processing goal n "+str(self.goal_counter+1)+" ... ")
        self.stdscr.refresh()


    def feedback_cb(self, feedback):
        self.feedback_counter += 1
        self.stdscr.addstr(18, 38, "Feedback for goal n "+str(self.goal_counter+1)+" received.          ")
        self.stdscr.addstr(18, 68 + self.feedback_counter % 10, ">")
        self.stdscr.refresh()


    def done_cb(self, status, result):
        self.goal_counter += 1

        if status == 2:
            self.stdscr.addstr(19, 38, "Goal n "+str(self.goal_counter)+" received a cancel request.       ")
            self.stdscr.refresh()
            return

        if status == 3:
            self.stdscr.addstr(19, 38, "Goal n "+str(self.goal_counter)+" reached.                         ")
            self.stdscr.refresh()
            return

        if status == 4:
            self.stdscr.addstr(19, 38, "Goal n "+str(self.goal_counter)+" was aborted.                     ")
            self.stdscr.refresh()
            return

        if status == 5:
            self.stdscr.addstr(19, 38, "Goal n "+str(self.goal_counter)+" has been rejected.               ")
            self.stdscr.refresh()
            return

        if status == 8:
            self.stdscr.addstr(19, 38, "Goal n "+str(self.goal_counter)+" received a cancel request.       ")
            self.stdscr.refresh()
            return

   
    def reach_goal(self, x, y):

        # Waits until the action server has started up and started
        # listening for goals.
        self.is_active = True

        self.client.wait_for_server()

        self.stdscr.addstr(15, 0, self.title)

        # Creates a goal to send to the action server.
        goal = MoveBaseGoal()

        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.orientation.w = 1
        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y
   
        # Sends the goal to the action server.
        self.client.send_goal(goal, self.done_cb, self.active_cb, self.feedback_cb)

    def cancel_goal(self):
        self.is_active = False
        clear_screen()
        self.client.cancel_goal()