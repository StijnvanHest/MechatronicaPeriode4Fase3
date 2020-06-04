#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.start_assignment_state import StartAssignment
from ariac_logistics_flexbe_states.get_order_state import GetOrderState
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_support_flexbe_states.replace_state import ReplaceState
from ariac_flexbe_states.end_assignment_state import EndAssignment
from ariac_logistics_flexbe_states.get_products_from_shipment_state import GetProductsFromShipmentState
from ariac_logistics_flexbe_states.get_part_from_products_state import GetPartFromProductsState
from ariac_logistics_flexbe_states.get_material_locations import GetMaterialLocationsState
from ariac_support_flexbe_states.get_item_from_list_state import GetItemFromListState
from ariac_support_flexbe_states.add_numeric_state import AddNumericState
from ariac_flexbe_behaviors.notify_shipment_ready_sm import Notify_Shipment_ReadySM
from ariac_flexbe_behaviors.transport_part_from_bin_to_agv_sm import Transport_part_from_bin_to_agvSM
from ariac_flexbe_states.Check_Gripper_attached import CheckGripperattached
from ariac_flexbe_behaviors.transport_part_from_bin_to_agv_leftarm_sm import Transport_part_from_bin_to_agv_LeftArmSM
from ariac_flexbe_behaviors.placeonagv_sm import PlaceOnAgvSM
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed May 27 2020
@author: Anne van Oirschot
'''
class MainProgramOrdersSM(Behavior):
	'''
	Hoofdprogramma voor het verwerken van orders
	'''


	def __init__(self):
		super(MainProgramOrdersSM, self).__init__()
		self.name = 'MainProgramOrders'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Notify_Shipment_ReadySM, 'Notify_Shipment_Ready')
		self.add_behavior(Transport_part_from_bin_to_agvSM, 'Transport_part_from_bin_to_agv')
		self.add_behavior(Transport_part_from_bin_to_agv_LeftArmSM, 'Transport_part_from_bin_to_agv_LeftArm')
		self.add_behavior(PlaceOnAgvSM, 'PlaceOnAgv')
		self.add_behavior(PlaceOnAgvSM, 'PlaceOnAgv_2')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:821 y:56, x:1214 y:358
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.order_id = ''
		_state_machine.userdata.shipments = []
		_state_machine.userdata.number_of_shipments = 0
		_state_machine.userdata.old_order_id = ''
		_state_machine.userdata.shipment_index = 0
		_state_machine.userdata.shipment_type = ''
		_state_machine.userdata.agv_id = ''
		_state_machine.userdata.products = []
		_state_machine.userdata.number_of_products = 0
		_state_machine.userdata.product_index = 0
		_state_machine.userdata.part_type = ''
		_state_machine.userdata.material_locations = []
		_state_machine.userdata.bin_index = 0
		_state_machine.userdata.bin_id = ''
		_state_machine.userdata.one_value = 1
		_state_machine.userdata.zero_value = 0
		_state_machine.userdata.arm_right = 'right_arm'
		_state_machine.userdata.arm_left = 'left_arm'
		_state_machine.userdata.product_location1 = ''
		_state_machine.userdata.product_location2 = ''
		_state_machine.userdata.home_rightarm_id = 'Right_PreGrasp'
		_state_machine.userdata.move_group_right = 'Right_Arm'
		_state_machine.userdata.move_group_prefix = '/ariac/gantry'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.home_leftarm_id = 'Left_PreGrasp'
		_state_machine.userdata.move_group_left = 'Left_Arm'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:57 y:48
			OperatableStateMachine.add('StartAssignment',
										StartAssignment(),
										transitions={'continue': 'GetOrder'},
										autonomy={'continue': Autonomy.Off})

			# x:218 y:48
			OperatableStateMachine.add('GetOrder',
										GetOrderState(),
										transitions={'continue': 'Test_LastOrder'},
										autonomy={'continue': Autonomy.Off},
										remapping={'order_id': 'order_id', 'shipments': 'shipments', 'number_of_shipments': 'number_of_shipments'})

			# x:422 y:47
			OperatableStateMachine.add('Test_LastOrder',
										EqualState(),
										transitions={'true': 'EndAssignment', 'false': 'Remember_OldOrder'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'order_id', 'value_b': 'old_order_id'})

			# x:614 y:124
			OperatableStateMachine.add('Remember_OldOrder',
										ReplaceState(),
										transitions={'done': 'GetShipment'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'order_id', 'result': 'old_order_id'})

			# x:622 y:47
			OperatableStateMachine.add('EndAssignment',
										EndAssignment(),
										transitions={'continue': 'finished'},
										autonomy={'continue': Autonomy.Off})

			# x:801 y:119
			OperatableStateMachine.add('GetShipment',
										GetProductsFromShipmentState(),
										transitions={'continue': 'GetPart', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'shipments': 'shipments', 'index': 'shipment_index', 'shipment_type': 'shipment_type', 'agv_id': 'agv_id', 'products': 'products', 'number_of_products': 'number_of_products'})

			# x:1023 y:119
			OperatableStateMachine.add('GetPart',
										GetPartFromProductsState(),
										transitions={'continue': 'MaterialLocation', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'products': 'products', 'index': 'product_index', 'type': 'part_type', 'pose': 'part_pose'})

			# x:1217 y:116
			OperatableStateMachine.add('MaterialLocation',
										GetMaterialLocationsState(),
										transitions={'continue': 'GetBin'},
										autonomy={'continue': Autonomy.Off},
										remapping={'part': 'part_type', 'material_locations': 'material_locations'})

			# x:1403 y:114
			OperatableStateMachine.add('GetBin',
										GetItemFromListState(),
										transitions={'done': 'CheckAttachedRight', 'invalid_index': 'failed'},
										autonomy={'done': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'list': 'material_locations', 'index': 'bin_index', 'item': 'bin_id'})

			# x:1361 y:507
			OperatableStateMachine.add('IncrementProductIndex',
										AddNumericState(),
										transitions={'done': 'EndProduct'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'product_index', 'value_b': 'one_value', 'result': 'product_index'})

			# x:1360 y:585
			OperatableStateMachine.add('EndProduct',
										EqualState(),
										transitions={'true': 'HomepositieRightArm', 'false': 'CheckAttachedRight2'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'product_index', 'value_b': 'number_of_products'})

			# x:95 y:565
			OperatableStateMachine.add('ResetProductIndex',
										ReplaceState(),
										transitions={'done': 'IncrementShipmentIndex'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'zero_value', 'result': 'product_index'})

			# x:98 y:469
			OperatableStateMachine.add('IncrementShipmentIndex',
										AddNumericState(),
										transitions={'done': 'Notify_Shipment_Ready'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'shipment_index', 'value_b': 'one_value', 'result': 'shipment_index'})

			# x:89 y:277
			OperatableStateMachine.add('EndShipment',
										EqualState(),
										transitions={'true': 'ResetShipmentIndex', 'false': 'GetShipment'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'shipment_index', 'value_b': 'number_of_shipments'})

			# x:87 y:378
			OperatableStateMachine.add('Notify_Shipment_Ready',
										self.use_behavior(Notify_Shipment_ReadySM, 'Notify_Shipment_Ready'),
										transitions={'finished': 'EndShipment', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'agv_id': 'agv_id', 'shipment_type': 'shipment_type'})

			# x:1605 y:181
			OperatableStateMachine.add('Transport_part_from_bin_to_agv',
										self.use_behavior(Transport_part_from_bin_to_agvSM, 'Transport_part_from_bin_to_agv'),
										transitions={'finished': 'SetVariablePart1', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'agv_id': 'agv_id', 'part_type': 'part_type', 'part_pose': 'part_pose', 'bin_id': 'bin_id'})

			# x:95 y:183
			OperatableStateMachine.add('ResetShipmentIndex',
										ReplaceState(),
										transitions={'done': 'GetOrder'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'zero_value', 'result': 'shipment_index'})

			# x:1354 y:248
			OperatableStateMachine.add('CheckAttachedRight',
										CheckGripperattached(),
										transitions={'True': 'CheckAttachedLeft', 'False': 'Transport_part_from_bin_to_agv', 'invalid_arm_id': 'failed'},
										autonomy={'True': Autonomy.Off, 'False': Autonomy.Off, 'invalid_arm_id': Autonomy.Off},
										remapping={'arm_id': 'arm_right'})

			# x:1356 y:335
			OperatableStateMachine.add('CheckAttachedLeft',
										CheckGripperattached(),
										transitions={'True': 'IncrementProductIndex', 'False': 'Transport_part_from_bin_to_agv_LeftArm', 'invalid_arm_id': 'failed'},
										autonomy={'True': Autonomy.Off, 'False': Autonomy.Off, 'invalid_arm_id': Autonomy.Off},
										remapping={'arm_id': 'arm_left'})

			# x:1572 y:418
			OperatableStateMachine.add('Transport_part_from_bin_to_agv_LeftArm',
										self.use_behavior(Transport_part_from_bin_to_agv_LeftArmSM, 'Transport_part_from_bin_to_agv_LeftArm'),
										transitions={'finished': 'SetVariablePart2', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'agv_id': 'agv_id', 'part_type': 'part_type', 'part_pose': 'part_pose', 'bin_id': 'bin_id'})

			# x:1654 y:275
			OperatableStateMachine.add('SetVariablePart1',
										ReplaceState(),
										transitions={'done': 'IncrementProductIndex'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'part_pose', 'result': 'product_location1'})

			# x:1651 y:503
			OperatableStateMachine.add('SetVariablePart2',
										ReplaceState(),
										transitions={'done': 'IncrementProductIndex'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'part_pose', 'result': 'product_location2'})

			# x:997 y:510
			OperatableStateMachine.add('CheckAttachedRight2',
										CheckGripperattached(),
										transitions={'True': 'CheckAttachedLeft2', 'False': 'GetPart', 'invalid_arm_id': 'failed'},
										autonomy={'True': Autonomy.Off, 'False': Autonomy.Off, 'invalid_arm_id': Autonomy.Off},
										remapping={'arm_id': 'arm_right'})

			# x:803 y:520
			OperatableStateMachine.add('CheckAttachedLeft2',
										CheckGripperattached(),
										transitions={'True': 'PlaceOnAgv', 'False': 'GetPart', 'invalid_arm_id': 'failed'},
										autonomy={'True': Autonomy.Off, 'False': Autonomy.Off, 'invalid_arm_id': Autonomy.Off},
										remapping={'arm_id': 'arm_left'})

			# x:533 y:450
			OperatableStateMachine.add('PlaceOnAgv',
										self.use_behavior(PlaceOnAgvSM, 'PlaceOnAgv'),
										transitions={'finished': 'GetPart', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'agv_id': 'agv_id', 'part_pose_right': 'product_location1', 'part_pose_left': 'product_location2'})

			# x:1371 y:670
			OperatableStateMachine.add('HomepositieRightArm',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'HomepositieLeftArm', 'planning_failed': 'Retry_1', 'control_failed': 'Retry_1', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'home_rightarm_id', 'move_group': 'move_group_right', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1182 y:655
			OperatableStateMachine.add('HomepositieLeftArm',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'PlaceOnAgv_2', 'planning_failed': 'Retry_2', 'control_failed': 'Retry_2', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'home_leftarm_id', 'move_group': 'move_group_left', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1558 y:671
			OperatableStateMachine.add('Retry_1',
										WaitState(wait_time=3),
										transitions={'done': 'HomepositieRightArm'},
										autonomy={'done': Autonomy.Off})

			# x:1226 y:733
			OperatableStateMachine.add('Retry_2',
										WaitState(wait_time=3),
										transitions={'done': 'HomepositieLeftArm'},
										autonomy={'done': Autonomy.Off})

			# x:832 y:626
			OperatableStateMachine.add('PlaceOnAgv_2',
										self.use_behavior(PlaceOnAgvSM, 'PlaceOnAgv_2'),
										transitions={'finished': 'ResetProductIndex', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'agv_id': 'agv_id', 'part_pose_right': 'product_location1', 'part_pose_left': 'product_location2'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
