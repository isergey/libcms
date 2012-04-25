# -*- coding: utf-8 -*-
import datetime
from lxml import etree as ET
import uuid
import binascii
class ILLTransactions(object):
    def __init__(self):
        self.transactions = []


    def add_transaction(self, transaction):
        if isinstance(transaction, ILLTransaction):
            self.transactions.append(transaction)
        else:
            raise TypeError('Argument must be  ILLTransaction object')


    def from_xml(self, xml_string, transaction_tag='transaction'):
        try:
            tree = ET.XML(xml_string)
            for el_transaction in tree.findall(transaction_tag):

                self.add_transaction(ILLTransaction().from_xml(el_transaction))
        except SyntaxError as e:
            raise SyntaxError('Not valid xml: ' + e.message)

        return self


    def to_xml(self, as_element=False):
        if len(self.transactions) == 0:
            return None

        root = ET.Element('transactions')

        for transaction in self.transactions:
            root.append(transaction.to_xml(True))

        if as_element == False:
            return ET.tostring(root, encoding='UTF-8')
        else:
            return root




class ILLTransaction(object):
    def __init__(self, status='new', seen=''):
        self.status = status
        self.seen = seen
        self.illapdus = []

    def add_illapdu(self, illapdu):
        if isinstance(illapdu, ILLAPDU):
            self.illapdus.append(illapdu)
        else:
            raise TypeError('Argument must be  ILLAPDU object')

    def from_xml(self, xml_transaction):
        if isinstance(xml_transaction, str) or isinstance(xml_transaction, unicode):
            try:
                tree = ET.XML(xml_transaction)
            except SyntaxError as e:
                raise SyntaxError('Not valid xml: ' + e.message)
        # иначе проверим является ли объект типа Element
        else:
            print type(xml_transaction)
            if type(xml_transaction) == ET._Element:
                tree = xml_transaction
            else:
                raise TypeError('xml_transaction must be str or unicode or Element type')

        status = tree.get('status')
        if status: self.status = status

        seen = tree.get('seen')
        if seen: self.seen = seen

        for el_illapdu in tree.findall('ILLAPDU'):
            apdu = ILLAPDU().from_xml(el_illapdu)
            if apdu != None:
                self.add_illapdu(apdu)

        return self

    def to_xml(self, as_element=False):
        if len(self.illapdus) == 0:
            return None

        root = ET.Element('transaction')
        root.set('status',self.status)
        if self.seen != '':
            root.set('seen',self.seen)


        for illapdu in self.illapdus:
            root.append(illapdu.to_xml(True))
        if as_element == False:
            return ET.tostring(root, encoding='UTF-8')
        else:
            return root




class ILLAPDU(object):
    def __init__(self):
        self.type = 'ILLAPDU'
        self.delivery_status = None


    def set_delivery_status(self, status):
        if isinstance(status, ILLRequest) or\
           isinstance(status, ILLShipped) or\
           isinstance(status, ILLAnswer) or\
           isinstance(status, Recall):
            self.delivery_status = status
        else:
            raise TypeError('Wrong type object. Must be ILLRequest, ILLRequest or ILLAnswer type')


    def from_xml(self, xml_illapdu):

        if isinstance(xml_illapdu, str) or isinstance(xml_illapdu, unicode):
            try:
                tree = ET.XML(xml_illapdu)
            except SyntaxError as e:
                raise SyntaxError('Not valid xml: ' + e.message)
        # иначе проверим является ли объект типа Element
        else:
            if type(xml_illapdu) == ET._Element:
                tree = xml_illapdu
            else:
                raise TypeError('xml_illapdu must be str or unicode or Element type')

        el_delivery_status = xml_illapdu.find('ILLRequest')
        if el_delivery_status:
            self.set_delivery_status(ILLRequest().from_xml(el_delivery_status))

        el_delivery_status = xml_illapdu.find('Shipped')
        if el_delivery_status:
            self.set_delivery_status(ILLShipped().from_xml(el_delivery_status))

        el_delivery_status = xml_illapdu.find('ILLAnswer')
        if el_delivery_status:
            self.set_delivery_status(ILLAnswer().from_xml(el_delivery_status))

        el_delivery_status = xml_illapdu.find('Recall')
        if el_delivery_status:
            self.set_delivery_status(Recall().from_xml(el_delivery_status))

        if self.delivery_status == None:
            return None
            #raise TypeError('Wrong type xml_illapdu. Must be str or unicode or Element type')

        return self


    def to_xml(self, as_element=False):

        if self.delivery_status == None:
            return None

        root = ET.Element(self.type)
        root.append(self.delivery_status.to_xml(True))

        if as_element == False:
            return ET.tostring(root, encoding='UTF-8')
        else:
            return root



