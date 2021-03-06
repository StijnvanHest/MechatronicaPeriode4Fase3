#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.message_state import MessageState
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_flexbe_behaviors.path_gear_red_sm import Path_Gear_RedSM
from ariac_support_flexbe_states.replace_state import ReplaceState
from ariac_flexbe_behaviors.path_shelves_sm import Path_ShelvesSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed May 27 2020
@author: Anne van Oirschot
'''
class Transport_part_from_bin_to_agvSM(Behavior):
	'''
	Transporteren van een part naar de AGV
	'''


	def __init__(self):
		super(Transport_part_from_bin_to_agvSM, self).__init__()
		self.name = 'Transport_part_from_bin_to_agv'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Path_Gear_RedSM, 'Path_Gear_Red')
		self.add_behavior(Path_ShelvesSM, 'Path_Shelves')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1185 y:352, x:524 y:568
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['agv_id', 'part_type', 'part_pose', 'bin_id'])
		_state_machine.userdata.agv_id = ''
		_state_machine.userdata.part_type = ''
		_state_machine.userdata.part_pose = ''
		_state_machine.userdata.bin_id = ''
		_state_machine.userdata.bin_gear_red = 'bin14'
		_state_machine.userdata.bin_pully_red = 'bin3'
		_state_machine.userdata.shelf_gasket_red = 'shelf6'
		_state_machine.userdata.shelf_gear_blue = 'shelf3'
		_state_machine.userdata.camera_frame = ''
		_state_machine.userdata.camera_frame_gear_red = 'logical_camera_BinGroup1_frame'
		_state_machine.userdata.camera_frame_pully_red = 'logical_camera_BinGroup3_frame'
		_state_machine.userdata.camera_frame_gear_blue = 'logical_camera_Shelf2_frame'
		_state_machine.userdata.camera_frame_gasket_red = 'logical_camera_Shelf1_frame'
		_state_machine.userdata.camera_topic = ''
		_state_machine.userdata.camera_topic_gear_red = '/ariac/logical_camera_BinGroup1'
		_state_machine.userdata.camera_topic_pully_red = '/ariac/logical_camera_BinGroup3'
		_state_machine.userdata.camera_topic_gear_blue = '/ariac/logical_camera_Shelf2'
		_state_machine.userdata.camera_topic_gasket_red = '/ariac/logical_camera_Shelf1'
		_state_machine.userdata.PreGraspGantry = ''
		_state_machine.userdata.PreGraspGantry_GearRed = 'Gantry_Bin3_4'
		_state_machine.userdata.PreGraspGantry_PullyRed = 'Gantry_Bin11_12'
		_state_machine.userdata.offset = 0
		_state_machine.userdata.offsetPully = 0.085
		_state_machine.userdata.offsetGear = 0.025
		_state_machine.userdata.offsetGasket = 0.035
		_state_machine.userdata.PreGraspGantry_GasketRed = 'Gantry_ShelfRightRed'
		_state_machine.userdata.PreGraspGantry_GearBlue = 'Gantry_ShelfRightBlue'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('AgvIdMessage',
										MessageState(),
										transitions={'continue': 'PartTypeMessage'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'agv_id'})

			# x:188 y:36
			OperatableStateMachine.add('PartTypeMessage',
										MessageState(),
										transitions={'continue': 'PoseMessage'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'part_type'})

			# x:346 y:36
			OperatableStateMachine.add('PoseMessage',
										MessageState(),
										transitions={'continue': 'BinIdMessage'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'part_pose'})

			# x:492 y:38
			OperatableStateMachine.add('BinIdMessage',
										MessageState(),
										transitions={'continue': 'Selector_BinGearRed'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'bin_id'})

			# x:24 y:124
			OperatableStateMachine.add('Selector_BinGearRed',
										EqualState(),
										transitions={'true': 'CameraFrameGearRed', 'false': 'Selector_BinPullyRed'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'bin_id', 'value_b': 'bin_gear_red'})

			# x:24 y:239
			OperatableStateMachine.add('Selector_BinPullyRed',
										EqualState(),
										transitions={'true': 'CameraFramePullyRed', 'false': 'Selector_ShelfGasketRed'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'bin_id', 'value_b': 'bin_pully_red'})

			# x:24 y:345
			OperatableStateMachine.add('Selector_ShelfGasketRed',
										EqualState(),
										transitions={'true': 'CameraFrameGasketRed', 'false': 'Selector_ShelfGearBlue'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'bin_id', 'value_b': 'shelf_gasket_red'})

			# x:23 y:448
			OperatableStateMachine.add('Selector_ShelfGearBlue',
										EqualState(),
										transitions={'true': 'CameraFrameGearBlue', 'false': 'failed'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'bin_id', 'value_b': 'shelf_gear_blue'})

			# x:1007 y:181
			OperatableStateMachine.add('Path_Gear_Red',
										self.use_behavior(Path_Gear_RedSM, 'Path_Gear_Red'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'bin_id': 'bin_id', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part_type': 'part_type', 'PreGraspGantry': 'PreGraspGantry', 'offset': 'offset'})

			# x:231 y:124
			OperatableStateMachine.add('CameraFrameGearRed',
										ReplaceState(),
										transitions={'done': 'CameraTopicGearRed'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'camera_frame_gear_red', 'result': 'camera_frame'})

			# x:230 y:228
			OperatableStateMachine.add('CameraFramePullyRed',
										ReplaceState(),
										transitions={'done': 'CameraTopicPullyRed'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'camera_frame_pully_red', 'result': 'camera_frame'})

			# x:230 y:331
			OperatableStateMachine.add('CameraFrameGasketRed',
										ReplaceState(),
										transitions={'done': 'CameraTopicGasketRed'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'camera_frame_gasket_red', 'result': 'camera_frame'})

			# x:232 y:431
			OperatableStateMachine.add('CameraFrameGearBlue',
										ReplaceState(),
										transitions={'done': 'CameraTopicGearBlue'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'camera_frame_gear_blue', 'result': 'camera_frame'})

			# x:601 y:128
			OperatableStateMachine.add('PreGraspRightGantry',
										ReplaceState(),
										transitions={'done': 'OffsetGearRed'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'PreGraspGantry_GearRed', 'result': 'PreGraspGantry'})

			# x:598 y:228
			OperatableStateMachine.add('PreGraspRightGantry_2',
										ReplaceState(),
										transitions={'done': 'OffsetPullyRed'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'PreGraspGantry_PullyRed', 'result': 'PreGraspGantry'})

			# x:413 y:125
			OperatableStateMachine.add('CameraTopicGearRed',
										ReplaceState(),
										transitions={'done': 'PreGraspRightGantry'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'camera_topic_gear_red', 'result': 'camera_topic'})

			# x:413 y:226
			OperatableStateMachine.add('CameraTopicPullyRed',
										ReplaceState(),
										transitions={'done': 'PreGraspRightGantry_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'camera_topic_pully_red', 'result': 'camera_topic'})

			# x:420 y:336
			OperatableStateMachine.add('CameraTopicGasketRed',
										ReplaceState(),
										transitions={'done': 'PreGraspRightGantry_3'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'camera_topic_gasket_red', 'result': 'camera_topic'})

			# x:422 y:434
			OperatableStateMachine.add('CameraTopicGearBlue',
										ReplaceState(),
										transitions={'done': 'PreGraspRightGantry_4'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'camera_topic_gear_blue', 'result': 'camera_topic'})

			# x:795 y:128
			OperatableStateMachine.add('OffsetGearRed',
										ReplaceState(),
										transitions={'done': 'Path_Gear_Red'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'offsetGear', 'result': 'offset'})

			# x:788 y:228
			OperatableStateMachine.add('OffsetPullyRed',
										ReplaceState(),
										transitions={'done': 'Path_Gear_Red'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'offsetPully', 'result': 'offset'})

			# x:801 y:327
			OperatableStateMachine.add('OffsetGasketRed',
										ReplaceState(),
										transitions={'done': 'Path_Shelves'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'offsetGasket', 'result': 'offset'})

			# x:804 y:434
			OperatableStateMachine.add('OffsetGearBlue',
										ReplaceState(),
										transitions={'done': 'Path_Shelves'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'offsetGear', 'result': 'offset'})

			# x:603 y:330
			OperatableStateMachine.add('PreGraspRightGantry_3',
										ReplaceState(),
										transitions={'done': 'OffsetGasketRed'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'PreGraspGantry_GasketRed', 'result': 'PreGraspGantry'})

			# x:598 y:425
			OperatableStateMachine.add('PreGraspRightGantry_4',
										ReplaceState(),
										transitions={'done': 'OffsetGearBlue'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'PreGraspGantry_GearBlue', 'result': 'PreGraspGantry'})

			# x:992 y:365
			OperatableStateMachine.add('Path_Shelves',
										self.use_behavior(Path_ShelvesSM, 'Path_Shelves'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'bin_id': 'bin_id', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part_type': 'part_type', 'PreGraspGantry': 'PreGraspGantry', 'offset': 'offset'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
