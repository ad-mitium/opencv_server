
def ver_info(version_info):
    version_number = '.'.join(str(c) for c in version_info)
    version = 'ver. '+version_number
    return version



if (__name__ == '__main__'):
    print(ver_info((0,0,0)))