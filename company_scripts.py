def print_result(info):
    """Takes in a dictionary with keys for 'company', 'title', 'url',
    and 'description' and prints them neatly to the terminal"""

    for key in ['company', 'title', 'url', 'description']:
        assert key in info.keys()
        assert isinstance(info[key], str)

    print('{} - {}'.format(info['company'], info['title']))
    print(info['url'])
    print(info['description'])


def main():
    print_result({'company': 'comp',
                  'title': 'title',
                  'url': 'url.com',
                  'description': 'things and stuff'})

if __name__ == "__main__":
    main()
