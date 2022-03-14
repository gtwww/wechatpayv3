# -*- coding: utf-8 -*-
import os.path

from .type import RequestType
from .utils import SM3


def fapiao_card_template(self, card_template_information, card_appid=None):
    """创建电子发票卡券模板
    :param card_template_information: 卡券模板信息。示例值:{'logo_url':'http://mmbiz.qpic.cn/mmbiz/iaL1LJM1mF9aRKPZJkmG8xX'}
    :param card_appid: 插卡公众号AppID，若是服务商模式，则可以是服务商申请的appid，也可以是子商户申请的appid；若是直连模式，则是直连商户申请的appid。示例值：wxb1170446a4c0a5a2
    """
    if not card_appid:
        card_appid = self._appid
    params = {}
    params.update({'card_appid': card_appid})
    if card_template_information:
        params.update({'card_template_information': card_template_information})
    else:
        raise Exception('card_template_information is not assigned.')
    path = '/v3/new-tax-control-fapiao/card-template'
    return self._core.request(path, method=RequestType.POST, data=params)


def fapiao_set_merchant_config(self, callback_url=None):
    """配置开发选项
    :param callback_url: 商户回调地址。收取微信的授权通知、开票通知、插卡通知等相关通知。示例值：'https://pay.weixin.qq.com/callback'
    """
    if not callback_url:
        callback_url = self._notify_url
    params = {}
    params.update({'callback_url': callback_url})
    path = '/v3/new-tax-control-fapiao/merchant/development-config'
    return self._core.request(path, method=RequestType.POST, data=params)


def fapiao_merchant_config(self):
    """查询商户配置的开发选项
    """
    path = '/v3/new-tax-control-fapiao/merchant/development-config'
    return self._core.request(path)


def fapiao_title_url(self, fapiao_apply_id, source, total_amount, openid, appid=None,
                     seller_name=None, show_phone_cell=False, must_input_phone=False,
                     show_email_cell=False, must_input_email=False):
    """获取抬头填写链接
    """
    path = '/v3/new-tax-control-fapiao/user-title/title-url?'
    if fapiao_apply_id:
        path += 'fapiao_apply_id=%s' % fapiao_apply_id
    else:
        raise Exception('fapiao_apply_id is not assigned.')
    if source:
        path += '&source=%s' % source
    else:
        raise Exception('source is not assigned.')
    if total_amount:
        path += '&total_amount=%s' % total_amount
    else:
        raise Exception('total_amount is not assigned.')
    if appid:
        path += '&appid=%s' % appid
    else:
        path += '&appid=%s' % self._appid
    if openid:
        path += '&openid=%s' % openid
    else:
        raise Exception('openid is not assigned.')
    if seller_name:
        path += '&seller_name=%s' % seller_name
    if show_phone_cell:
        path += '&show_phone_cell=true'
    if must_input_phone:
        path += '&must_input_phone=true'
    if show_email_cell:
        path += '&show_email_cell=true'
    if must_input_email:
        path += '&must_input_email=true'
    return self._core.request(path)


def fapiao_title(self, fapiao_apply_id, scene='WITH_WECHATPAY'):
    """获取用户填写的抬头
    :param fapiao_apply_id:
    :param scene:
    """
    path = '/v3/new-tax-control-fapiao/user-title'
    if fapiao_apply_id:
        path += 'fapiao_apply_id=%s' % fapiao_apply_id
    else:
        raise Exception('fapiao_apply_id is not assigned.')
    path += '&scene=%s' % scene
    return self._core.request(path)


def fapiao_tax_codes(self, offset=0, limit=20):
    """获取商品和服务税收分类对照表
    :param offset:
    :param limit:
    """
    path = '/v3/new-tax-control-fapiao/merchant/tax-codes?offset=%s&limit=%s' % (offset, limit)
    return self._core.request(path)


def fapiao_merchant_base_info(self):
    """获取商户开票基础信息
    """
    path = '/v3/new-tax-control-fapiao/merchant/base-information'
    return self._core.request(path)


