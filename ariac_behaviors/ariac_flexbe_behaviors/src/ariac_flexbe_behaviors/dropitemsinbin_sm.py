#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_flexbe_states.get_object_pose import GetObjectPoseState
from ariac_flexbe_states.Check_Gripper_attached import CheckGripperattached
from ariac_flexbe_states.vacuum_gripper_control_state import VacuumGripperControlState
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_behaviors.startup_sm import StartUPSM
from ariac_support_flexbe_states.replace_state import ReplaceState
from ariac_flexbe_states.Compute_belt_drop import ComputeBeltDrop
from ariac_support_flexbe_states.add_numeric_state import AddNumericState
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jun 01 2020
@author: Stijn van Hest
'''
class DropItemsInBINSM(Behavior):
	'''
	This behavoir drops both items in the bins
	'''


	def __init__(self):
		super(DropItemsInBINSM, self).__init__()
		self.name = 'DropItemsInBIN'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(StartUPSM, 'StartUP')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:2425 y:70, x:1043 y:385, x:2422 y:460, x:1682 y:414
		_state_machine = OperatableStateMachine(outcomes=['Next arm', 'failed', 'BothArmsEmpty', 'BinVol'], input_keys=['USEarmID', 'GantryLocation', 'RightArmItem', 'LeftArmItem'], output_keys=['RightArmItem', 'LeftArmItem'])
		_state_machine.userdata.arm_idL = 'left_arm'
		_state_machine.userdata.arm_idR = 'right_arm'
		_state_machine.userdata.USEarmID = ''
		_state_machine.userdata.move_groupR = 'Right_Arm'
		_state_machine.userdata.move_groupL = 'Left_Arm'
		_state_machine.userdata.tool_linkL = 'left_ee_link'
		_state_machine.userdata.tool_linkR = 'right_ee_link'
		_state_machine.userdata.DropPose = []
		_state_machine.userdata.offsetXPiston = 0
		_state_machine.userdata.offsetPiston = 0
		_state_machine.userdata.offsetYPiston = 0
		_state_machine.userdata.rotation = 0
		_state_machine.userdata.move_group_prefix = '/ariac/gantry'
		_state_machine.userdata.PistonOffset = 0.22
		_state_machine.userdata.GasketOffset = 0.15
		_state_machine.userdata.offsetGasket = 0
		_state_machine.userdata.offsetXGasket = -0.1
		_state_machine.userdata.offsetYGasket = 0
		_state_machine.userdata.GasketLocation = 'GasketLoc'
		_state_machine.userdata.PistonLocation = 'PistonLoc'
		_state_machine.userdata.GantryLocation = ''
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.Niks = 'Niks'
		_state_machine.userdata.RightArmItem = ''
		_state_machine.userdata.LeftArmItem = ''
		_state_machine.userdata.SideXoffset = 0
		_state_machine.userdata.SideYoffset = 0
		_state_machine.userdata.SideZoffset = 0
		_state_machine.userdata.GasketRow = 0
		_state_machine.userdata.PistonRow = 0
		_state_machine.userdata.RowTarget = 4
		_state_machine.userdata.GasketRound = 0
		_state_machine.userdata.PistonRound = 0
		_state_machine.userdata.RoundTarget = 12
		_state_machine.userdata.Zero_Value = 0
		_state_machine.userdata.One_value = 1
		_state_machine.userdata.move_groupG = 'Gantry'
		_state_machine.userdata.config_nameSH3 = 'Gantry_SafeHall3'
		_state_machine.userdata.robot_name = ''

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:46 y:59
			OperatableStateMachine.add('GasketLocation',
										EqualState(),
										transitions={'true': 'GetGasketBinPosition', 'false': 'PistonLocation'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'GasketLocation', 'value_b': 'GantryLocation'})

			# x:229 y:59
			OperatableStateMachine.add('GetGasketBinPosition',
										GetObjectPoseState(object_frame='bin12_frame', ref_frame='world'),
										transitions={'continue': 'SetGasketBinXOffset', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'DropPose'})

			# x:212 y:697
			OperatableStateMachine.add('GetPistonBinPosition',
										GetObjectPoseState(object_frame='bin1_frame', ref_frame='world'),
										transitions={'continue': 'SetPistonBinYOffset', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'DropPose'})

			# x:2308 y:231
			OperatableStateMachine.add('checkLeftArmAttached',
										CheckGripperattached(),
										transitions={'True': 'Next arm', 'False': 'BothArmsEmpty', 'invalid_arm_id': 'failed'},
										autonomy={'True': Autonomy.Off, 'False': Autonomy.Off, 'invalid_arm_id': Autonomy.Off},
										remapping={'arm_id': 'arm_idL'})

			# x:1094 y:48
			OperatableStateMachine.add('GripperUITRechts',
										VacuumGripperControlState(enable=False),
										transitions={'continue': 'ResetRightArmItem', 'failed': 'GoToDropRight', 'invalid_arm_id': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_arm_id': Autonomy.Off},
										remapping={'arm_id': 'arm_idR'})

			# x:897 y:49
			OperatableStateMachine.add('GoToDropRight',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'GripperUITRechts', 'planning_failed': 'GripperUITRechts', 'control_failed': 'GripperUITRechts'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_groupR', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1971 y:230
			OperatableStateMachine.add('StartUP',
										self.use_behavior(StartUPSM, 'StartUP'),
										transitions={'finished': 'checkRightArmAttached', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:1280 y:44
			OperatableStateMachine.add('ResetRightArmItem',
										ReplaceState(),
										transitions={'done': 'AddX2offsetGasket'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'Niks', 'result': 'RightArmItem'})

			# x:1086 y:120
			OperatableStateMachine.add('GripperUITLinks',
										VacuumGripperControlState(enable=False),
										transitions={'continue': 'ResetLeftArmItem', 'failed': 'GoToDropLeft', 'invalid_arm_id': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_arm_id': Autonomy.Off},
										remapping={'arm_id': 'arm_idL'})

			# x:43 y:696
			OperatableStateMachine.add('PistonLocation',
										EqualState(),
										transitions={'true': 'GetPistonBinPosition', 'false': 'failed'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'PistonLocation', 'value_b': 'GantryLocation'})

			# x:896 y:116
			OperatableStateMachine.add('GoToDropLeft',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'GripperUITLinks', 'planning_failed': 'GripperUITLinks', 'control_failed': 'GripperUITLinks'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_groupL', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1263 y:123
			OperatableStateMachine.add('ResetLeftArmItem',
										ReplaceState(),
										transitions={'done': 'AddX2offsetGasket'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'Niks', 'result': 'LeftArmItem'})

			# x:2147 y:229
			OperatableStateMachine.add('checkRightArmAttached',
										CheckGripperattached(),
										transitions={'True': 'Next arm', 'False': 'checkLeftArmAttached', 'invalid_arm_id': 'failed'},
										autonomy={'True': Autonomy.Off, 'False': Autonomy.Off, 'invalid_arm_id': Autonomy.Off},
										remapping={'arm_id': 'arm_idR'})

			# x:760 y:46
			OperatableStateMachine.add('ComputeRightDrop',
										ComputeBeltDrop(joint_names=['right_shoulder_pan_joint', 'right_shoulder_lift_joint', 'right_elbow_joint', 'right_wrist_1_joint', 'right_wrist_2_joint', 'right_wrist_3_joint']),
										transitions={'continue': 'GoToDropRight', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_groupR', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_linkR', 'pose': 'DropPose', 'offset': 'SideZoffset', 'SideYoffset': 'SideYoffset', 'SideXoffset': 'SideXoffset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:759 y:123
			OperatableStateMachine.add('ComputeLeftDrop',
										ComputeBeltDrop(joint_names=['left_shoulder_pan_joint', 'left_shoulder_lift_joint', 'left_elbow_joint', 'left_wrist_1_joint', 'left_wrist_2_joint', 'left_wrist_3_joint']),
										transitions={'continue': 'GoToDropLeft', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_groupL', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_linkL', 'pose': 'DropPose', 'offset': 'SideZoffset', 'SideYoffset': 'SideYoffset', 'SideXoffset': 'SideXoffset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:410 y:12
			OperatableStateMachine.add('SetGasketBinXOffset',
										ReplaceState(),
										transitions={'done': 'SetGasketBinYOffset'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'offsetXGasket', 'result': 'SideXoffset'})

			# x:409 y:76
			OperatableStateMachine.add('SetGasketBinYOffset',
										ReplaceState(),
										transitions={'done': 'RechterARM?2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'offsetYGasket', 'result': 'SideYoffset'})

			# x:359 y:789
			OperatableStateMachine.add('SetPistonBinXOffset',
										ReplaceState(),
										transitions={'done': 'RechterARM?'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'offsetXPiston', 'result': 'SideXoffset'})

			# x:365 y:699
			OperatableStateMachine.add('SetPistonBinYOffset',
										ReplaceState(),
										transitions={'done': 'SetPistonBinXOffset'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'offsetYPiston', 'result': 'SideYoffset'})

			# x:1523 y:45
			OperatableStateMachine.add('AddX2offsetGasket',
										AddNumericState(),
										transitions={'done': 'CheckGasketRows'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'offsetXGasket', 'value_b': 'GasketOffset', 'result': 'offsetXGasket'})

			# x:1521 y:100
			OperatableStateMachine.add('CheckGasketRows',
										EqualState(),
										transitions={'true': 'ResetGasketRow', 'false': 'AddGasketRound'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'GasketRound', 'value_b': 'RowTarget'})

			# x:1519 y:160
			OperatableStateMachine.add('ResetGasketRow',
										ReplaceState(),
										transitions={'done': 'AddYoffsetGasket'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'Zero_Value', 'result': 'offsetXGasket'})

			# x:1523 y:222
			OperatableStateMachine.add('AddYoffsetGasket',
										AddNumericState(),
										transitions={'done': 'CheckGasketRound'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'GasketOffset', 'value_b': 'offsetYGasket', 'result': 'offsetYGasket'})

			# x:1699 y:46
			OperatableStateMachine.add('AddGasketRound',
										AddNumericState(),
										transitions={'done': 'CheckGasketRound'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'One_value', 'value_b': 'GasketRound', 'result': 'GasketRound'})

			# x:1698 y:112
			OperatableStateMachine.add('CheckGasketRound',
										EqualState(),
										transitions={'true': 'ResetGasketRound', 'false': 'BackToSH3'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'GasketRound', 'value_b': 'RoundTarget'})

			# x:1698 y:197
			OperatableStateMachine.add('ResetGasketRound',
										ReplaceState(),
										transitions={'done': 'BinVol'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'Zero_Value', 'result': 'offsetYGasket'})

			# x:578 y:81
			OperatableStateMachine.add('RechterARM?2',
										EqualState(),
										transitions={'true': 'ComputeRightDrop', 'false': 'ComputeLeftDrop'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'USEarmID', 'value_b': 'arm_idR'})

			# x:558 y:692
			OperatableStateMachine.add('RechterARM?',
										EqualState(),
										transitions={'true': 'ComputeRightDrop_2', 'false': 'ComputeLeftDrop_2'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'USEarmID', 'value_b': 'arm_idR'})

			# x:766 y:699
			OperatableStateMachine.add('ComputeRightDrop_2',
										ComputeBeltDrop(joint_names=['right_shoulder_pan_joint', 'right_shoulder_lift_joint', 'right_elbow_joint', 'right_wrist_1_joint', 'right_wrist_2_joint', 'right_wrist_3_joint']),
										transitions={'continue': 'GoToDropRight_2', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_groupR', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_linkR', 'pose': 'DropPose', 'offset': 'SideZoffset', 'SideYoffset': 'SideYoffset', 'SideXoffset': 'SideXoffset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:747 y:820
			OperatableStateMachine.add('ComputeLeftDrop_2',
										ComputeBeltDrop(joint_names=['left_shoulder_pan_joint', 'left_shoulder_lift_joint', 'left_elbow_joint', 'left_wrist_1_joint', 'left_wrist_2_joint', 'left_wrist_3_joint']),
										transitions={'continue': 'GoToDropLeft_2', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_groupL', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_linkL', 'pose': 'DropPose', 'offset': 'SideZoffset', 'SideYoffset': 'SideYoffset', 'SideXoffset': 'SideXoffset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:920 y:692
			OperatableStateMachine.add('GoToDropRight_2',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'GripperUITRechts_2', 'planning_failed': 'GripperUITRechts_2', 'control_failed': 'GripperUITRechts_2'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_groupR', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:915 y:817
			OperatableStateMachine.add('GoToDropLeft_2',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'GripperUITLinks_2', 'planning_failed': 'GripperUITLinks_2', 'control_failed': 'GripperUITLinks_2'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_groupL', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1097 y:698
			OperatableStateMachine.add('GripperUITRechts_2',
										VacuumGripperControlState(enable=False),
										transitions={'continue': 'ResetRightArmItem_2', 'failed': 'GoToDropRight_2', 'invalid_arm_id': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_arm_id': Autonomy.Off},
										remapping={'arm_id': 'arm_idR'})

			# x:1099 y:814
			OperatableStateMachine.add('GripperUITLinks_2',
										VacuumGripperControlState(enable=False),
										transitions={'continue': 'ResetLeftArmItem_2', 'failed': 'GoToDropLeft_2', 'invalid_arm_id': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_arm_id': Autonomy.Off},
										remapping={'arm_id': 'arm_idL'})

			# x:1275 y:697
			OperatableStateMachine.add('ResetRightArmItem_2',
										ReplaceState(),
										transitions={'done': 'AddX2offsetPiston'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'Niks', 'result': 'RightArmItem'})

			# x:1277 y:816
			OperatableStateMachine.add('ResetLeftArmItem_2',
										ReplaceState(),
										transitions={'done': 'AddX2offsetPiston'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'Niks', 'result': 'LeftArmItem'})

			# x:1498 y:688
			OperatableStateMachine.add('AddX2offsetPiston',
										AddNumericState(),
										transitions={'done': 'CheckPistonRows'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'offsetXPiston', 'value_b': 'PistonOffset', 'result': 'offsetXPiston'})

			# x:1799 y:736
			OperatableStateMachine.add('CheckPistonRound',
										EqualState(),
										transitions={'true': 'ResetPistonRound', 'false': 'StartUP'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'PistonRound', 'value_b': 'RoundTarget'})

			# x:1496 y:761
			OperatableStateMachine.add('CheckPistonRows',
										EqualState(),
										transitions={'true': 'ResetPistonRow', 'false': 'AddPistonRound'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'PistonRound', 'value_b': 'RowTarget'})

			# x:1521 y:897
			OperatableStateMachine.add('ResetPistonRow',
										ReplaceState(),
										transitions={'done': 'AddYoffsetPiston'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'Zero_Value', 'result': 'offsetXPiston'})

			# x:1519 y:959
			OperatableStateMachine.add('AddYoffsetPiston',
										AddNumericState(),
										transitions={'done': 'AddPistonRound'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'PistonOffset', 'value_b': 'offsetYPiston', 'result': 'offsetYPiston'})

			# x:1800 y:661
			OperatableStateMachine.add('AddPistonRound',
										AddNumericState(),
										transitions={'done': 'CheckPistonRound'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'One_value', 'value_b': 'PistonRound', 'result': 'PistonRound'})

			# x:1811 y:860
			OperatableStateMachine.add('ResetPistonRound',
										ReplaceState(),
										transitions={'done': 'BinVol'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'Zero_Value', 'result': 'offsetYPiston'})

			# x:1954 y:43
			OperatableStateMachine.add('BackToSH3',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'StartUP', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_nameSH3', 'move_group': 'move_groupG', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