class ILLRequest(object):
    def __init__(self):
        self.type = 'ILLRequest'
        self.protocol_version_num = '2' # protocolVersionNum
        self.transaction_id = {# transactionId
                               'tgq': None, # transactionGroupQualifier
                               'tq': str(binascii.crc32(str(uuid.uuid4()))&0xffffffff) # transactionQualifier
        }

        now = datetime.datetime.now()
        self.service_date_time = {
            'dtots':{# dateTimeOfThisService
                     'date': now.strftime("%Y%m%d"),
                     'time': now.strftime("%H%M%S"),
                     }
        }

        self.requester_id = {
            'pois': {# personOrInstitutionSymbol
                     'is': None # institutionSymbol
            }
        }

        self.responder_id = {
            'pois': {# personOrInstitutionSymbol
                     'is': None # institutionSymbol
            }
        }

        self.transaction_type = '1' # transactionType
        self.ill_service_type = '1' # iLLServiceType

        self.requester_optional_messages = {# requesterOptionalMessages
                                            'csrec': '0', # canSendRECEIVED
                                            'csret': '0', # canSendRETURNED
                                            'rs': '2', # requesterSHIPPED
                                            'rc': '2', # requesterCHECKEDIN
        }

        self.place_on_hold = '3' # placeOnHold

        self.item_id = {# itemId
                        'it': '3', # itemType
                        'pagination': '' # pagination
        }

        self.retry_flag = '0' # retryFlag
        self.forward_flag = '0' # forwardFlag

        self.supplemental_item_description = None # тут вставим марк xml
        self.requester_note = '' # requesterNote

        self.third_party_info_type = { # thirdPartyInfoType
                                       'tpit':{
                                           'stl':{ #sendToList
                                                   'stlt':{
                                                       'si':'' # systemId
                                                   }
                                           }
                                       }
        }
    def from_xml(self, xml_illrequest):
        if isinstance(xml_illrequest, str) or isinstance(xml_illrequest, unicode):
            try:
                tree = ET.XML(xml_illrequest)
            except SyntaxError as e:
                raise SyntaxError('Not valid xml: ' + e.message)
        # иначе проверим является ли объект типа Element
        else:
            if type(xml_illrequest) == ET._Element:
                tree = xml_illrequest
            else:
                raise TypeError('xml_illrequest must be str or unicode or Element type')


        temp_text = tree.findtext('protocolVersionNum')
        if temp_text:
            self.protocol_version_num = temp_text

        temp_text = tree.findtext('transactionId/transactionGroupQualifier')
        if temp_text:
            self.transaction_id['tgq'] = temp_text

        temp_text = tree.findtext('transactionId/transactionQualifier')
        if temp_text:
            self.transaction_id['tq'] = temp_text

        temp_text = tree.findtext('serviceDateTime/dateTimeOfThisService/date')
        if temp_text:
            self.service_date_time['dtots']['date'] = temp_text

        temp_text = tree.findtext('serviceDateTime/dateTimeOfThisService/time')
        if temp_text:
            self.service_date_time['dtots']['time'] = temp_text

        temp_text = tree.findtext('requesterId/personOrInstitutionSymbol/institutionSymbol')
        if temp_text:
            self.requester_id['pois']['is'] = temp_text

        temp_text = tree.findtext('responderId/personOrInstitutionSymbol/institutionSymbol')
        if temp_text:
            self.responder_id['pois']['is'] = temp_text

        temp_text = tree.findtext('transactionType')
        if temp_text:
            self.transaction_type = temp_text

        temp_text = tree.findtext('iLLServiceType')
        if temp_text:
            self.ill_service_type = temp_text

        temp_text = tree.findtext('requesterOptionalMessages/canSendRECEIVED')
        if temp_text:
            self.requester_optional_messages['csrec'] = temp_text

        temp_text = tree.findtext('requesterOptionalMessages/canSendRETURNED')
        if temp_text:
            self.requester_optional_messages['csret'] = temp_text

        temp_text = tree.findtext('requesterOptionalMessages/requesterSHIPPED')
        if temp_text:
            self.requester_optional_messages['rs'] = temp_text

        temp_text = tree.findtext('requesterOptionalMessages/requesterCHECKEDIN')
        if temp_text:
            self.requester_optional_messages['rc'] = temp_text

        temp_text = tree.findtext('placeOnHold')
        if temp_text:
            self.place_on_hold = temp_text

        temp_text = tree.findtext('itemId/itemType')
        if temp_text:
            self.item_id['it'] = temp_text

        temp_text = tree.findtext('itemId/pagination')
        if temp_text:
            self.item_id['pagination'] = temp_text

        temp_text = tree.findtext('retryFlag')
        if temp_text:
            self.retry_flag = temp_text

        temp_text = tree.findtext('forwardFlag')
        if temp_text:
            self.forward_flag = temp_text

        el_supplemental_item_description = tree.find('supplementalItemDescription/external/*')
        if el_supplemental_item_description:
            self.supplemental_item_description = el_supplemental_item_description

        temp_text = tree.findtext('requesterNote')
        if temp_text:
            self.requester_note = temp_text

        temp_text = tree.findtext('thirdPartyInfoType/sendToList/sendToListType/systemId')

        if temp_text:
            self.third_party_info_type['tpit']['stl']['stlt']['si'] = temp_text


        return self

    def to_xml(self, as_element=False):
        """
        Преобразует ILLRequest в XML строку или Element
        as_element=Flase: возвращается XML строка
        as_element=True: возвращается xml.etree.cElementTree.Element объект
        """
        root = ET.Element(self.type)

        protocol_version_num = ET.SubElement(root, "protocolVersionNum")
        protocol_version_num.text = str(self.protocol_version_num)

        transaction_id = ET.SubElement(root, "transactionId")
        tgq = ET.SubElement(transaction_id, "transactionGroupQualifier")
        tgq.text = str(self.transaction_id['tgq'])
        tq = ET.SubElement(transaction_id, "transactionQualifier")
        tq.text = str(self.transaction_id['tq'])

        dtots = ET.SubElement(root, "serviceDateTime")
        service_date_time = ET.SubElement(dtots, "dateTimeOfThisService")
        date = ET.SubElement(service_date_time, "date")
        date.text = str(self.service_date_time['dtots']['date'])
        time = ET.SubElement(service_date_time, "time")
        time.text = str(self.service_date_time['dtots']['time'])

        requester_id = ET.SubElement(root, "requesterId")
        pois = ET.SubElement(requester_id, "personOrInstitutionSymbol")
        institution_symbol = ET.SubElement(pois, "institutionSymbol")
        institution_symbol.text = str(self.requester_id['pois']['is'])

        responder_id = ET.SubElement(root, "responderId")
        rpois = ET.SubElement(responder_id, "personOrInstitutionSymbol")
        rinstitution_symbol = ET.SubElement(rpois, "institutionSymbol")
        rinstitution_symbol.text = str(self.responder_id['pois']['is'])

        transactionType = ET.SubElement(root, "transactionType")
        transactionType.text = str(self.transaction_type)

        ill_service_type = ET.SubElement(root, "iLLServiceType")
        ill_service_type.text = str(self.ill_service_type)

        requester_optional_messages = ET.SubElement(root, "requesterOptionalMessages")
        csrec = ET.SubElement(requester_optional_messages, "canSendRECEIVED")
        csrec.text = str(self.requester_optional_messages['csrec'])
        csret = ET.SubElement(requester_optional_messages, "canSendRETURNED")

        csret.text = str(self.requester_optional_messages['csret'])
        rs = ET.SubElement(requester_optional_messages, "requesterSHIPPED")
        rs.text = str(self.requester_optional_messages['rs'])
        rc = ET.SubElement(requester_optional_messages, "requesterCHECKEDIN")
        rc.text = str(self.requester_optional_messages['rc'])

        place_on_hold = ET.SubElement(root, "placeOnHold")
        place_on_hold.text = str(self.place_on_hold)

        item_id = ET.SubElement(root, "itemId")
        item_type = ET.SubElement(item_id, "itemType")
        item_type.text = str(self.item_id['it'])
        if self.item_id['pagination']:
            pagination = ET.SubElement(item_id, "pagination")
            pagination.text = self.item_id['pagination']

        retry_flag = ET.SubElement(root, "retryFlag")
        retry_flag.text = str(self.retry_flag)

        forward_flag = ET.SubElement(root, "forwardFlag")
        forward_flag.text = str(self.forward_flag)

        if self.supplemental_item_description:
        # если строка XML то преобразуем в Element
            if isinstance(self.supplemental_item_description, str) or\
               isinstance(self.supplemental_item_description, unicode):
                try:
                    if isinstance(self.supplemental_item_description, unicode):
                        self.supplemental_item_description = self.supplemental_item_description.encode('UTF-8')
                    sid = ET.XML(self.supplemental_item_description)
                except SyntaxError as e:
                    raise SyntaxError('Not valid xml: ' + e.message)
                    # иначе проверим является ли объект типа Element
            else:
                if type(self.supplemental_item_description) == ET._Element:
                    sid = self.supplemental_item_description
                else:
                    raise TypeError('supplemental_item_description must be str or unicode or Element type')
            supplemental_item_description = ET.SubElement(root, "supplementalItemDescription")
            external = ET.SubElement(supplemental_item_description, "external")

            external_syntax = sid.get('syntax')
            if external_syntax:
                external.set('syntax', external_syntax)
            else:
                external.set('syntax', 'unknown')

            external.append(sid)

        if self.requester_note:
            requester_note = ET.SubElement(root, "requesterNote")
            requester_note.text = self.requester_note

        if self.third_party_info_type['tpit']['stl']['stlt']['si']:
            third_party_info_type = ET.SubElement(root, "thirdPartyInfoType")
            send_to_list = ET.SubElement(third_party_info_type, "sendToList")
            send_to_list_type = ET.SubElement(send_to_list, "sendToListType")
            si = ET.SubElement(send_to_list_type, "systemId")
            si.text = str(self.third_party_info_type['tpit']['stl']['stlt']['si'])
        if as_element == False:
            return ET.tostring(root, encoding='UTF-8')
        else:
            return root



