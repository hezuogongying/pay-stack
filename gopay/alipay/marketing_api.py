"""
支付宝营销API
包含现金红包、代金券、营销活动等功能
"""

import logging
from typing import Dict, Any
from gopay.utils.datastructure import BodyMap, ResponseData


logger = logging.getLogger(__name__)


class AlipayMarketingMixin:
    """
    支付宝营销API Mixin类
    包含现金红包、代金券、营销活动等营销功能
    """

    def alipay_fund_trans_order_query(self, params: BodyMap) -> ResponseData:
        """
        查询转账订单接口
        文档: https://opendocs.alipay.com/open/02cbr8

        :param params: 参数对象
        :return: 查询结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.fund.trans.order.query", biz_content)

    def alipay_trade_order_settle(self, params: BodyMap) -> ResponseData:
        """
        统一收单交易结算接口
        文档: https://opendocs.alipay.com/open/02cbr8

        :param params: 参数对象
        :return: 结算结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.trade.order.settle", biz_content)

    def alipay_trade_order_onsettle(self, params: BodyMap) -> ResponseData:
        """
        统一收单交易预结算接口
        :param params: 参数对象
        :return: 预结算结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.trade.order.onsettle", biz_content)

    def alipay_user_authzh详情(self, params: BodyMap) -> ResponseData:
        """
        支付宝会员卡信息查询
        :param params: 参数对象
        :return: 查询结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.user.auth.zh Details", biz_content)

    def alipay_commerce_cityfacilitator_station_upload(self, params: BodyMap) -> ResponseData:
        """
        公交线路上传接口
        :param params: 参数对象
        :return: 上传结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.commerce.cityfacilitator.station.upload", biz_content)

    def alipay_commerce_cityfacilitator_station_query(self, params: BodyMap) -> ResponseData:
        """
        公交线路查询接口
        :param params: 参数对象
        :return: 查询结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.commerce.cityfacilitator.station.query", biz_content)

    def alipay_commerce_cityfacilitator_station_delete(self, params: BodyMap) -> ResponseData:
        """
        公交线路删除接口
        :param params: 参数对象
        :return: 删除结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.commerce.cityfacilitator.station.delete", biz_content)

    def alipay_commerce_transport_offlinepoliceitem_create(self, params: BodyMap) -> ResponseData:
        """
        创建加油订单接口
        :param params: 参数对象
        :return: 创建结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.commerce.transport.offlinepoliceitem.create", biz_content)

    def alipay_commerce_transport_offlinepoliceitem_pay(self, params: BodyMap) -> ResponseData:
        """
        支付加油订单接口
        :param params: 参数对象
        :return: 支付结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.commerce.transport.offlinepoliceitem.pay", biz_content)

    def alipay_commerce_transport_offlinepoliceitem_cancel(self, params: BodyMap) -> ResponseData:
        """
        撤销加油订单接口
        :param params: 参数对象
        :return: 撤销结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.commerce.transport.offlinepoliceitem.cancel", biz_content)

    def alipay_commerce_transport_offlinepoliceitem_complete(self, params: BodyMap) -> ResponseData:
        """
        完成加油订单接口
        :param params: 参数对象
        :return: 完成结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.commerce.transport.offlinepoliceitem.complete", biz_content)

    def alipay_commerce_transport_offlinepoliceitem_query(self, params: BodyMap) -> ResponseData:
        """
        查询加油订单接口
        :param params: 参数对象
        :return: 查询结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.commerce.transport.offlinepoliceitem.query", biz_content)

    def alipay_commerce_taximeterinvoice_create(self, params: BodyMap) -> ResponseData:
        """
        创建出租车发票接口
        :param params: 参数对象
        :return: 创建结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.commerce.taximeterinvoice.create", biz_content)

    def alipay_commerce_taximeterinvoice_query(self, params: BodyMap) -> ResponseData:
        """
        查询出租车发票接口
        :param params: 参数对象
        :return: 查询结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.commerce.taximeterinvoice.query", biz_content)

    def alipay_commerce_operation_type_query(self, params: BodyMap) -> ResponseData:
        """
        场景化 capabilitytype 查询接口
        :param params: 参数对象
        :return: 查询结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.commerce.operation.type.query", biz_content)

    def alipay_commerce_piccdataupload(self, params: BodyMap) -> ResponseData:
        """
        平安数据上传接口
        :param params: 参数对象
        :return: 上传结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.commerce.piccdataupload", biz_content)

    def alipay_databiz_core_data_replay(self, params: BodyMap) -> ResponseData:
        """
        数据回流开放接口
        :param params: 参数对象
        :return: 回流结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.databiz.core.data.replay", biz_content)

    def alipay_eco_cplife_bill_create(self, params: BodyMap) -> ResponseData:
        """
        创建物业费账单接口
        :param params: 参数对象
        :return: 创建结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.eco.cplife.bill.create", biz_content)

    def alipay_eco_cplife_bill_query(self, params: BodyMap) -> ResponseData:
        """
        查询物业费账单接口
        :param params: 参数对象
        :return: 查询结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.eco.cplife.bill.query", biz_content)

    def alipay_eco_cplife_bill_pay(self, params: BodyMap) -> ResponseData:
        """
        支付物业费账单接口
        :param params: 参数对象
        :return: 支付结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.eco.cplife.bill.pay", biz_content)

    def alipay_eco_cplife_community_create(self, params: BodyMap) -> ResponseData:
        """
        创建小区接口
        :param params: 参数对象
        :return: 创建结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.eco.cplife.community.create", biz_content)

    def alipay_eco_cplife_community_query(self, params: BodyMap) -> ResponseData:
        """
        查询小区接口
        :param params: 参数对象
        :return: 查询结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.eco.cplife.community.query", biz_content)

    def alipay_eco_cplife_community_modify(self, params: BodyMap) -> ResponseData:
        """
        修改小区接口
        :param params: 参数对象
        :return: 修改结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.eco.cplife.community.modify", biz_content)

    def alipay_eco_cplife_room_create(self, params: BodyMap) -> ResponseData:
        """
        创建房间接口
        :param params: 参数对象
        :return: 创建结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.eco.cplife.room.create", biz_content)

    def alipay_eco_cplife_room_query(self, params: BodyMap) -> ResponseData:
        """
        查询房间接口
        :param params: 参数对象
        :return: 查询结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.eco.cplife.room.query", biz_content)

    def alipay_eco_cplife_room_modify(self, params: BodyMap) -> ResponseData:
        """
        修改房间接口
        :param params: 参数对象
        :return: 修改结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.eco.cplife.room.modify", biz_content)

    def alipay_eco_mycar_parking_chargeorder_create(self, params: BodyMap) -> ResponseData:
        """
        创单接口
        :param params: 参数对象
        :return: 创建结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.eco.mycar.parking.chargeorder.create", biz_content)

    def alipay_eco_mycar_parking_chargeorder_pay(self, params: BodyMap) -> ResponseData:
        """
        支付接口
        :param params: 参数对象
        :return: 支付结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.eco.mycar.parking.chargeorder.pay", biz_content)

    def alipay_eco_mycar_parking_chargeorder_query(self, params: BodyMap) -> ResponseData:
        """
        查询接口
        :param params: 参数对象
        :return: 查询结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.eco.mycar.parking.chargeorder.query", biz_content)

    def alipay_eco_mycar_parking_chargingpile_notify(self, params: BodyMap) -> ResponseData:
        """
        充电桩设备状态同步接口
        :param params: 参数对象
        :return: 同步结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.eco.mycar.parking.chargingpile.notify", biz_content)

    def alipay_eco_mycar_parking_chargingpile_order_create(self, params: BodyMap) -> ResponseData:
        """
        创建充电订单接口
        :param params: 参数对象
        :return: 创建结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.eco.mycar.parking.chargingpile.order.create", biz_content)

    def alipay_eco_mycar_parking_chargingpile_order_pay(self, params: BodyMap) -> ResponseData:
        """
        充电订单支付接口
        :param params: 参数对象
        :return: 支付结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.eco.mycar.parking.chargingpile.order.pay", biz_content)

    def alipay_eco_mycar_parking_chargingpile_order_query(self, params: BodyMap) -> ResponseData:
        """
        充电订单查询接口
        :param params: 参数对象
        :return: 查询结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.eco.mycar.parking.chargingpile.order.query", biz_content)

    def alipay_eco_mycar_parking_agreement_query(self, params: BodyMap) -> ResponseData:
        """
        查询签约信息接口
        :param params: 参数对象
        :return: 查询结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.eco.mycar.parking.agreement.query", biz_content)

    def alipay_eco_mycar_parking_vehicle_query(self, params: BodyMap) -> ResponseData:
        """
        车牌信息查询接口
        :param params: 参数对象
        :return: 查询结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.eco.mycar.parking.vehicle.query", biz_content)

    def alipay_eco_mycar_parking_overtime_notify(self, params: BodyMap) -> ResponseData:
        """
        停车超时提醒接口
        :param params: 参数对象
        :return: 提醒结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.eco.mycar.parking.overtime.notify", biz_content)

    def alipay_eco_mycar_parking_enterinfo_push(self, params: BodyMap) -> ResponseData:
        """
        车辆入场信息推送接口
        :param params: 参数对象
        :return: 推送结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.eco.mycar.parking.enterinfo.push", biz_content)


# 将 Mixin 的方法添加到 AlipayClient 类
def inject_marketing_methods():
    """动态注入营销API方法到 AlipayClient"""
    from gopay.alipay.client import AlipayClient

    for method_name in dir(AlipayMarketingMixin):
        if not method_name.startswith("_"):
            method = getattr(AlipayMarketingMixin, method_name)
            if callable(method):
                setattr(AlipayClient, method_name, method)


# 自动注入
inject_marketing_methods()
