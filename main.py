import xml.etree.ElementTree as et


def tag_eval(tag, tag_depth):
    for subtag in tag.findall('*'):
        print('\t' * tag_depth + str(subtag.tag) + ':')
        tag_eval(subtag, tag_depth + 1)


if __name__ == '__main__':
    # Parse XML file
    tree = et.parse('wp_posts.xml')
    tag_eval(tree, 0)
