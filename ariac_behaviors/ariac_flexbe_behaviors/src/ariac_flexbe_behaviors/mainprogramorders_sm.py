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

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:821 y:56, x:886 y:255
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
										transitions={'done': 'Transport_part_from_bin_to_agv', 'invalid_index': 'failed'},
										autonomy={'done': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'list': 'material_locations', 'index': 'bin_index', 'item': 'bin_id'})

			# x:1410 y:229
			OperatableStateMachine.add('IncrementProductIndex',
										AddNumericState(),
										transitions={'done': 'EndProduct'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'product_index', 'value_b': 'one_value', 'result': 'product_index'})

			# x:1413 y:335
			OperatableStateMachine.add('EndProduct',
										EqualState(),
										transitions={'true': 'ResetProductIndex', 'false': 'GetPart'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'product_index', 'value_b': 'number_of_products'})

			# x:1415 y:459
			OperatableStateMachine.add('ResetProductIndex',
										ReplaceState(),
										transitions={'done': 'IncrementShipmentIndex'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'zero_value', 'result': 'product_index'})

			# x:1418 y:560
			OperatableStateMachine.add('IncrementShipmentIndex',
										AddNumericState(),
										transitions={'done': 'Notify_Shipment_Ready'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'shipment_index', 'value_b': 'one_value', 'result': 'shipment_index'})

			# x:1155 y:666
			OperatableStateMachine.add('EndShipment',
										EqualState(),
										transitions={'true': 'ResetShipmentIndex', 'false': 'GetShipment'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'shipment_index', 'value_b': 'number_of_shipments'})

			# x:1402 y:654
			OperatableStateMachine.add('Notify_Shipment_Ready',
										self.use_behavior(Notify_Shipment_ReadySM, 'Notify_Shipment_Ready'),
										transitions={'finished': 'EndShipment', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'agv_id': 'agv_id', 'shipment_type': 'shipment_type'})

			# x:1596 y:125
			OperatableStateMachine.add('Transport_part_from_bin_to_agv',
										self.use_behavior(Transport_part_from_bin_to_agvSM, 'Transport_part_from_bin_to_agv'),
										transitions={'finished': 'IncrementProductIndex', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'agv_id': 'agv_id', 'part_type': 'part_type', 'part_pose': 'part_pose'})

			# x:907 y:664
			OperatableStateMachine.add('ResetShipmentIndex',
										ReplaceState(),
										transitions={'done': 'GetOrder'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'zero_value', 'result': 'shipment_index'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
