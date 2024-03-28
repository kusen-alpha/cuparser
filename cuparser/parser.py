# -*- coding:utf-8 -*-
# author: kusen
# email: 1194542196@qq.com
# date: 2023/11/28

import re

from .configs import ALL_UNIT_REGEX, NUMBER_REGEX, UNIT_MAP
from .configs import CLEAR_REGEX_LIST, SUB_REGEX_LIST


class CUParser(object):
    @classmethod
    def parse_unit(cls, s=None, regex_list=ALL_UNIT_REGEX):
        if not s:
            return
        for regex, unit in regex_list:
            if regex.search(s):
                return unit

    @classmethod
    def parse_num(cls, s, regex=NUMBER_REGEX):
        for _regex in CLEAR_REGEX_LIST:
            s = _regex.sub('', s)
        for _regex in SUB_REGEX_LIST:
            s = _regex.sub('@', s)
        nums = regex.findall(s)
        if not nums:
            return
        try:
            return float(nums[0])
        except:
            pass

    @classmethod
    def _return(cls, num, unit, show_unit):
        if show_unit:
            return num, unit
        return num

    @classmethod
    def parse(cls, s, unit=None, unit_regex_list=None, show_unit=False):
        """

        :param s: string
        :param unit_regex_list: [(regex1, unit), ...]
        :param unit:
        :param show_unit:
        :return:
        """
        if not s:
            if show_unit:
                return None, None
            return None
        if not unit_regex_list:
            unit_regex_list = []
        unit_regex_list = [(re.compile(regex), _unit) for regex, _unit in
                           unit_regex_list]
        result_unit = unit if unit in UNIT_MAP else None or cls.parse_unit(
            unit, unit_regex_list) or cls.parse_unit(unit) or cls.parse_unit(
            s, unit_regex_list) or cls.parse_unit(s)
        num = cls.parse_num(s)
        if not num:
            return cls._return(num, result_unit, show_unit)
        return cls._return(
            round(num * UNIT_MAP[result_unit],
                  2) if result_unit in UNIT_MAP else num, result_unit,
            show_unit)


parse = CUParser.parse
parse_unit = CUParser.parse
