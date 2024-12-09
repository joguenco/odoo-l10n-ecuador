from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.backends import default_backend


class Sign:
    def __init__(self, file_content):
        self.p12_data = file_content

    def _decode_certificate(self, password):
        private_key, certificate, additional_certs = pkcs12.load_key_and_certificates(
            self.p12_data, password.encode(), backend=default_backend()
        )

        return private_key, certificate, additional_certs
