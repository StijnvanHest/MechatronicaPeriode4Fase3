#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_flexbe_states.get_object_pose import GetObjectPoseState
from flexbe_states.wait_state import WaitState
from ariac_flexbe_states.compute_grasp_part_offset_ariac_state import ComputeGraspPartOffsetAriacState
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_states.vacuum_gripper_control_state import VacuumGripperControlState
from ariac_flexbe_states.Check_Gripper_attached import CheckGripperattached
from ariac_flexbe_states.message_state import MessageState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jun 01 2020
@author: Anne van Oirschot
'''
class PlaceOnAgv_LastProductSM(Behavior):
	'''
	Product plaatsen op de juiste AGV
	'''


	def __init__(self):
		super(PlaceOnAgv_LastProductSM, self).__init__()
		self.name = 'PlaceOnAgv_LastProduct'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:860 y:686, x:845 y:354
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['agv_id', 'part_pose_right', 'part_pose_left'])
		_state_machine.userdata.agv_id = ''
		_state_machine.userdata.agv1 = 'agv1'
		_state_machine.userdata.agv2 = 'agv2'
		_state_machine.userdata.Gantry_AGV1_right = 'Gantry_AGV1Right'
		_state_machine.userdata.move_group_right = 'Right_Arm'
		_state_machine.userdata.move_group_prefix = '/ariac/gantry'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.move_group_gantry = 'Gantry'
		_state_machine.userdata.PreGrasp_rightArm = 'Right_AGV'
		_state_machine.userdata.PreGrasp_leftArm = 'Left_AGV'
		_state_machine.userdata.tool_link_right = 'right_ee_link'
		_state_machine.userdata.tool_link_left = 'left_ee_link'
		_state_machine.userdata.offset = 0.115
		_state_machine.userdata.part_pose_right = ''
		_state_machine.userdata.rotation = 0
		_state_machine.userdata.part_pose_left = ''
		_state_machine.userdata.arm_right = 'right_arm'
		_state_machine.userdata.arm_left = 'left_arm'
		_state_machine.userdata.Gantry_AGV1_left = 'Gantry_AGV1Left'
		_state_machine.userdata.move_group_left = 'Left_Arm'
		_state_machine.userdata.gantry_home = 'Gantry_Home'
		_state_machine.userdata.Home_right_arm = 'Right_PreGrasp'
		_state_machine.userdata.Home_left_arm = 'Left_PreGrasp'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:31 y:18
			OperatableStateMachine.add('Gantry_Home',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'AGV1', 'planning_failed': 'Retry', 'control_failed': 'Retry', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'gantry_home', 'move_group': 'move_group_gantry', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:24 y:608
			OperatableStateMachine.add('AGV2',
										EqualState(),
										transitions={'true': 'GetAgv2Pose', 'false': 'failed'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'agv_id', 'value_b': 'agv2'})

			# x:254 y:615
			OperatableStateMachine.add('GetAgv2Pose',
										GetObjectPoseState(object_frame='kit_tray_2', ref_frame='Gantry'),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'agv_pose'})

			# x:202 y:85
			OperatableStateMachine.add('GetAgv1Pose',
										GetObjectPoseState(object_frame='kit_tray_1', ref_frame='world'),
										transitions={'continue': 'PreDropTrayGantryRight', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'agv_pose'})

			# x:351 y:86
			OperatableStateMachine.add('PreDropTrayGantryRight',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'PreDropTrayRightArm', 'planning_failed': 'Retry_1', 'control_failed': 'Retry_1', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'Gantry_AGV1_right', 'move_group': 'move_group_gantry', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:378 y:4
			OperatableStateMachine.add('Retry_1',
										WaitState(wait_time=3),
										transitions={'done': 'PreDropTrayGantryRight'},
										autonomy={'done': Autonomy.Off})

			# x:531 y:89
			OperatableStateMachine.add('PreDropTrayRightArm',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'ComputeDropPartPose', 'planning_failed': 'Retry_2', 'control_failed': 'Retry_2', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'PreGrasp_rightArm', 'move_group': 'move_group_right', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:553 y:6
			OperatableStateMachine.add('Retry_2',
										WaitState(wait_time=3),
										transitions={'done': 'PreDropTrayRightArm'},
										autonomy={'done': Autonomy.Off})

			# x:690 y:92
			OperatableStateMachine.add('ComputeDropPartPose',
										ComputeGraspPartOffsetAriacState(joint_names=['right_shoulder_pan_joint', 'right_shoulder_lift_joint', 'right_elbow_joint', 'right_wrist_1_joint', 'right_wrist_2_joint', 'right_wrist_3_joint']),
										transitions={'continue': 'MoveToDrop', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group_right', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_link_right', 'pose': 'agv_pose', 'offset': 'offset', 'rotation': 'rotation', 'part_pose': 'part_pose_right', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:902 y:89
			OperatableStateMachine.add('MoveToDrop',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'GripperOff', 'planning_failed': 'Retry_3', 'control_failed': 'Retry_3'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_group_right', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:933 y:10
			OperatableStateMachine.add('Retry_3',
										WaitState(wait_time=3),
										transitions={'done': 'MoveToDrop'},
										autonomy={'done': Autonomy.Off})

			# x:1086 y:86
			OperatableStateMachine.add('GripperOff',
										VacuumGripperControlState(enable=False),
										transitions={'continue': 'PreDropTrayRightArm_2', 'failed': 'MoveToDrop', 'invalid_arm_id': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_arm_id': Autonomy.Off},
										remapping={'arm_id': 'arm_right'})

			# x:1267 y:87
			OperatableStateMachine.add('PreDropTrayRightArm_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'PreDropTrayRightArm_2_2', 'planning_failed': 'Retry_4', 'control_failed': 'Retry_4', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'PreGrasp_rightArm', 'move_group': 'move_group_right', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1291 y:8
			OperatableStateMachine.add('Retry_4',
										WaitState(wait_time=3),
										transitions={'done': 'PreDropTrayRightArm_2'},
										autonomy={'done': Autonomy.Off})

			# x:1551 y:189
			OperatableStateMachine.add('PreDropTrayGantryLeft',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'PreDropTrayLeftArm', 'planning_failed': 'Retry_5', 'control_failed': 'Retry_5', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'Gantry_AGV1_left', 'move_group': 'move_group_gantry', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1555 y:266
			OperatableStateMachine.add('PreDropTrayLeftArm',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'ComputeDropPartPose_2', 'planning_failed': 'Retry_6', 'control_failed': 'Retry_6', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'PreGrasp_leftArm', 'move_group': 'move_group_left', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1518 y:345
			OperatableStateMachine.add('ComputeDropPartPose_2',
										ComputeGraspPartOffsetAriacState(joint_names=['left_shoulder_pan_joint', 'left_shoulder_lift_joint', 'left_elbow_joint', 'left_wrist_1_joint', 'left_wrist_2_joint', 'left_wrist_3_joint']),
										transitions={'continue': 'MoveToDrop_2', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group_left', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_link_left', 'pose': 'agv_pose', 'offset': 'offset', 'rotation': 'rotation', 'part_pose': 'part_pose_left', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1519 y:419
			OperatableStateMachine.add('MoveToDrop_2',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'GripperOff_2', 'planning_failed': 'Retry_7', 'control_failed': 'Retry_7'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_group_left', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1523 y:510
			OperatableStateMachine.add('GripperOff_2',
										VacuumGripperControlState(enable=False),
										transitions={'continue': 'PreDropTrayLeftArm_2', 'failed': 'MoveToDrop_2', 'invalid_arm_id': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_arm_id': Autonomy.Off},
										remapping={'arm_id': 'arm_left'})

			# x:1542 y:606
			OperatableStateMachine.add('PreDropTrayLeftArm_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'PreDropTrayLeftArm_2_2_2', 'planning_failed': 'Retry_8', 'control_failed': 'Retry_8', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'PreGrasp_leftArm', 'move_group': 'move_group_left', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1719 y:183
			OperatableStateMachine.add('Retry_5',
										WaitState(wait_time=3),
										transitions={'done': 'PreDropTrayGantryLeft'},
										autonomy={'done': Autonomy.Off})

			# x:1720 y:264
			OperatableStateMachine.add('Retry_6',
										WaitState(wait_time=3),
										transitions={'done': 'PreDropTrayLeftArm'},
										autonomy={'done': Autonomy.Off})

			# x:1715 y:416
			OperatableStateMachine.add('Retry_7',
										WaitState(wait_time=3),
										transitions={'done': 'MoveToDrop_2'},
										autonomy={'done': Autonomy.Off})

			# x:1717 y:597
			OperatableStateMachine.add('Retry_8',
										WaitState(wait_time=3),
										transitions={'done': 'PreDropTrayLeftArm_2'},
										autonomy={'done': Autonomy.Off})

			# x:207 y:9
			OperatableStateMachine.add('Retry',
										WaitState(wait_time=3),
										transitions={'done': 'Gantry_Home'},
										autonomy={'done': Autonomy.Off})

			# x:25 y:157
			OperatableStateMachine.add('AGV1',
										EqualState(),
										transitions={'true': 'AttachedRight', 'false': 'AGV2'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'agv_id', 'value_b': 'agv1'})

			# x:1462 y:93
			OperatableStateMachine.add('PreDropTrayRightArm_2_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'Attached_Left', 'planning_failed': 'Retry_9_2', 'control_failed': 'Retry_9_2', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'Home_right_arm', 'move_group': 'move_group_right', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1524 y:697
			OperatableStateMachine.add('PreDropTrayLeftArm_2_2_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'Home_Gantry', 'planning_failed': 'Retry_9', 'control_failed': 'Retry_9', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'Home_left_arm', 'move_group': 'move_group_left', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1720 y:705
			OperatableStateMachine.add('Retry_9',
										WaitState(wait_time=3),
										transitions={'done': 'PreDropTrayLeftArm_2_2_2'},
										autonomy={'done': Autonomy.Off})

			# x:1495 y:6
			OperatableStateMachine.add('Retry_9_2',
										WaitState(wait_time=3),
										transitions={'done': 'PreDropTrayRightArm_2_2'},
										autonomy={'done': Autonomy.Off})

			# x:1124 y:654
			OperatableStateMachine.add('Home_Gantry',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'Retry_9_3', 'control_failed': 'Retry_9_3', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'gantry_home', 'move_group': 'move_group_gantry', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1147 y:732
			OperatableStateMachine.add('Retry_9_3',
										WaitState(wait_time=3),
										transitions={'done': 'Home_Gantry'},
										autonomy={'done': Autonomy.Off})

			# x:201 y:157
			OperatableStateMachine.add('AttachedRight',
										CheckGripperattached(),
										transitions={'True': 'TestMessagePositie1', 'False': 'Home_Gantry', 'invalid_arm_id': 'failed'},
										autonomy={'True': Autonomy.Off, 'False': Autonomy.Off, 'invalid_arm_id': Autonomy.Off},
										remapping={'arm_id': 'arm_right'})

			# x:1671 y:94
			OperatableStateMachine.add('Attached_Left',
										CheckGripperattached(),
										transitions={'True': 'PreDropTrayGantryLeft', 'False': 'Home_Gantry', 'invalid_arm_id': 'failed'},
										autonomy={'True': Autonomy.Off, 'False': Autonomy.Off, 'invalid_arm_id': Autonomy.Off},
										remapping={'arm_id': 'arm_left'})

			# x:199 y:253
			OperatableStateMachine.add('TestMessagePositie1',
										MessageState(),
										transitions={'continue': 'GetAgv1Pose'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'part_pose_right'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
