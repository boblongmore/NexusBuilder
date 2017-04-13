#!/usr/bin/env python

import xlrd
import yaml
import json
from jinja2 import Template
import os

def start_xls(hostname, sheet_id):
	check_path()
	ipam_book = xlrd.open_workbook("switch_worksheet.xlsx")
	ipam_sheet_common = ipam_book.sheet_by_index(0)
	ipam_sheet_vlan = ipam_book.sheet_by_index(1)
	#num_sheets = len(ipam_book.sheet_names())

	yml_file_name = hostname + '.yml'
	out_file = open("./yml_files/" + yml_file_name, 'a')
	#out_file.write('---\n\n')

	items = {}
	items['hostname'] = hostname

	for row in range(ipam_sheet_common.nrows):
		for column in range(ipam_sheet_common.ncols):
			if ipam_sheet_common.cell_value(row,column) == "Domain Name":
				domain = ipam_sheet_common.cell_value(row,1)
				items['domain_name'] = domain
				#yaml.safe_dump(items, out_file, default_flow_style=False)
			elif ipam_sheet_common.cell_value(row,column) == "Syslog":
				syslog = ipam_sheet_common.cell_value(row,1)
				syslog_servers = [syslog]
				items['syslog_ip'] = syslog_servers
				#yaml.safe_dump(items, out_file, default_flow_style=False)
			elif ipam_sheet_common.cell_value(row,column) == "Netflow":
				netflow = ipam_sheet_common.cell_value(row,1)
				items['netflow_ip'] = netflow
				#yaml.safe_dump(items, out_file, default_flow_style=False)
			elif ipam_sheet_common.cell_value(row,column) == "NTP":
				netflow = ipam_sheet_common.cell_value(row,1)
				items['ntp_ip'] = netflow
				#yaml.safe_dump(items, out_file, default_flow_style=False)
			elif ipam_sheet_common.cell_value(row,column) == "Time Zone":
				time_zone_value = ipam_sheet_common.cell_value(row,1)
				items['time_zone'] = time_zone_value
				#yaml.safe_dump(items, out_file, default_flow_style=False)
			elif ipam_sheet_common.cell_value(row,column) == "SNMP Server":
				SNMP_ip = ipam_sheet_common.cell_value(row,1)
				try:
					SNMP_list
					SNMP_list.extend([SNMP_ip])
				except NameError:
					SNMP_list = [SNMP_ip]
				items['SNMP'] = SNMP_list
				#yaml.safe_dump(items, out_file, default_flow_style=False)
			elif ipam_sheet_common.cell_value(row,column) == "SNMP RO":
				RO_string = ipam_sheet_common.cell_value(row,1)
				try:
					SNMP_RO_list
					SNMP_RO_list.extend([RO_string])
				except NameError:
					SNMP_RO_list = [RO_string]
				items['snmp_community'] = SNMP_RO_list
				#yaml.safe_dump(items, out_file, default_flow_style=False)
			elif ipam_sheet_common.cell_value(row,column) == "SNMP RW":
				RW_string = ipam_sheet_common.cell_value(row,1)
				items['SNMP_RW'] = RW_string
				#yaml.safe_dump(items, out_file, default_flow_style=False)
			elif ipam_sheet_common.cell_value(row,column) == "DHCP Relay":
				DHCP_relay_ip = ipam_sheet_common.cell_value(row,1)
				items['DHCP_Relay'] = DHCP_relay_ip
				#yaml.safe_dump(items, out_file, default_flow_style=False)
			elif ipam_sheet_common.cell_value(row,column) == "EIGRP Name":
				eigrp_string = ipam_sheet_common.cell_value(row,1)
				items['EIGRP_name'] = eigrp_string
				#yaml.safe_dump(items, out_file, default_flow_style=False)
			elif ipam_sheet_common.cell_value(row,column) == "EIGRP AS#":
				eigrp_as_string = ipam_sheet_common.cell_value(row,1)
				items['EIGRP_AS'] = int(eigrp_as_string)
				#yaml.safe_dump(items, out_file, default_flow_style=False)

	for row in range(ipam_sheet_vlan.nrows):
		vlan_id = ipam_sheet_vlan.cell_value(row, 0)
		vlan_name = ipam_sheet_vlan.cell_value(row, 1)
		try:
			vlan_info = {}
			vlan_info["id"] = int(vlan_id)
			vlan_info["name"] = str(vlan_name)
			try:
				vlan_list
				vlan_list.extend([vlan_info])
			except NameError:
				vlan_list = [vlan_info]
			# vlans = [vlan_info]
			items['vlans'] = vlan_list
		except ValueError:
			pass

	#for sheet_id in range(2,num_sheets):
	ipam_sheet_intf = ipam_book.sheet_by_index(sheet_id)
	for row in range(ipam_sheet_intf.nrows):
		intf_id = ipam_sheet_intf.cell_value(row, 0)
		ip_addr = ipam_sheet_intf.cell_value(row, 1)
		sw_mode = ipam_sheet_intf.cell_value(row, 5)
		allowed_vlans = ipam_sheet_intf.cell_value(row, 6)
		native_vlan = ipam_sheet_intf.cell_value(row, 7)
		port_ch = ipam_sheet_intf.cell_value(row, 8)
		stp_mode = ipam_sheet_intf.cell_value(row, 9)
		intf_descr = ipam_sheet_intf.cell_value(row, 10)
		if sw_mode == 'Trunk':
			try:
				intf_info = {}
				intf_info["intf"] = intf_id
				intf_info["description"] = intf_descr
				intf_info["mode"] = sw_mode
				intf_info["switchport"] = "switchport"
				intf_info["vpc"] = int(port_ch)
				intf_info["vlan_range"] = allowed_vlans
				intf_info["native_vlan"] = int(native_vlan)
				intf_info["stp"] = stp_mode
				intf_info["state"] = "no shutdown"
				try:
					intf_list
					intf_list.extend([intf_info])
				except NameError:
					intf_list = [intf_info]
				# vlans = [vlan_info]
				items['interfaces'] = intf_list
			except ValueError:
				pass
		elif sw_mode == 'Access':
			try:
				intf_info = {}
				intf_info["intf"] = intf_id
				intf_info["description"] = intf_descr
				intf_info["mode"] = sw_mode
				intf_info["switchport"] = "switchport"
				intf_info["vpc"] = int(port_ch)
				intf_info["vlan_range"] = allowed_vlans
				intf_info["stp"] = stp_mode
				intf_info["state"] = "no shutdown"
				try:
					intf_list
					intf_list.extend([intf_info])
				except NameError:
					intf_list = [intf_info]
				items['interfaces'] = intf_list
			except ValueError:
				pass
		elif sw_mode == 'L3':
			try:
				intf_info = {}
				intf_info["intf"] = intf_id
				intf_info["description"] = intf_descr
				intf_info["switchport"] = "no switchport"
				intf_info["ip"] = ip_addr
				intf_info["state"] = "no shutdown"
				try:
					intf_list
					intf_list.extend([intf_info])
				except NameError:
					intf_list = [intf_info]
				items['interfaces'] = intf_list
			except ValueError:
				pass



	#items.update(item)
	#print json.dumps(items, indent=4)

	#print yaml.safe_dump(items)
	print yaml.safe_dump(items, default_flow_style=None, explicit_start=True)
	yaml.safe_dump(items, out_file, default_flow_style=None, explicit_start=True)
	config_render(yml_file_name)

