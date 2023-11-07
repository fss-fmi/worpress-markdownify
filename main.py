from xml.etree import ElementTree

import markdownify
from dateutil import parser as date


def tag_eval(tag, tag_depth):
    for subtag in tag.findall('*'):
        print('\t' * tag_depth + str(subtag.tag))
        tag_eval(subtag, tag_depth + 1)


def parse_post(tag):
    title = tag.find('title').text
    description = tag.find('description').text
    author = tag.find('{http://purl.org/dc/elements/1.1/}creator').text

    raw_pub_date = tag.find('pubDate').text
    pub_date = date.parse(raw_pub_date if raw_pub_date is not None else '2000-01-01')

    raw_content = tag.find('content').text
    content = markdownify.markdownify(raw_content if raw_content else '')

    return {"title": title, "description": description, "author": author, "pub_date": pub_date, "content": content}


if __name__ == '__main__':
    # Parse XML file
    tree = ElementTree.parse('wp_posts.xml')
    tag_eval(tree, 0)

    # Parse posts from tree
    parsed_posts = []
    for post_tag in tree.find('channel').findall('item'):
        parsed_posts.append(parse_post(post_tag))
        print(parsed_posts[-1]['content'])
