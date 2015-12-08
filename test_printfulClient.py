
import unittest
from printful import Printful, \
    PrintfulAPIException, PrintfulException

KEY = ''

SAMPLE_ORDER = { 'recipient':  {
                'name': 'John Doe',
                'address1': '172 W Providencia Ave #105',
                'city': 'Burbank',
                'state_code': 'CA',
                'country_code': 'US',
                'zip': '91502'
                },
                'items': [
                    {
                        'variant_id': 1, #Small poster
                        'name': 'Niagara Falls poster', #Display name
                        'retail_price': '19.99', #Retail price for packing slip
                        'quantity': 1,
                        'files': [
                            {'url': 'http://example.com/files/posters/poster_1.jpg'}
                        ]
                    },
                    {
                       'variant_id': 1118,
                       'quantity': 2,
                       'name': 'Grand Canyon T-Shirt', #Display name
                       'retail_price': '29.99', #Retail price for packing slip
                       'files': [
                            {'url': 'http://example.com/files/tshirts/shirt_front.ai'}, #Front print
                            {'type': 'back', 'url': 'http://example.com/files/tshirts/shirt_back.ai'}, #Back print
                            {'type': 'preview', 'url': 'http://example.com/files/tshirts/shirt_mockup.jpg'} #Mockup image
                       ],
                       'options': [ #Additional options
                            {'id': 'remove_labels', 'value': True}
                       ]
                    }
                ]
             }


SHIPPING_RATES = {  'recipient': {
                         'country_code': 'US',
                         'state_code': 'CA'
                     },
                     'items': [
                        {'variant_id': 1, 'quantity': 1},
                        {'variant_id': 1118, 'quantity': 2}
                     ]
                 }



class TestPrintfulClient(unittest.TestCase):
    
    def setUp(self):
        self.pf = Printful(KEY)

    def test_get_store_info(self):
        p = self.pf.get('store')
        self.assertEqual(p['code'], 200)
        self.assertTrue('result' in p)


    def test_get_product_list(self):
        p = self.pf.get('products')
        self.assertEqual(p['code'], 200)
        self.assertTrue('result' in p)


    def test_get_variants(self):
        """Get variants for product 10
        """
        prod = [('brand','American Apparel'),
                ('model', '2007 Unisex Fine Jersey Long Sleeve T-Shirt'),
                ('variant_count', 35)]
        p = self.pf.get('products/10')['result']['product']
        for k, v in prod:
            self.assertEqual(p[k], v)


    def test_get_variant_info_1007(self):
        """Get information about Variant 1007
        """
        prod = [('brand','American Apparel'),
                ('type', 'T-SHIRT'),
                ('variant_count', 35)]
        p = self.pf.get('products/variant/1007')['result']['product']
        for k, v in prod:
            self.assertEqual(p[k], v)


    def test_get_last_10_orders(self):
        """Select 10 latest orders and get the total number of orders
        """
        p = self.pf.get('orders', params={'offset': 5, 'limit':10})
        self.assertEqual(p['code'], 200)
        self.assertEqual(p['paging']['limit'], 10)
        self.assertEqual(p['paging']['offset'], 5)


    def test_get_order_info(self):
        """Select order with ID 12345 (Replace with your order's ID)
        """
        p = self.pf.get('orders/12345')
        pass


    def test_get_order_info_external(self):
        """Select order with External ID 9900999 (Replace with your order's External ID)
        """
        p = self.pf.get('orders/@9900999')
        pass


    def test_confirm_order(self):
        """Confirm order with ID 12345 (Replace with your order's ID)
        """
        p = self.pf.post('orders/12345/confirm')
        pass


    def test_shipping_rates(self):
        exp = {'currency': 'USD',
                'id': 'STANDARD',
                'name': 'Flat Rate (3-8 business days after fulfillment)',
                'rate': '14.20'}
        p = self.pf.post('shipping/rates', json=SHIPPING_RATES)
        self.assertEqual(p['code'], 200)
        for k in exp.keys():
            self.assertEqual(exp[k], p['result'][0][k])


    def test_create_order_and_delete(self):
        """This will create a dummy order and delete afterwards.
        """
        # create
        p = self.pf.post('orders', json=SAMPLE_ORDER)
        self.assertEqual(p['code'], 200)

        # delete
        order_id = p['result']['id']
        p = self.pf.delete('orders/{}'.format(order_id))


    def test_raise_bad_request(self):
        self.assertRaises(PrintfulAPIException, self.pf.get, 'fakeurl')

    def test_item_count(self):
        pf = self.pf.get('orders')
        item_count = self.pf.item_count()
        self.assertTrue(item_count > 0)



if __name__ == '__main__':
    unittest.main()