def config_render(yml_file):
	# Parse the YAML file and produce a Python dict.
	yaml_vars = yaml.load(open("./yml_files/" + yml_file).read())
	# Load the Jinja2 template into a Python data structure.
	template = Template(open('nexus9k.j2').read())
	# Render the configuration using the Jinja2 render method using yaml_vars as arg.
	rendered_config = template.render(yaml_vars)
	# Write the rendered configuration to a text file.
	# config_name = yaml_vars['hostname']
	name_split = yml_file.split(".")[0]
	config_name = "./cfg_files/" + name_split + ".cfg"
	with open(config_name, 'w') as config:
		config.write(rendered_config)
	if os.path.isfile(config_name):
		print "The configuration file, %s, is present." % config_name
	else:
		print "The configuration file, %s,  is not present." % config_name

def check_path():
	path_yml = "./yml_files/"
	path_cfg = "./cfg_files/"
	paths = [path_yml, path_cfg]
	for path in paths:
		dir = os.path.dirname(path)
		if not os.path.exists(dir):
			os.makedirs(dir)
	return

def build_config():
	ipam_book = xlrd.open_workbook("switch_worksheet.xlsx")
	num_sheets = len(ipam_book.sheet_names())
	for sheet_id in range(2, num_sheets):
		hostname = ipam_book.sheet_names()[sheet_id]
		start_xls(hostname, sheet_id)

if __name__ == "__main__":
	build_config()
