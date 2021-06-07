import argparse
import textwrap

from utils import get_dataset, get_dataset_confs, list_datasets, removeHyphen, renameDatasetColumn, render_features

from templates import Template, TemplateCollection


parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument("dataset_path", type=str, help="path to dataset name")

args = parser.parse_args()
if "templates.yaml" not in args.dataset_path:
    exit()

path = args.dataset_path.split("/")

dataset_name = path[1]
subset_name = path[2] if len(path) == 4 else ""
template_collection = TemplateCollection()

dataset, _ = get_dataset(dataset_name, subset_name)
splits = list(dataset.keys())
dataset = dataset[splits[0]]

dataset_templates = template_collection.get_dataset(dataset_name, subset_name)
template_list = dataset_templates.all_template_names

width = 80
for template_name in template_list:
    template = dataset_templates[template_name]
    print()
    print("TEMPLATE", template_name)
    print("--------")
    print()
    print(template.jinja)
    print()

    for example_index in range(10):
        example = dataset[example_index]
        print()
        print("\tExample ", example)
        print()
        xp, yp = template.apply(example)
        print()
        print("\tPrompt | X")
        for l in textwrap.wrap(xp, width=width, replace_whitespace=False):
            print("\t", l.replace("\n", "\n\t"))
        print()
        print("\tY")
        for l in textwrap.wrap(yp, width=width, replace_whitespace=False):
            print("\t", l.replace("\n", "\n\t"))