class ILLShipped(object):
    def __init__(self):
        self.type = 'Shipped'
        self.protocol_version_num = '2'
        self.transaction_id = {
            'tgq': None, # transactionGroupQualifier
            'tq': None # transactionQualifier
        }

        now = datetime.datetime.now()
        self.service_date_time = {
            'dtots':{# dateTimeOfThisService
                     'date': now.strftime("%Y%m%d"),
                     'time': now.strftime("%H%M%S"),
                     }
        }

        self.requester_id = {
            'pois': {# personOrInstitutionSymbol
                     'is': None # institutionSymbol
            }
        }

        self.responder_id = {
            'pois': {# personOrInstitutionSymbol
                     'is': None # institutionSymbol
            }
        }

        self.transaction_type = '1'
        self.shipped_service_type = '1' # shippedServiceType

        self.supply_details = { # supplyDetails
                                'ds':None, #dateShipped
                                'dd': {# dateDue
                                       'ddf': None, # dateDueField
                                       'renewable': None, # renewable
                                }
        }
        self.responder_note = '' # responderNote

    def from_xml(self, xml_shipped):
        if isinstance(xml_shipped, str) or isinstance(xml_shipped, unicode):
            try:
                tree = ET.XML(xml_shipped)
            except SyntaxError as e:
                raise SyntaxError('Not valid xml: ' + e.message)
        # иначе проверим является ли объект типа Element
        else:
            if type(xml_shipped) == ET._Element:
                tree = xml_shipped
            else:
                raise TypeError('xml_shipped must be str or unicode or Element type')


        temp_text = tree.findtext('protocolVersionNum')
        if temp_text:
            self.protocol_version_num = temp_text

        temp_text = tree.findtext('transactionId/transactionGroupQualifier')
        if temp_text:
            self.transaction_id['tgq'] = temp_text

        temp_text = tree.findtext('transactionId/transactionQualifier')
        if temp_text:
            self.transaction_id['tq'] = temp_text

        temp_text = tree.findtext('serviceDateTime/dateTimeOfThisService/date')
        if temp_text:
            self.service_date_time['dtots']['date'] = temp_text

        temp_text = tree.findtext('serviceDateTime/dateTimeOfThisService/time')
        if temp_text:
            self.service_date_time['dtots']['time'] = temp_text

        temp_text = tree.findtext('requesterId/personOrInstitutionSymbol/institutionSymbol')
        if temp_text:
            self.requester_id['pois']['is'] = temp_text

        temp_text = tree.findtext('responderId/personOrInstitutionSymbol/institutionSymbol')
        if temp_text:
            self.responder_id['pois']['is'] = temp_text

        temp_text = tree.findtext('transactionType')
        if temp_text:
            self.transaction_type = temp_text

        temp_text = tree.findtext('shippedServiceType')
        if temp_text:
            self.shipped_service_type = temp_text

        temp_text = tree.findtext('supplyDetails/dateShipped')
        if temp_text:
            self.supply_details['ds'] = temp_text

        temp_text = tree.findtext('supplyDetails/dateDue/dateDueField')
        if temp_text:
            self.supply_details['dd']['ddf'] = temp_text

        temp_text = tree.findtext('supplyDetails/dateDue/renewable')
        if temp_text:
            self.supply_details['dd']['renewable'] = temp_text

        temp_text = tree.findtext('responderNote')
        if temp_text:
            self.responder_note = temp_text
        return self

    def to_xml(self, as_element=False):
        """
        Преобразует ILLShipped в XML строку или Element
        as_element=Flase: возвращается XML строка
        as_element=True: возвращается xml.etree.cElementTree.Element объект
        """
        root = ET.Element(self.type)

        protocol_version_num = ET.SubElement(root, "protocolVersionNum")
        protocol_version_num.text = str(self.protocol_version_num)

        transaction_id = ET.SubElement(root, "transactionId")
        tgq = ET.SubElement(transaction_id, "transactionGroupQualifier")
        tgq.text = str(self.transaction_id['tgq'])
        tq = ET.SubElement(transaction_id, "transactionQualifier")
        tq.text = str(self.transaction_id['tq'])

        dtots = ET.SubElement(root, "serviceDateTime")
        service_date_time = ET.SubElement(dtots, "dateTimeOfThisService")
        date = ET.SubElement(service_date_time, "date")
        date.text = str(self.service_date_time['dtots']['date'])
        time = ET.SubElement(service_date_time, "time")
        time.text = str(self.service_date_time['dtots']['time'])

        requester_id = ET.SubElement(root, "requesterId")
        pois = ET.SubElement(requester_id, "personOrInstitutionSymbol")
        institution_symbol = ET.SubElement(pois, "institutionSymbol")
        institution_symbol.text = str(self.requester_id['pois']['is'])

        responder_id = ET.SubElement(root, "responderId")
        rpois = ET.SubElement(responder_id, "personOrInstitutionSymbol")
        rinstitution_symbol = ET.SubElement(rpois, "institutionSymbol")
        rinstitution_symbol.text = str(self.responder_id['pois']['is'])

        transactionType = ET.SubElement(root, "transactionType")
        transactionType.text = str(self.transaction_type)

        shipped_service_type = ET.SubElement(root, "iLLServiceType")
        shipped_service_type.text = str(self.shipped_service_type)

        supply_details = ET.SubElement(root, "supplyDetails")
        ds = ET.SubElement(supply_details, "dateShipped")
        ds.text = str(self.supply_details['ds'])
        dd = ET.SubElement(ds, "dateDue")
        ddf = ET.SubElement(dd, "dateDueField")
        ddf.text = str(self.supply_details['dd']['ddf'])
        renewable = ET.SubElement(dd, "renewable")
        renewable.text = str(self.supply_details['dd']['renewable'])

        if self.responder_note:
            responder_note = ET.SubElement(root, "responderNote")
            responder_note.text = self.responder_note

        if as_element == False:
            return ET.tostring(root, encoding='UTF-8')
        else:
            return root


