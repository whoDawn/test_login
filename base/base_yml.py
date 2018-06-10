import yaml

def yml_with_file(file_name, key):
    with open("./data/" + file_name + ".yml","r",encoding='utf-8') as f:
        file_yml =  yaml.load(f)[key]

        yml_list = []
        for i in file_yml.values():
            yml_list.append(i)
        return yml_list