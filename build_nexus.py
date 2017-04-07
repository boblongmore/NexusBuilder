#!/usr/bin/env python

import xlrd
import yaml
import json

def start_xls():
	ipam_book = xlrd.open_workbook("Port_Allocation.xlsx")
	ipam_sheet_common = ipam_book.sheet_by_index(0)
	ipam_sheet_vlan = ipam_book.sheet_by_index(1)
	
	out_file = open('xlstoyaml.yml', 'a')
	#out_file.write('---\n\n')

	items = {}

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

	#items.update(item)
	#print json.dumps(items, indent=4)

	#print yaml.safe_dump(items)
	print yaml.safe_dump(items, default_flow_style=None, explicit_start=True)
	yaml.safe_dump(items, out_file, default_flow_style=None, explicit_start=True)

if __name__ == "__main__":
	start_xls()