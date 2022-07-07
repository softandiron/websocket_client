from unittest import TestCase, main

from main import strip_key, convert_email, compose_payload


class ClientFunTest(TestCase):
    def test_stripper(self):
        self.assertEqual(strip_key('Key: n5AUbpMiEGV1WvAcgvjFdm75vDqrvFlm884ZN9IEBjJshGgOouCuNx'),
                         'n5AUbpMiEGV1WvAcgvjFdm75vDqrvFlm884ZN9IEBjJshGgOouCuNx')

    def test_converter(self):
        self.assertEqual(convert_email(b'n5AUbpMiEGV1WvAcgvjFdm75vDqrvFlm884ZN9IEBjJshGgOouCuNx',
                                       "minin.kp11@gmail.com"),
                         b"\x01\xac$5\x19IQ'V\xf2\xd5\xc0\x00\xa5;\x85Cs\xf5 "
                         b"\xd1\xc7\xc7\xc7\x9c\xa1%\x1dU\x8d\xad\xc5")

    def test_composer(self):
        self.assertEqual(compose_payload("minin.kp11@gmail.com",
                                         b"\x01\xac$5\x19IQ'V\xf2\xd5\xc0\x00\xa5;\x85Cs\xf5 "
                                         b"\xd1\xc7\xc7\xc7\x9c\xa1%\x1dU\x8d\xad\xc5"
                                         ),
                         b"minin.kp11@gmail.com:\x01\xac$5\x19IQ'V\xf2\xd5\xc0\x00\xa5;\x85Cs\xf5 "
                         b"\xd1\xc7\xc7\xc7\x9c\xa1%\x1dU\x8d\xad\xc5")


if __name__ == '__main__':
    main()
