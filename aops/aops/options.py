#coding=utf-8

from django.utils.translation import ugettext_lazy
from django.utils.translation import ugettext

from libs.common import Common


class GLOBAL_OPTIONS(Common):

    def __init__(self, *args, **kwargs):
        self.trans_type = kwargs.get('trans_type', 'lazy')
        self.OPTIONS = {}
        self.set_trans(trans_type=self.trans_type)


    def original_output(self, var_s=''):
            return var_s


    def set_trans(self, **kwargs):
        self.trans_type = kwargs.get('trans_type', self.trans_type)
        if self.trans_type == 'lazy':
            self.trans  =  ugettext_lazy
        elif self.trans_type == 'original':
            self.trans = self.original_output
        elif self.trans_type == 'immediate':
            self.trans = ugettext
        else:
            self.trans = self.original_output

        self.set_options()


    def set_option(self, var_name, val):
        setattr(self, var_name, val)
        self.OPTIONS[var_name] = val


    def set_options(self):
        self.set_option('INT_CHOICES',
            (
                (0,  self.trans('True')),
                (1,  self.trans('False')),
            )
        )

        self.set_option('STATUS_CHOICES',
            (
                (0,  self.trans('Valid')),
                (1,  self.trans('Spare')),
                (2,  self.trans('Invalid')),
            )
        )

        self.set_option('CONTRACT_CHOICES',
            (
                (0, self.trans('Internal Protocol')),
                (1, self.trans('Purchase Contract')),
                (2, self.trans('Contract')),
            )
        )

        self.set_option('OPERATOR_CHOICES',
            (
                ('cmcc', self.trans('CMCC')),
                ('cucc', self.trans('CUCC')),
                ('ctcc', self.trans('CTCC')),
                ('gwbh', self.trans('GWBN')),
                ('cht', self.trans('CHT')),
                ('bgp', self.trans('BGP')),
                ('lan', self.trans('LAN'))
            )
        )

        self.set_option('DOMAIN_RECORD_TYPE_CHOICES',
            (
                ('0', self.trans('A')),
                ('1', self.trans('CNAME')),
                ('2', self.trans('MX')),
                ('3', self.trans('NS')),
                ('4', self.trans('TXT')),
            )
        )

        self.set_option('NETWORKING_HARDWARE_TYPE_CHOICES',
            (
                ('switch',   self.trans('Switch')),
                ('router',   self.trans('Router')),
                ('hub',      self.trans('Hub')),
                ('gateway',  self.trans('Gateway')),
                ('vpn',      self.trans('VPN')),
                ('firewall', self.trans('Firewall')),
                ('modem',    self.trans('Modem')),
                ('bridge',   self.trans('Bridge')),
                ('repeater', self.trans('Repeater')),
            )
        )

        self.set_option('IP_PURPOSE_CHOICES',
            (
                ('0', self.trans('NORMAL')),
                ('1', self.trans('ADMIN')),
            )
        )

        self.set_option('TF_CHOICES',
            (
                (True, self.trans('True')),
                (False, self.trans('False')),
            )
        )

        self.set_option('PROTOCOL_CHOICES',
            (
                ('0', self.trans('SOCKET')),
                ('1', self.trans('HTTP')),
                ('2', self.trans('HTTPS')),
            )
        )

        self.set_option('PROXY_CHOICE',
            (
                ('0', self.trans('NGINX')),
                ('1', self.trans('HAPROXY')),
                ('2', self.trans('LVS')),
                ('3', self.trans('APACHE')),
                ('4', self.trans('SQUID')),
                ('5', self.trans('VARNISH')),
            )
        )

        self.set_option('PROGRAM_CHOICES',
            (
                ('0', self.trans('Java')),
                ('1', self.trans('Python')),
                ('2', self.trans('Perl')),
                ('3', self.trans('PHP')),
                ('4', self.trans('Ruby')),
                ('5', self.trans('Shell')),
            )
        )

        self.set_option('RUN_CHOICES',
            (
                ('0', self.trans('Tomcat')),
                ('1', self.trans('Resin')),
                ('2', self.trans('JBoss')),
                ('3', self.trans('Glassfish')),
                ('4', self.trans('WSCGI')),
                ('5', self.trans('UWSCGI')),
            )
        )

        self.set_option('DEPLOY_CHOICES',
            (
                ('0', self.trans('Normal')),#只是简单粗暴的全部业务机瞬间重启。
                ('1', self.trans('NormalTest')), #只开启一台业务机进行预发布。
                ('2', self.trans('IntervalTest')), #每个代理后边只开启一台业务机进行预发布。
                ('3', self.trans('Interval')),#间隔，每次发布，每个代理后面轮流开启一台业务机，直至所有业务机都发布。
                ('4', self.trans('Delay')),#延迟，在前一台业务机发布后延迟多久再发布另一台业务机。
                ('5', self.trans('DelayInterval')),#间隔+延迟。
            )
        )

        self.set_option('DEPLOY_SYSTEM_STATUS_CHOICES',
            (
                ('0', self.trans('None')),
                ('1', self.trans('Start')),
                ('2', self.trans('Init_Machine_Start')),
                ('3', self.trans('Init_Machine_Config_RAID_Start')),
                ('4', self.trans('Init_Machine_Config_RAID_End')),
                ('5', self.trans('Init_Machine_Config_BIOS_Start')),
                ('6', self.trans('Init_Machine_Config_BIOS_End')),
                ('7', self.trans('Init_Machine_Config_Control_Card_Start')),
                ('8', self.trans('Init_Machine_Config_Control_Card_End')),
                ('9', self.trans('Init_Machine_End')),
                ('10', self.trans('Deploy_System_Start')),
                ('11', self.trans('Deploy_System_End')),
                ('12', self.trans('Init_System_Start')),
                ('13', self.trans('Init_System_End')),
                ('14', self.trans('End')),
            )
        )


        self.set_option('DEPLOY_SYSTEM_TYPE_CHOICES',
                        (
                            ('0', self.trans('None')),
                            ('1', self.trans('ALL')), #包涵所有操作
                            ('2', self.trans('ALL_Machine')), #包涵init_raid, init_bios, init_control_card
                            ('3', self.trans('Init_Machine_Config_RAID')),
                            ('4', self.trans('Init_Machine_Config_BIOS')),
                            ('3', self.trans('Init_Machine_Config_Control_Card')),
                            ('5', self.trans('ALL_System')),  #包涵deploy_system + init_system
                            ('6', self.trans('Deploy_System')),
                            ('7', self.trans('Init_System')),
                        )
                        )


    def trans_tuple_to_dict(self, v_tuple):
        n_dict = {}
        for vv in v_tuple:
            n_dict[vv[1]] = vv[0]
        return n_dict


    def reverse_dict(self, dict={}):
        n_dict = {}
        for key in dict:
            n_dict[dict[key]] = key
        return n_dict


    def get_option(self, var_name=None):
        return getattr(self, var_name)


    def get_dict_option(self, var_name=None):
        var = getattr(self, var_name)
        return self.trans_tuple_to_dict(var)


    def get_reverse_dict_option(self, var_name=None):
        dict = self.get_dict_option(var_name)
        n_dict = self.reverse_dict(dict)
        return n_dict




def DECLARE_OPTIONS(trans_type='lazy'):
    GB_OP = GLOBAL_OPTIONS (trans_type=trans_type)
    for option in GB_OP.OPTIONS:
        exec('global  %s' % option)
        exec('%s = GB_OP.get_option("%s")' % (option, option)  )

