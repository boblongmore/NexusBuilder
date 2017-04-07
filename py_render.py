#!/usr/bin/env python

from jinja2 import Template  
import yaml
import os

def config_render():
    #Parse the YAML file and produce a Python dict.
    yaml_vars = yaml.load(open('xlstoyaml.yml').read())

    #Load the Jinja2 template into a Python data structure.
    template = Template(open('nexus9k.j2').read())

    #Render the configuration using the Jinja2 render method using yaml_vars as arg.
    rendered_config = template.render(yaml_vars)

    #Write the rendered configuration to a text file.
    #config_name = yaml_vars['hostname']
    config_name = "testrender"
    with open(config_name, 'w') as config:
        config.write(rendered_config)
    if os.path.isfile(config_name):
        print "The configuration file, %s, is present." % config_name
    else:
        print "The configuration file, %s,  is not present." % config_name

if __name__ == "__main__":
    config_render()