import glob
import os
import xml.etree.ElementTree as ET

import pandas as pd

import config


def xml_to_csv(path):
    classes_names = []
    xml_list = []
    for xml_file in glob.glob(path + "/*.xml"):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall("object"):
            classes_names.append(member[0].text)
            value = (
                root.find("filename").text,
                int(root.find("size")[0].text),
                int(root.find("size")[1].text),
                member[0].text,
                int(member[4][0].text),
                int(member[4][1].text),
                int(member[4][2].text),
                int(member[4][3].text),
            )
            xml_list.append(value)
    column_name = [
        "filename",
        "width",
        "height",
        "class",
        "xmin",
        "ymin",
        "xmax",
        "ymax",
    ]
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    classes_names = list(set(classes_names))
    classes_names.sort()
    return xml_df, classes_names


def generate_labels(path, type):

    xml_df, classes_names = xml_to_csv(path)
    xml_df.to_csv(config.ANNOTATIONS_PATH + type + '_labels.csv', index=None)
    print("XML to CSV for {}: Yes".format(type))

    labels_path = os.path.join(config.ANNOTATIONS_PATH, "label_map.pbtxt")

    pbtxt_content = ""
    for i, class_name in enumerate(classes_names):
        pbtxt_content = (
                pbtxt_content
                + "item {{\n    id: {0}\n    name: '{1}'\n}}\n\n".format(
            i + 1, class_name
        )
        )
    pbtxt_content = pbtxt_content.strip()
    with open(labels_path, "w") as f:
        f.write(pbtxt_content)
    print("Label map for {}: Yes".format(type))


def main():
    # Create the annotation directory if it does not exists
    os.makedirs(os.path.dirname(config.ANNOTATIONS_PATH), exist_ok=True)

    # Generate labels for train images
    generate_labels(config.TRAIN_IMAGES_PATH, 'train')

    # Generate labels for test images
    generate_labels(config.TEST_IMAGES_PATH, 'test')


if __name__ == "__main__":
    main()
