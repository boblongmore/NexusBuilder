#!/usr/bin/env python

from jinja2 import Template  
import yaml  


#Parse the YAML file and produce a Python dict.
yaml_vars = yaml.load(open('nexus.yml').read())

#Load the Jinja2 template into a Python data structure.
template = Template(open('nexus9k.j2').read())

#Render the configuration using the Jinja2 render method using yaml_vars as arg.
rendered_config = template.render(yaml_vars)

#Write the rendered configuration to a text file.
with open('9k_test_config', 'w') as config:  
    config.write(rendered_config)