def fapiao_applications(self, fapiao_apply_id, buyer_information, fapiao_information, scene='WITH_WECHATPAY'):
    """开具电子发票
    :fapiao_apply_id: 发票申请单号，示例值：'4200000444201910177461284488'
    :buyer_information: 购买方信息，示例值：{'type':'ORGANIZATION','name':'深圳市南山区测试企业'}
    :fapiao_information: 需要开具的发票信息，示例值：[{'fapiao_id':'20200701123456','total_amount':382895,'need_list':False,'items':[{'tax_code':'3010101020203000000','quantity':100000000,'total_amount':'429900','discount':False}]}]
    """
    params = {}
    if fapiao_apply_id:
        params.update({'fapiao_apply_id': fapiao_apply_id})
    else:
        raise Exception('fapiao_aply_id is not assigned.')
    if buyer_information:
        params.update({'buyer_information': buyer_information})
    else:
        raise Exception('buyer_information is not assigned.')
    if fapiao_information:
        params.update({'fapiao_information': fapiao_information})
    else:
        raise Exception('fapiao_information is not assigned.')
    params.update({'scene': scene})
    path = '/v3/new-tax-control-fapiao/fapiao-applications'
    return self._core.request(path, method=RequestType.POST, data=params)


def fapiao_query(self, fapiao_apply_id, fapiao_id=None):
    """查询电子发票
    :param fapiao_apply_id: 发票申请单号，示例值：'4200000444201910177461284488'
    :param fapiao_id: 商户发票单号，示例值：'20200701123456'
    """
    path = '/v3/new-tax-control-fapiao/fapiao-applications/%s' % fapiao_apply_id
    if fapiao_id:
        path += '?fapiao_id=%s' % fapiao_id
    return self._core.request(path)


def fapiao_reverse(self, fapiao_apply_id, reverse_reason, fapiao_information):
    """冲红电子发票
    :param fapiao_apply_id: 
    """
    if fapiao_apply_id:
        path = '/v3/new-tax-control-fapiao/fapiao-applications/%s/reverse' % fapiao_apply_id
    else:
        raise Exception('fapiao_apply_id is not assigned.')
    params = {}
    if reverse_reason:
        params.update({'reverse_reason': reverse_reason})
    else:
        raise Exception('reverse_reason is not assigned.')
    if fapiao_information:
        params.update({'fapiao_information': fapiao_information})
    else:
        raise Exception('fapiao_information is not assigned.')
    return self._core.request(path, method=RequestType.POST, data=params)


def fapiao_upload_file(self, filepath):
    """上传电子发票文件
    :filepath: 电子发票文件路径，只支持pdf和odf两种格式，示例值：'./fapiao/0001.pdf'
    """
    if not (filepath and os.path.exists(filepath) and os.path.isfile(filepath)):
        raise Exception('filepath is not assigned or not exists')
    f = open(filepath, mode='rb')
    content = f.read()
    f.close()
    h = SM3()
    h.update(content)
    digest = h.sm3_final()
    filename = os.path.basename(filepath)
    filetype = os.path.splitext(filename)[-1][1:].upper()
    mimes = {
        'PDF': 'application/pdf',
        'ODF': 'application/odf'
    }
    if filetype not in mimes:
        raise Exception('sdk does not support this file type.')
    params = {}
    params.update({'meta': '{"file_type":"%s","digest_alogrithm":"SM3","digest":"%s"}' % (filetype, digest)})
    files = [('file', (filename, content, mimes[filetype]))]
    path = '/v3/new-tax-control-fapiao/fapiao-applications/upload-fapiao-file'
    return self._core.request(path, method=RequestType.POST, data=params, sign_data=params.get('meta'), files=files)


def fapiao_insert_cards(self, fapiao_apply_id, buyer_information, fapiao_card_information, scene='WITH_WECHATPAY'):
    """将电子发票插入微信用户卡包
    :param fapiao_apply_id: 发票申请单号，示例值：'4200000444201910177461284488'
    :param buyer_information: 
    """
    if fapiao_apply_id:
        path = '/v3/new-tax-control-fapiao/fapiao-applications/%s/insert-cards' % fapiao_apply_id
    else:
        raise Exception('fapiao_apply_id is not assigned.')
    params = {}
    if buyer_information:
        params.update({'buyer_information': buyer_information})
    else:
        raise Exception('buyer_information is not assigned.')
    if fapiao_card_information:
        params.update({'fapiao_card_information': fapiao_card_information})
    else:
        raise Exception('fapiao_card_information is not assigned.')
    params.update({'scene': scene})
    return self._core.request(path, method=RequestType.POST, data=params)