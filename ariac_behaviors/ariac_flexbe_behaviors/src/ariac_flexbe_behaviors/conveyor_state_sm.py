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
from ariac_flexbe_states.detect_first_part_camera_ariac_state import DetectFirstPartCameraAriacState
from ariac_support_flexbe_states.replace_state import ReplaceState
from ariac_flexbe_states.set_conveyorbelt_power_state import SetConveyorbeltPowerState
from flexbe_states.wait_state import WaitState
from flexbe_states.log_key_state import LogKeyState
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue May 26 2020
@author: Stijn van Hest
'''
class Conveyor_StateSM(Behavior):
	'''
	Dit is een state die de conveyor aanzet en uitzet. Ook worden de informatie van de camera doorgegeven
	'''


	def __init__(self):
		super(Conveyor_StateSM, self).__init__()
		self.name = 'Conveyor_State'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:2367 y:42, x:116 y:605
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['ARMidMAIN'], output_keys=['PartPose', 'PartOffset', 'PartTYPE', 'exactparttype'])
		_state_machine.userdata.power = 100
		_state_machine.userdata.Nopower = 0
		_state_machine.userdata.PartTYPE = ''
		_state_machine.userdata.Gear = 'Gear'
		_state_machine.userdata.Pulley = 'Pulley'
		_state_machine.userdata.Piston = 'Piston'
		_state_machine.userdata.Gasket = 'Gasket'
		_state_machine.userdata.ref_conveyor_frame = 'world'
		_state_machine.userdata.camera_conveyor_topic = '/ariac/logical_camera_Conveyor'
		_state_machine.userdata.camera_conveyor_frame = 'logical_camera_Conveyor_frame'
		_state_machine.userdata.exactparttype = ''
		_state_machine.userdata.PartPose = []
		_state_machine.userdata.Gantryjoint_values = []
		_state_machine.userdata.Rightjoint_values = []
		_state_machine.userdata.Leftjoint_values = []
		_state_machine.userdata.move_groupGantry = 'Gantry'
		_state_machine.userdata.move_group_prefixGantry = '/ariac/gantry'
		_state_machine.userdata.config_nameGtoConR = 'Gantry_RightPreConveyor'
		_state_machine.userdata.tool_linkRight = 'right_ee_link'
		_state_machine.userdata.tool_linkLeft = 'left_ee_link'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.config_nameLeftPregrasp = 'Left_PreGrasp'
		_state_machine.userdata.config_nameRightPregrasp = 'Right_PreGrasp'
		_state_machine.userdata.move_groupLeft = 'Left_Arm'
		_state_machine.userdata.move_groupRight = 'Right_Arm'
		_state_machine.userdata.PartOffset = 0
		_state_machine.userdata.PistonOffset = 0.019
		_state_machine.userdata.GasketOffset = 0.034
		_state_machine.userdata.Right_armID = 'right_arm'
		_state_machine.userdata.ARMidMAIN = ''
		_state_machine.userdata.config_nameGtoConL = 'Gantry_LeftPreConveyor'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:45 y:31
			OperatableStateMachine.add('RightArm?',
										EqualState(),
										transitions={'true': 'MoveGantryToRightConveyor', 'false': 'MoveGantryToLeftConveyor'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'ARMidMAIN', 'value_b': 'Right_armID'})

			# x:670 y:40
			OperatableStateMachine.add('DetecteerGasketParts',
										DetectFirstPartCameraAriacState(part_list=['gasket_part_red', 'gasket_part_green', 'gasket_part_blue'], time_out=3),
										transitions={'continue': 'TypePartGasket', 'failed': 'FailedWait', 'not_found': 'DetecteerPistonParts'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_conveyor_frame', 'camera_topic': 'camera_conveyor_topic', 'camera_frame': 'camera_conveyor_frame', 'part': 'exactparttype', 'pose': 'PartPose'})

			# x:668 y:143
			OperatableStateMachine.add('DetecteerPistonParts',
										DetectFirstPartCameraAriacState(part_list=['piston_rod_part_blue','piston_rod_part_red','piston_rod_part_green'], time_out=5),
										transitions={'continue': 'TypePartPiston', 'failed': 'FailedWait', 'not_found': 'DetecteerGasketParts'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_conveyor_frame', 'camera_topic': 'camera_conveyor_topic', 'camera_frame': 'camera_conveyor_frame', 'part': 'exactparttype', 'pose': 'PartPose'})

			# x:971 y:36
			OperatableStateMachine.add('TypePartGasket',
										ReplaceState(),
										transitions={'done': 'SetOffsetGasket'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'Gasket', 'result': 'PartTYPE'})

			# x:971 y:219
			OperatableStateMachine.add('TypePartPiston',
										ReplaceState(),
										transitions={'done': 'SetOffsetPiston'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'Piston', 'result': 'PartTYPE'})

			# x:89 y:512
			OperatableStateMachine.add('StopConveyor_2',
										SetConveyorbeltPowerState(),
										transitions={'continue': 'failed', 'fail': 'StopConveyor_2'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'power': 'Nopower'})

			# x:491 y:604
			OperatableStateMachine.add('FailedWait',
										WaitState(wait_time=3),
										transitions={'done': 'StopConveyor_2'},
										autonomy={'done': Autonomy.Off})

			# x:2030 y:33
			OperatableStateMachine.add('LogParttype',
										LogKeyState(text='Dit is een {}', severity=Logger.REPORT_HINT),
										transitions={'done': 'LogParttype_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'PartTYPE'})

			# x:2128 y:30
			OperatableStateMachine.add('LogParttype_2',
										LogKeyState(text='om precies te zijn een: {}', severity=Logger.REPORT_HINT),
										transitions={'done': 'CompletedWait'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'exactparttype'})

			# x:2239 y:29
			OperatableStateMachine.add('CompletedWait',
										WaitState(wait_time=0.5),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:1620 y:105
			OperatableStateMachine.add('StopConveyorafterdetected',
										SetConveyorbeltPowerState(),
										transitions={'continue': 'LogParttype', 'fail': 'FailedWait'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'power': 'Nopower'})

			# x:306 y:23
			OperatableStateMachine.add('MoveGantryToRightConveyor',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'StartConveyor', 'planning_failed': 'FailedWait', 'control_failed': 'WaitControlfailed', 'param_error': 'FailedWait'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_nameGtoConR', 'move_group': 'move_groupGantry', 'move_group_prefix': 'move_group_prefixGantry', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:51 y:252
			OperatableStateMachine.add('WaitControlfailed',
										WaitState(wait_time=1),
										transitions={'done': 'MoveGantryToRightConveyor'},
										autonomy={'done': Autonomy.Off})

			# x:1140 y:216
			OperatableStateMachine.add('SetOffsetPiston',
										ReplaceState(),
										transitions={'done': 'StopConveyorafterdetected'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'PistonOffset', 'result': 'PartOffset'})

			# x:1145 y:34
			OperatableStateMachine.add('SetOffsetGasket',
										ReplaceState(),
										transitions={'done': 'StopConveyorafterdetected'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'GasketOffset', 'result': 'PartOffset'})

			# x:302 y:113
			OperatableStateMachine.add('MoveGantryToLeftConveyor',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'StartConveyor', 'planning_failed': 'FailedWait', 'control_failed': 'WaitControlfailed_2', 'param_error': 'FailedWait'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_nameGtoConL', 'move_group': 'move_groupGantry', 'move_group_prefix': 'move_group_prefixGantry', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:53 y:339
			OperatableStateMachine.add('WaitControlfailed_2',
										WaitState(wait_time=1),
										transitions={'done': 'MoveGantryToLeftConveyor'},
										autonomy={'done': Autonomy.Off})

			# x:493 y:49
			OperatableStateMachine.add('StartConveyor',
										SetConveyorbeltPowerState(),
										transitions={'continue': 'DetecteerPistonParts', 'fail': 'FailedWait'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'power': 'power'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
