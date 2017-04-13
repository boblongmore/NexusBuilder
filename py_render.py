#!/usr/bin/env python

from jinja2 import Template  
import yaml
import os

def config_render():
    yaml_files = ["HQ_N9K1_xlstoyaml.yml", "HQ_N9K2_xlstoyaml.yml"]
    for file_name in yaml_files:
        #Parse the YAML file and produce a Python dict.
        yaml_vars = yaml.load(open(file_name).read())

        #Load the Jinja2 template into a Python data structure.
        template = Template(open('nexus9k.j2').read())

        #Render the configuration using the Jinja2 render method using yaml_vars as arg.
        rendered_config = template.render(yaml_vars)

        #Write the rendered configuration to a text file.
        #config_name = yaml_vars['hostname']
        name_split = file_name.split(".")[0]
        config_name = name_split + ".cfg"
        with open(config_name, 'w') as config:
            config.write(rendered_config)
        if os.path.isfile(config_name):
            print "The configuration file, %s, is present." % config_name
        else:
            print "The configuration file, %s,  is not present." % config_name

if __name__ == "__main__":
    config_render()