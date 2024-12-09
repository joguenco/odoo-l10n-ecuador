# -*- coding: utf-8 -*-
import os
from sign import Sign


def main():
    print('Sign XML')
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.abspath(os.path.join(current_dir, '..', 'resources'))
    file_path = os.path.join(parent_dir, 'Hacker.p12')

    with open(file_path, 'rb') as p12_file:
        p12_data = p12_file.read()

        s = Sign(p12_data)
        private_key, certificate, additional_certs = s._decode_certificate('No_Piratear')

        print('Private Key:', private_key)
        print('Certificate:', certificate)
        if additional_certs:
            print('Additional Certificates:', additional_certs)


if __name__ == '__main__':
    main()
