# -*- coding: utf-8 -*-
import subprocess


from libs.ill import ILLRequest, ILLAPDU, ILLTransaction, ILLTransactions
import xml.etree.cElementTree as ET

import urllib
class OrderManagerException(Exception): pass

class OrderManager(object):
    def __init__(self, db_catalog, rdx_path='/usr/local/bin/rdx'):
        self.db_catalog = db_catalog
        self.rdx_path = rdx_path



    def insert_record(self, container_name, record):
        env = {
            'LD_LIBRARY_PATH':'/usr/local/lib',
            'RDBXML_DATA': self.db_catalog
        }

        proc = subprocess.Popen([self.rdx_path, container_name, 'write'], stdin = subprocess.PIPE,
                                stdout = subprocess.PIPE, stderr=subprocess.PIPE,
                                env=env
        )

        
        proc.stdin.write(record)
        proc.stdin.close()
        error = proc.stderr.read()
        proc.stderr.close()
        if error:
            raise OrderManagerException(error)

    
    def get_results(self, container_name, query_string):

        env = {
            'LD_LIBRARY_PATH':'/usr/local/lib',
            'RDBXML_DATA': self.db_catalog
        }

        proc = subprocess.Popen([self.rdx_path, container_name, 'query', query_string], stdin = subprocess.PIPE,
                                stdout = subprocess.PIPE, stderr=subprocess.PIPE, env=env
        )


        transactions =  proc.stdout.read()

        error = proc.stderr.read()
        if error:
            raise OrderManagerException(error)
        
        if transactions:
            root = ET.XML(transactions)
            return list(root)
        else:
            return []

    def delete_record(self, container_name, query_string):
        env = {
            'LD_LIBRARY_PATH':'/usr/local/lib',
            'RDBXML_DATA': self.db_catalog
        }

        proc = subprocess.Popen([self.rdx_path, container_name, 'delete', query_string], stderr=subprocess.PIPE, env=env)
        error = proc.stderr.read()
        if error:
            raise OrderManagerException(error)
        
    def order_document(self, order_type, sender_id, reciver_id, xml_record, copy_doc_reciver_id='', comments='', copy_info='', manager_id=''):
        """
        copy_doc_reciver_id  - конечная организация получатель
        order_type document || copy || reserver
        """
        sender_id = sender_id.encode('utf-8')
        reciver_id = reciver_id.encode('utf-8')
        
        ill_request = ILLRequest()
        ill_request.requester_id['pois']['is'] = sender_id # id пользователя
        ill_request.responder_id['pois']['is'] = reciver_id # id первичного получателя
        ill_request.third_party_info_type['tpit']['stl']['stlt']['si'] = manager_id # id конечного получателя
        ill_service_type = '1'
        if order_type == 'document':
            ill_service_type = '1'
        elif order_type == 'copy':
            ill_service_type = '2'
        elif order_type == 'reserve':
            ill_service_type = '5'
        
        if order_type != 'copy':
            copy_comments = ''
            
        #if (ill_service_type == '1' or ill_service_type == '2') and not copy_doc_reciver_id:
        #    raise Exception('copy_doc_reciver_id not defined in reservation')
                
        ill_request.ill_service_type = ill_service_type # заказываем документ (2) - копия
        ill_request.supplemental_item_description = xml_record
        ill_request.requester_note = comments
        ill_request.transaction_id['tgq'] = sender_id
        ill_request.third_party_info_type['tpit']['stl']['stlt']['si'] = manager_id
        ill_request.item_id['pagination'] = copy_info
        apdu = ILLAPDU()
        apdu.set_delivery_status(ill_request)

        transaction = ILLTransaction()
        transaction.add_illapdu(apdu)
        container_name = self.db_catalog + '/' + str(reciver_id) + ".user"
        user_container_name = self.db_catalog + '/' + sender_id + ".orders"

        self.insert_record(container_name, transaction.to_xml())
        self.insert_record(user_container_name, transaction.to_xml())




    def get_orders(self, user_id):
        results_by_org = {}
        query_string = "/*"
        query_params = {}

        container_name = '%s.orders' % user_id.encode('utf-8')
        results = self.get_results(container_name, query_string)

        transactions = [ ILLTransaction().from_xml(result) for result in results ]

        return  transactions

    def get_order(self, order_id='', user_id=''):


        query_string = "/transaction/ILLAPDU/ILLRequest/transactionId[transactionQualifier=%s]" % order_id
        container_name = '%s.orders' % user_id.encode('utf-8')

        results = self.get_results(container_name, query_string)

        transactions = [ ILLTransaction().from_xml(result) for result in results ]

        return transactions

    def delete_order(self, order_id, user_id):
        query_string = "/transaction[ILLAPDU/ILLRequest/transactionId/transactionQualifier=%s]" % order_id
        container_name = '%s.orders' % str(user_id)
        self.delete_record(container_name,query_string)


