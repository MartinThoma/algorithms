#!/usr/bin/env python

from dblp_parser import context_iter, log_msg, parse_article


def main():
    dblp_path = "dblp.xml"
    save_path = "article.json"
    try:
        context_iter(dblp_path)
        log_msg(f'LOG: Successfully loaded "{dblp_path}".')
    except OSError:
        log_msg(
            'ERROR: Failed to load file "{}". Please check your XML and DTD files.'.format(
                dblp_path
            )
        )
        exit()
    parse_article(dblp_path, save_path, save_to_csv=True)  # default save as json format


if __name__ == "__main__":
    main()
