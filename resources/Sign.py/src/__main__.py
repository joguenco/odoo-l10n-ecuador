# -*- coding: utf-8 -*-
import os
from xadessri import sign_xml
from xadessri import get_private_key
from sign import Sign
import xml.etree.ElementTree as ET


def main():
    print('Sign XML')
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.abspath(os.path.join(current_dir, '..', 'resources'))
    certificate_file_path = os.path.join(parent_dir, 'Hacker.p12')
    password = 'No_Piratear'
    xml_file_name = '0301202301123456789000110010030000000071234567811'
    xml_file_path = os.path.join(parent_dir, f'{xml_file_name}.xml')

    with open(certificate_file_path, 'rb') as p12_file:
        p12_data = p12_file.read()

        print('with xades-bes-sri')
        p12 = get_private_key(p12_data, password)
        print('Private Key:', p12.key)
        print('Certificate:', p12.cert)

        print('with Sign')
        s = Sign(p12_data)
        private_key, certificate, additional_certs = s._decode_certificate(password)
        print('Private Key:', private_key)
        print('Certificate:', certificate)
        if additional_certs:
            print('Additional Certificates:', additional_certs)

        with open(xml_file_path, 'r', encoding='utf-8') as file:
            xml_content = ''
            line = file.readline()

            while line:
                if '<?xml ' not in line:
                    xml_content += line
                line = file.readline()

            print(xml_content)
            signed = sign_xml(p12_data, password, xml_content)
            print('signed: ', signed)
            root = ET.fromstring(signed)
            tree = ET.ElementTree(root)
            xml_file_path_output = os.path.join(parent_dir, f'{xml_file_name}-signed.xml')
            tree.write(xml_file_path_output, encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    main()
