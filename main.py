import os
from shlex import quote
from xml.etree import ElementTree

import markdownify
from caseconverter import kebabcase
from dateutil import parser as date


def tag_eval(tag, tag_depth):
    for subtag in tag.findall('*'):
        print('\t' * tag_depth + str(subtag.tag))
        tag_eval(subtag, tag_depth + 1)


def parse_post(tag):
    raw_title = tag.find('title').text
    title = raw_title if raw_title else ''

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

    # Parse posts from tree
    posts = []
    for post_tag in tree.find('channel').findall('item'):
        posts.append(parse_post(post_tag))

    # Load template
    template = ''
    with open('news.template', 'r') as template_file:
        template = template_file.read()

    # Create markdown files for posts
    out_dir = 'out'
    for post in posts:
        filepath = "{}/{:02d}/{:02d}/{}.md".format(out_dir, post['pub_date'].year, post['pub_date'].month,
                                                   kebabcase(post['title']))
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as md_file:
            md_file.write(
                template.format(title=quote(post["title"]), description=quote(post["description"]),
                                author=quote(post["author"]), pub_date=post["pub_date"], content=post["content"]))