class ILLAnswer(object):
    def __init__(self):
        self.type = 'ILLAnswer'
        self.protocol_version_num = '2'
        self.transaction_id = {
            'tgq': None, # transactionGroupQualifier
            'tq': None # transactionQualifier
        }

        now = datetime.datetime.now()
        self.service_date_time = {
            'dtots':{# dateTimeOfThisService
                     'date': now.strftime("%Y%m%d"),
                     'time': now.strftime("%H%M%S"),
                     }
        }

        self.requester_id = {
            'pois': {# personOrInstitutionSymbol
                     'is': None # institutionSymbol
            }
        }

        self.responder_id = {
            'pois': {# personOrInstitutionSymbol
                     'is': None # institutionSymbol
            }
        }

        self.results_explanation = {# resultsExplanation
                                    'ur': {# unfilledResults
                                           'ru': '' # reasonUnfilled
                                    },
                                    'wsr': { #willSupplyResults
                                             'rws': '' #reasonWillSupply
                                    }
        }

        self.responder_note = ''



    def to_xml(self, as_element=False):
        root = ET.Element(self.type)

        protocol_version_num = ET.SubElement(root, "protocolVersionNum")
        protocol_version_num.text = str(self.protocol_version_num)

        transaction_id = ET.SubElement(root, "transactionId")
        tgq = ET.SubElement(transaction_id, "transactionGroupQualifier")
        tgq.text = str(self.transaction_id['tgq'])
        tq = ET.SubElement(transaction_id, "transactionQualifier")
        tq.text = str(self.transaction_id['tq'])

        dtots = ET.SubElement(root, "serviceDateTime")
        service_date_time = ET.SubElement(dtots, "dateTimeOfThisService")
        date = ET.SubElement(service_date_time, "date")
        date.text = str(self.service_date_time['dtots']['date'])
        time = ET.SubElement(service_date_time, "time")
        time.text = str(self.service_date_time['dtots']['time'])

        requester_id = ET.SubElement(root, "requesterId")
        pois = ET.SubElement(requester_id, "personOrInstitutionSymbol")
        institution_symbol = ET.SubElement(pois, "institutionSymbol")
        institution_symbol.text = str(self.requester_id['pois']['is'])

        responder_id = ET.SubElement(root, "responderId")
        rpois = ET.SubElement(responder_id, "personOrInstitutionSymbol")
        rinstitution_symbol = ET.SubElement(rpois, "institutionSymbol")
        rinstitution_symbol.text = str(self.responder_id['pois']['is'])

        results_explanation = ET.SubElement(root, "resultsExplanation")
        ur = ET.SubElement(results_explanation, "unfilledResults")
        ru = ET.SubElement(ur, "reasonUnfilled")
        ru.text = str(self.results_explanation['ur']['ru'])

        if self.results_explanation['wsr']['rws']:
            wsr = ET.SubElement(results_explanation, "willSupplyResults")
            rws = ET.SubElement(wsr, "reasonWillSupply")
            rws.text = str(self.results_explanation['wsr']['rws'])

        if self.responder_note:
            responder_note = ET.SubElement(root, "responderNote")
            responder_note.text = str(self.responder_note)

        if as_element == False:
            return ET.tostring(root, encoding='UTF-8')
        else:
            return root

    def from_xml(self, xml_illanswer):

        if isinstance(xml_illanswer, str) or isinstance(xml_illanswer, unicode):
            try:
                tree = ET.XML(xml_illanswer)
            except SyntaxError as e:
                raise SyntaxError('Not valid xml: ' + e.message)
        # иначе проверим является ли объект типа Element
        else:
            if type(xml_illanswer) == ET._Element:
                tree = xml_illanswer
            else:
                raise TypeError('xml_illanswer must be str or unicode or Element type')

        temp_text = tree.findtext('protocolVersionNum')
        if temp_text:
            self.protocol_version_num = temp_text

        temp_text = tree.findtext('transactionId/transactionGroupQualifier')
        if temp_text:
            self.transaction_id['tgq'] = temp_text

        temp_text = tree.findtext('transactionId/transactionQualifier')
        if temp_text:
            self.transaction_id['tq'] = temp_text

        temp_text = tree.findtext('serviceDateTime/dateTimeOfThisService/date')
        if temp_text:
            self.service_date_time['dtots']['date'] = temp_text

        temp_text = tree.findtext('serviceDateTime/dateTimeOfThisService/time')
        if temp_text:
            self.service_date_time['dtots']['time'] = temp_text

        temp_text = tree.findtext('requesterId/personOrInstitutionSymbol/institutionSymbol')
        if temp_text:
            self.requester_id['pois']['is'] = temp_text

        temp_text = tree.findtext('responderId/personOrInstitutionSymbol/institutionSymbol')
        if temp_text:
            self.responder_id['pois']['is'] = temp_text

        temp_text = tree.findtext('resultsExplanation/unfilledResults/reasonUnfilled')
        if temp_text:
            self.results_explanation['ur']['ru'] = temp_text

        temp_text = tree.findtext('resultsExplanation/willSupplyResults/reasonWillSupply')
        if temp_text:
            self.results_explanation['wsr']['rws'] = temp_text

        temp_text = tree.findtext('responderNote')
        if temp_text:
            self.responder_note = temp_text

        return self

