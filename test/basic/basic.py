# encoding: utf-8

import core

if __name__ == '__main__':
    """
    A basic, non-threaded implementation of an application using the FTI library.
    What it does is simply:
        (1) Get the query from the user.
        (2) Transfer the query to the server, and get the available results.
        (3) Download every file one at a time.
    """
    print('Using FTI library version [{}]'.format(core.FtiVersion.get_version()))
    print('Use at your own risk!')
    text = input('Enter your query... ')
    print('Processing query [{}]'.format(text))
    p = Path(text)
    p.mkdir()
    query = core.FtiQuery()
    if query.process(text):
        results = query.get_results()
        print('Found [{}] result(s)...'.format(len(results)))
        for name, date in results:
            print('Downloading [{}]...'.format(name))
            file = core.FtiFile(name, date)
            if file.request_file():
                response = file.get_response()
                name2 = p / name
                with open(name2, 'wb') as f:
                    f.write(response.content)
            else:
                print('Unable to request the file')
    else:
        print('Unable to process the query properly')
