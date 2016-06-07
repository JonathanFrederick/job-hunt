

def print_result(info):
    """Takes in a dictionary with keys for 'company', 'title', 'url',
    and 'description' and prints them neatly to the terminal"""

    for key in ['company', 'title', 'url', 'description']:
        assert key in info.keys(), \
            "The key '{}' is not in the dictionary".format(key)
        assert isinstance(info[key], str), \
            "The value at '{}' is not a string".format(key)

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