class Recall(object):
    def __init__(self):
        self.type = 'Recall'
        self.protocol_version_num = '2'
        self.transaction_id = {
            'tgq': None, # transactionGroupQualifier
            'tq': None # transactionQualifier
        }

        now = datetime.datetime.now()
        self.service_date_time = {
            'dtots':{# dateTimeOfThisService
                     'date': now.strftime("%Y%m%d"),
                     'time': now.strftime("%H%M%S"),
                     }
        }

        self.requester_id = {
            'pois': {# personOrInstitutionSymbol
                     'is': None # institutionSymbol
            }
        }

        self.responder_id = {
            'pois': {# personOrInstitutionSymbol
                     'is': None # institutionSymbol
            }
        }

        self.responder_note = ''


    def to_xml(self, as_element=False):
        root = ET.Element(self.type)

        protocol_version_num = ET.SubElement(root, "protocolVersionNum")
        protocol_version_num.text = str(self.protocol_version_num)

        transaction_id = ET.SubElement(root, "transactionId")
        tgq = ET.SubElement(transaction_id, "transactionGroupQualifier")
        tgq.text = str(self.transaction_id['tgq'])
        tq = ET.SubElement(transaction_id, "transactionQualifier")
        tq.text = str(self.transaction_id['tq'])

        dtots = ET.SubElement(root, "serviceDateTime")
        service_date_time = ET.SubElement(dtots, "dateTimeOfThisService")
        date = ET.SubElement(service_date_time, "date")
        date.text = str(self.service_date_time['dtots']['date'])
        time = ET.SubElement(service_date_time, "time")
        time.text = str(self.service_date_time['dtots']['time'])

        requester_id = ET.SubElement(root, "requesterId")
        pois = ET.SubElement(requester_id, "personOrInstitutionSymbol")
        institution_symbol = ET.SubElement(pois, "institutionSymbol")
        institution_symbol.text = str(self.requester_id['pois']['is'])

        responder_id = ET.SubElement(root, "responderId")
        rpois = ET.SubElement(responder_id, "personOrInstitutionSymbol")
        rinstitution_symbol = ET.SubElement(rpois, "institutionSymbol")
        rinstitution_symbol.text = str(self.responder_id['pois']['is'])

        if self.responder_note:
            responder_note = ET.SubElement(root, "responderNote")
            responder_note.text = str(self.responder_note)

        if as_element == False:
            return ET.tostring(root, encoding='UTF-8')
        else:
            return root

    def from_xml(self, xml_illanswer):

        if isinstance(xml_illanswer, str) or isinstance(xml_illanswer, unicode):
            try:
                tree = ET.XML(xml_illanswer)
            except SyntaxError as e:
                raise SyntaxError('Not valid xml: ' + e.message)
        # иначе проверим является ли объект типа Element
        else:
            if type(xml_illanswer) == ET._Element:
                tree = xml_illanswer
            else:
                raise TypeError('xml_illanswer must be str or unicode or Element type')

        temp_text = tree.findtext('protocolVersionNum')
        if temp_text:
            self.protocol_version_num = temp_text

        temp_text = tree.findtext('transactionId/transactionGroupQualifier')
        if temp_text:
            self.transaction_id['tgq'] = temp_text

        temp_text = tree.findtext('transactionId/transactionQualifier')
        if temp_text:
            self.transaction_id['tq'] = temp_text

        temp_text = tree.findtext('serviceDateTime/dateTimeOfThisService/date')
        if temp_text:
            self.service_date_time['dtots']['date'] = temp_text

        temp_text = tree.findtext('serviceDateTime/dateTimeOfThisService/time')
        if temp_text:
            self.service_date_time['dtots']['time'] = temp_text

        temp_text = tree.findtext('requesterId/personOrInstitutionSymbol/institutionSymbol')
        if temp_text:
            self.requester_id['pois']['is'] = temp_text

        temp_text = tree.findtext('responderId/personOrInstitutionSymbol/institutionSymbol')
        if temp_text:
            self.responder_id['pois']['is'] = temp_text

        temp_text = tree.findtext('responderNote')
        if temp_text:
            self.responder_note = temp_text

        return self